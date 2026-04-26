import math

def get_distance(p1, p2):
    # This function calculates the distance between the starting point
    # of the mouse click and the current position to determine the radius.
    # Formula: sqrt((x2-x1)^2 + (y2-y1)^2)
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)