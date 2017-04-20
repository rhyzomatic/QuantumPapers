from qutip import *
from scipy import *
import numpy as np
import os

num_points = 20

def animate_bloch(xz, yz, zz, dir_name):
    b = Bloch()
    b.vector_color = ['r']
    #b.view = [45,10]
    #b.size = [2000, 2000]
    b.figsize = [10, 10]
    b.font_size = 30
    b.zlabel = ['$z=\\left|0\\right>$', '$z=\\left|1\\right>$']
    print(b)
    for i in range(num_points):
        b.clear()
        b.add_points([xz[:i+1], yz[:i+1], zz[:i+1]])
        b.add_vectors([xz[i], yz[i], zz[i]])
        b.save(dirc=dir_name) #saving images to temp directory in current working directory

    os.system("ffmpeg -y -i "+dir_name+"/bloch_%01d.png "+dir_name+"/movie.mp4")

xz = np.zeros(num_points)
yz = [np.sin(th) for th in np.linspace(0, pi ,num_points)]
zz = [np.cos(th) for th in np.linspace(0, pi, num_points)]
#animate_bloch(xz, yz, zz, "pauli_x")

theta = np.linspace(0, pi/2, num_points)
phi = np.append(np.linspace(0, pi/4, num_points/2), np.linspace(pi/4, 0, num_points/2))
xz = np.sin(theta)*np.cos(phi)
yz = np.sin(theta)*np.sin(phi)
zz = np.cos(theta)
#animate_bloch(xz, yz, zz, "hadamard")

def rotation_vector(initial_state, axis, theta):
    x, y, z = initial_state
    u, v, w = axis
    return [u*(u*x + v*y + w*z)*(1 - cos(theta)) + x*cos(theta) + (-w*y + v*z)*sin(theta),
            v*(u*x + v*y + w*z)*(1 - cos(theta)) + y*cos(theta) + (w*x - u*z)*sin(theta),
            w*(u*x + v*y + w*z)*(1 - cos(theta)) + z*cos(theta) + (-v*x + u*y)*sin(theta)]

def rotate_bloch(initial_state, axis, rotation, dir_name, num_frames=350, num_points=50):
    b = Bloch()
    #b.vector_color = ['r']
    b.figsize = [10, 10]
    b.font_size = 30
    b.zlabel = ['$z=\\left|0\\right>$', '$z=\\left|1\\right>$']
    points = []
    for frame, theta in enumerate(np.linspace(0, rotation, num_frames)):
        b.clear()
        b.add_vectors(axis)
        vec = rotation_vector(initial_state, axis, -theta)
        if frame % (1000 // 50) == 0:
            points.append(vec)
        b.add_points(list(map(list, zip(*points))))
        b.add_vectors(vec)
        b.save(dirc=dir_name)

    os.system("ffmpeg -y -r 60 -i "+dir_name+"/bloch_%01d.png "+dir_name+"/"+dir_name+str(initial_state)+".mp4")

for inits in ((0, 0, 1), (0, -1, 0)):
    rotate_bloch(inits, (1/sqrt(2), 0, 1/sqrt(2)), pi, "hadamard")
    rotate_bloch(inits, (1, 0, 0), pi, "pauli_x")
    rotate_bloch(inits, (0, 1, 0), pi, "pauli_y")
    rotate_bloch(inits, (0, 0, 1), pi, "pauli_z")

"""
b = Bloch()
b.add_vectors([1/sqrt(2), 0, 1/sqrt(2)])
b.show()
"""
