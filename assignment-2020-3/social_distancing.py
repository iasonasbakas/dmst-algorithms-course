import argparse
import pprint
import sys
import math
import random
import svgwrite
import matplotlib

parser = argparse.ArgumentParser()
parser.add_argument("-items", "--items", type=int, help="items")
parser.add_argument("-r", "--radius", type=int, help="radius")
parser.add_argument("--min_radius", type=int, help="minimum radius")
parser.add_argument("--max_radius", type=int, help="maximum radius")
parser.add_argument("-b", "--boundary", help="boundary")
parser.add_argument("-s", "--seed", type=int, help="seed")
parser.add_argument("output_file", help="output file")
args = parser.parse_args()

SEED = args.seed
if SEED:
    number = random.seed(SEED)

def write_output_file(circles, output_file=args.output_file, boundary = args.boundary):
    with open(output_file, 'w') as f:
        for circle in circles:
            f.write("{0:0.2f} ".format(circle[0]))
            f.write("{0:0.2f} ".format(circle[1]))
            f.write("{:d}\n".format(circle[2]))
        if boundary:
            with open(boundary, 'r') as b:
                for line in b:
                    f.write(line)

def get_boundary(boundary=args.boundary):
    bounds = []
    with open(boundary, 'r') as b:
        for line in b:
            coordinates = [float(x) for x in line.split()]
            bounds.append(coordinates)
    return bounds

def find_tanged_circle(circleM, circleN, r):
    dx = circleN[0] - circleM[0]
    dy = circleN[1] - circleM[1]
    d = math.sqrt(dx**2 + dy**2)
    r1 = circleM[2] + r
    r2 = circleN[2] + r
    l = (r1**2 - r2**2 + d**2) / (2*d**2)
    e = math.sqrt(r1**2/d**2 - l**2)
    x = circleM[0] + l*dx - e*dy
    y = circleM[1] + l*dy + e*dx
    x = round(x, 2)
    y = round(y, 2)
    circleK = (x, y, r)
    return circleK

def find_distance(circle, line_segment):
    u = [line_segment[0], line_segment[1]]
    v = [line_segment[2], line_segment[3]]
    l2 = (u[0] - v[0])**2 + (u[1] - v[1])**2
    if l2 == 0:
        d = math.sqrt((u[0] - circle[0])**2 + (u[1] - circle[1])**2)
    else:
        t = ((circle[0] - u[0]) * (v[0] - u[0]) + (circle[1] - u[1]) * (v[1] - u[1])) / l2
        t = max(0, min(1, t))
        p = []
        p.append(u[0] + t * (v[0] - u[0]))
        p.append(u[1] + t * (v[1] - u[1]))
        d = math.sqrt((p[0] - circle[0])**2 + (p[1] - circle[1])**2)
    d = round(d, 2)
    return d

def check_circle_to_boundary(circle, bounds):
    available = True
    for line in bounds:
        if find_distance(circle, line) < circle[2]:
            available = False
    return available

def random_radius(min=args.min_radius, max=args.max_radius):
    radius = random.randint(min, max)
    return radius

def add_starting_circles(start, r=args.radius, min=args.min_radius, max=args.max_radius):
    space = []
    polygon = {}
    polygon_backwards = {}
    alive = []
    if r:
        circle1 = (start[0], start[1], r)
        circle2 = (circle1[0] + 2*r, circle1[1], r)
    else:
        circle1 = (start[0], start[1], random_radius())
        r2 = random_radius()
        circle2 = (circle1[0] + circle1[2] + r2, circle1[1], r2)
    space.append(circle1)
    space.append(circle2)
    polygon[circle1] = circle2
    polygon[circle2] = circle1
    polygon_backwards[circle2] = circle1
    polygon_backwards[circle1] = circle2
    alive.append(circle1)
    alive.append(circle2)
    return space, polygon, polygon_backwards, alive

def find_closest_circle_to_start(polygon, start):
    min_dist = sys.maxsize
    closest_circle = 0
    for circle in polygon:
        d = math.sqrt((circle[0] - start[0])**2 + (circle[1] - start[1])**2)
        d = round(d, 2)
        if d < min_dist:
            min_dist = d
            closest_circle = circle
    return closest_circle

def circle_intersects(Ci, Cj):
    distance = math.sqrt((Ci[0] - Cj[0])**2 + (Ci[1] - Cj[1])**2)
    distance = round(distance)
    sum_radius = Ci[2] + Cj[2]
    if distance < sum_radius:
        return True
    else:
        return False

def check_intersections(polygon, polygon_backwards, Cm, Cn, Ci):
    intersected_circles = []
    circle = Cn
    Cj = None
    direction = None
    while circle != Cm:
        if circle_intersects(Ci, circle):
            intersected_circles.append(circle)
        circle = polygon.get(circle)
    if intersected_circles:
        Cj1 = intersected_circles[0]
        Cj2 = intersected_circles[-1]
        counter1 = 0
        counter2 = 0
        while Cn != Cj1:
            counter1 += 1
            Cn = polygon.get(Cn)
        while Cm != Cj2:
            counter2 += 1
            Cm = polygon_backwards.get(Cm)
        if counter2 < counter1:
            direction = "beforeCm"
            Cj = Cj2
        else:
            direction = "afterCn"
            Cj = Cj1
    return Cj, direction

def remove_polygon_circles(Cm, Cn, Cj, direction, polygon, polygon_backwards, undo):
    if direction == "beforeCm":
        circle = polygon.get(Cj)
        while circle != Cn:
            circle = polygon.pop(circle)
            polygon_backwards.pop(circle)
        Cm = Cj
        polygon[Cm] = Cn
        polygon_backwards[Cn] = Cm
    if direction == "afterCn":
        circle = polygon.get(Cm)
        while circle != Cj:
            circle = polygon.pop(circle)
            polygon_backwards.pop(circle)
        Cn = Cj
        polygon[Cm] = Cn
        polygon_backwards[Cn] = Cm
    return Cm, Cn, polygon, polygon_backwards

def create_circles(start, items=args.items, r=args.radius):
    space, polygon, polygon_backwards = add_starting_circles(start, r)
    skipstep2 = False
    if not r:
        random = True
        r = random_radius()
    else:
        random = False
    while len(space) != items:
        if not skipstep2:
            Cm = find_closest_circle_to_start(polygon, start)
        Cn = polygon.get(Cm)
        Ci = find_tanged_circle(Cm, Cn, r)
        Cj, direction = check_intersections(polygon, polygon_backwards, Cm, Cn, Ci)
        if not Cj:
            polygon[Cm] = Ci
            polygon[Ci] = Cn
            polygon_backwards[Ci] = Cm
            polygon_backwards[Cn] = Ci
            space.append(Ci)
            if random:
                r = random_radius()
            skipstep2 = False
        else:
            Cm, Cn, polygon, polygon_backwards = remove_polygon_circles(Cm, Cn, Cj, direction, polygon, polygon_backwards)
            skipstep2 = True
    print(len(space))
    return space

start = (0.00, 0.00)
if args.boundary:
    bounds = get_boundary()
space = create_circles(start)
write_output_file(space)