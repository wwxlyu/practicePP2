import math

def get_distance(p1, p2):
    # Calculates the distance between two points
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_equilateral_triangle(start, end):
    # Returns 3 points for an equilateral triangle
    x1, y1 = start
    side = get_distance(start, end)
    height = (math.sqrt(3) / 2) * side
    return [(x1, y1), (x1 - side/2, y1 + height), (x1 + side/2, y1 + height)]

def get_rhombus(start, end):
    # Returns 4 points for a rhombus
    x1, y1 = start
    x2, y2 = end
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return [(x1, y1 - dy), (x1 + dx, y1), (x1, y1 + dy), (x1 - dx, y1)]