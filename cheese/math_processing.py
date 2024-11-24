import numpy as np

def classify_polar_lines(lines, angle_threshold):
    vertical_lines = []
    horizontal_lines = []

    for line in lines:
        for rho, theta in line:
            if abs(theta - 0) < angle_threshold or abs(theta - np.pi) < angle_threshold:
                horizontal_lines.append(line)
            elif abs(theta - np.pi/2) < angle_threshold:
                vertical_lines.append(line)
    return vertical_lines, horizontal_lines

def line_distance(line1, line2):
    rtho1, theta1 = line1
    rtho2, theta2 = line2
    return abs(rtho1 - rtho2)

def filter_close_lines(lines, distance_threshold, angle_threshold):

    filtered_lines = []

    for line in lines:
        rho, theta = line[0]
        add = True

        for filtered_line in filtered_lines:
            if line_distance(line[0], filtered_line[0]) < distance_threshold and abs(theta - filtered_line[0][1]) < angle_threshold:
                add = False
                break
        if add:
            filtered_lines.append(line)
    return filtered_lines

def polar_to_cartesian(line, max_length):
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + max_length * (-b))
    y1 = int(y0 + max_length * (a))
    x2 = int(x0 - max_length * (-b))
    y2 = int(y0 - max_length * (a))
    return x1, y1, x2, y2

def intersection_point(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if det != 0:
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det
        return (int(x), int(y))
    else:
        return None
    
'''
def intersection_point(line1, line2):
    rho1, theta1 = line1
    rho2, theta2 = line2

    A1 = np.cos(theta1)
    B1 = np.sin(theta1)
    C1 = rho1

    A2 = np.cos(theta2)
    B2 = np.sin(theta2)
    C2 = rho2

    det = A1 * B2 - A2 * B1
    dx = C1 * B2 - C2 * B1
    dy = A1 * C2 - A2 * C1

    if det != 0:
        x = dx / det
        y = dy / det
        return (int(x), int(y))
    else:
        return None
'''

def filter_close_points(points, distance_threshold):
    filtered_points = []

    for point in points:
        add = True

        for filtered_point in filtered_points:
            if np.linalg.norm(np.array(point) - np.array(filtered_point)) < distance_threshold:
                add = False
                break
        if add:
            filtered_points.append(point)
    return filtered_points

def sort_points(points):
    points_sorted_x = sorted(points, key=lambda point: (point[1], point[0]))

    sorted_intersection_points = []

    for i in range(0, len(points_sorted_x), 9):
        row = points_sorted_x[i:i+9]
        sorted_row = sorted(row, key=lambda point: point[0])
        sorted_intersection_points.extend(sorted_row)

    return sorted_intersection_points

def get_indices(columns, rows):
    indices = []
    for i in range(columns):
        k1 = i * (rows + 1)
        k2 = k1 + rows + 1

        for j in range(rows):
           indices.append((k1 + j, k1 + j + 1, k2 + j, k2 + j + 1))

    return indices