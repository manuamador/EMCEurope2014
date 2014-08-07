# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 15:06:20 2014

@author: e68972
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

a=1

n=100#number of radiating dipoles on the EUT
#generate the dipoles
theta_eut=arccos(2*rand(n,1)-1) #uniformly random along theta
phi_eut=2*pi*rand(n,1) #uniformly random along phi
x=a*cos(phi_eut)*sin(theta_eut)  
y=a*sin(phi_eut)*sin(theta_eut) 
z=a*cos(theta_eut) 
tilt=arccos(2*rand(n,1)-1)
azimut=2*pi*rand(n,1)
amp=rand(n) #random amplitude of the currents
amplitude=vstack((amp,amp,amp)).T



fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=amplitude, marker='o', s=100)
max_radius = 0.8
for axis in 'xyz':
    getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))
ax._axis3don = False
fig.savefig("eut.pdf",bbox="tight")
plt.show()