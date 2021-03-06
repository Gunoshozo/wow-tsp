import tsp
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import PIL
import tsp as tsp
from PIL import Image

def parse(filename):
    file = open(filename,'r')
    points = np.empty((0,2),dtype=np.float)
    while True:
        line = file.readline()
        if line == '':
            break
        coords = line.split(' ')
        points = np.append(points,[[np.float(i) for i in coords]],axis=0)
    return points

def get_distance_between_points(a,b):
    return scipy.linalg.norm(a-b)

def get_distance_matrix(points:np.ndarray):
    length = points.shape[0]
    mtrx = np.zeros((length,length))
    for i in range(length):
        for j in range(length):
            if i < j:
                mtrx[i,j] = get_distance_between_points(points[i],points[j])
            elif i == j:
                continue
            else:
                mtrx[i, j] = mtrx[j, i]

    return mtrx

def draw_line(image, p1,p2,size):
    x0,y0 = p1
    x1,y1 = p2
    pixels = image.load()
    steep = False
    x0 = int(x0)
    x1 = int(x1)
    y0 = int(y0)
    y1 = int(y1)
    if np.abs(x0 - x1) < np.abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range(x0, x1, 1):
        t = (x - x0) / (x1 - x0)
        y = int(y0 * (1. - t) + y1 * t)
        if 0 <= x < size[0] and 0 <= y < size[1]:
            if steep:
                pixels[x, y] = (255,255,255)
            else:
                pixels[y, x] = (255,255,255)

def fat_dot(image,p1,size):
    x0,y0 = p1
    pixels = image.load()
    x0 = int(x0)
    y0 = int(y0)
    for x in range(x0-size,x0+size):
        for y in range(y0-size,y0+size):
            pixels[y, x] = (255, 0, 0)


def draw_map(coords,size):
    size = size
    img = Image.new(mode='RGB',size=size)
    for i in range(-1,len(coords)-1):
        p1 = [coords[i][1],coords[i][0]]
        p2 = [coords[i+1][1],coords[i+1][0]]
        draw_line(img,p1,p2,size)
        fat_dot(img,p1,6)
        fat_dot(img,p2,6)
        img.show()
    img.show()
    img.save("opt_path.png")

def tsp_solve(coords):
    dist_mtrx = get_distance_matrix(points)
    r = range(len(points))
    dist = {(i, j): dist_mtrx[i][j] for i in r for j in r}
    tsp_sol = tsp.tsp(r, dist)
    return points[tsp_sol[1]]

def convert(val,old_min,old_max,new_min,new_max):
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    return (((val - old_min) * new_range) / old_range) + new_min

v_convert = np.vectorize(convert,excluded=['old_min','old_max','new_min','new_max'])

if __name__ == '__main__':
    filename = 'coords'
    points = parse(filename)
    size = (1920,1080)
    points = tsp_solve(points)
    points[:,0] = v_convert(points[:,0],0,100,0,size[0])
    points[:,1] = v_convert(points[:,1],0,100,0,size[1])
    draw_map(points,size)
