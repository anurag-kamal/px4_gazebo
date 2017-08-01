#! /usr/bin/env python

from __future__ import print_function
import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry


all_data = []
rospy.init_node('grabber')
r = rospy.Rate(1)
time_ar=[]

def getArray():


    def joystick(data):
        t = data.header.stamp
        x = data.buttons[5]
        y = data.axes[1]
        z = data.axes[0]
        total=3
        all_data[:3] = [x, y, z]

    def camera1(data):
        image=Image()
        image.data=data.data
        l=len(all_data)
        m=len(image.data)
        all_data[l:l+m]=image.data

    def camera2(data):
        image=Image()
        image.data=data.data
        l=len(all_data)
        m=len(image.data)
        all_data[l:l+m]=image.data


    def camera3(data):
        image=Image()
        image.data=data.data
        l=len(all_data)
        m=len(image.data)
        all_data[l:l+m]=image.data

    def husky_odom(data):
        data=data.pose.position
        xp = data.pose.position.x
        yp = data.pose.position.y
        zo = data.pose.orientation.z
        wo = data.pose.orientation.w
        xl = data.twist.linear.x
        za = data.angular.z
        l=len(all_data)
        all_data[l:l+6] = [xp, yp, zo, wo, xl, za]

    def lidar(data):
	lidar=LaserScan()
        lidar.ranges=data.ranges
        n=len(lidar.ranges)
        l=len(all_data)
        all_data[l:l+n]=lidar.ranges


    rospy.Subscriber('/joy_teleop/joy', Joy, joystick, queue_size=1)
    rospy.Subscriber('/camera1/usb_cam/image_raw', Image, camera1, queue_size=1)
    rospy.Subscriber('/camera2/usb_cam2/image_raw', Image, camera2, queue_size=$
    rospy.Subscriber('/camera3/usb_cam3/image_raw', Image, camera3, queue_size=$
    rospy.Subscriber('/husky_velocity_controller', Odometry, husky_odom, queue_$
    rospy.Subscriber('/scan', LaserScan, lidar, queue_size=1)

    return all_data


if __name__ == "__main__":
    AA=[]
    try:
        while not rospy.is_shutdown():
            print('recording')
            print('...')
            AA.append(getArray())
            r.sleep()
    except KeyboardInterrupt:
        pass

    file_name = raw_input('\nname for file: ')
    if file_name != '':
        print("Saving...")
        np.save(file_name, AA)
        print("Saved as %s.npy" % file_name)
    else:
        print("Information discarded.")


