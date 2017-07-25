#!/usr/bin/env python
from __future__ import print_function
import matplotlib.pyplot as plt
import rospy
import numpy as np
from numpy import arange, pi, sqrt, arctan2, sin, cos
from sensor_msgs.msg import LaserScan  # Messages from Lidar System
from time import sleep
from sys import path, exit

robot_id = 3
target_id = 1
target_distance = 1.
gap_size = .6
map_bound = 3.

every_other = 4
increment = pi * .5 / 180
angles = arange(-3 * pi / 4, 3 * pi / 4 + increment, increment)

plt.ion()
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
lidar, = ax.plot([],[],'r.',markersize=10,label='Lidar')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
# ax.legend()
# ax.axis('equal')
ax.set_xlim([-3*pi/4,3*pi/4])
ax.set_ylim([0, 10])
plt.tight_layout()
data = [None, None]


class LidarLogger(object):

    def __init__(self):
        rospy.init_node('realtime_debugger', disable_signals=True)  # start the control node

        self.subscriber = rospy.Subscriber('/scan', LaserScan, self.readDistance, queue_size=1)

        while True:
            lidar.set_xdata(data[0])
            lidar.set_ydata(data[1])
            # plt.draw()
            fig.canvas.draw()
            

    def readDistance(self, scan):
        distances = np.array(list(scan.ranges))
        data[0] = angles
        data[1] = distances



if __name__ == "__main__":
    try:
        lidarLog = LidarLogger()
    except KeyboardInterrupt:
        plt.show(block=True)

