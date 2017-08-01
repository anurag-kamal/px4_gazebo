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



rospy.init_node('grabber')
r = rospy.Rate(5)
global time_ar
time_ar=[]
global j
j=[]
global c1
c1=[]
global c2
c2=[]
global c3
c3=[]
global h
h=[]
global li
li=[]
global X


def getArray():

    time = [0,0,0,0,0]
    def joystick(data):
	global j
	#print(data.header.stamp.to_sec())
	#time[0]=data.header.stamp.to_nsec()
        x = data.buttons[5]
        y = data.axes[1]
        z = data.axes[0]
        j=[x, y, z]

    def camera1(data):
	global c1
	time[0]=data.header.stamp.to_sec()+data.header.stamp.to_nsec()*1E-9
        image=Image()
        image.data=data.data
        c1=[image.data]

    def camera2(data):
	global c2
	time[1]=data.header.stamp.to_sec()+data.header.stamp.to_nsec()*1E-9
        image=Image()
        image.data=data.data
	c2=[image.data]

    def camera3(data):
	global c3
	time[2]=data.header.stamp.to_sec()+data.header.stamp.to_nsec()*1E-9
        image=Image()
        image.data=data.data
        c3=[image.data]

    def husky_odom(data):
        global h
	time[3]=data.header.stamp.to_sec()+data.header.stamp.to_nsec()*1E-9
        xp = data.pose.pose.position.x
        yp = data.pose.pose.position.y
        zo = data.pose.pose.orientation.z
        wo = data.pose.pose.orientation.w
        xl = data.twist.twist.linear.x
        za = data.twist.twist.angular.z
        h=([xp, yp, zo, wo, xl, za])

    def lidar(data):
	global li
	time[4]=data.header.stamp.to_sec()+data.header.stamp.to_nsec()*1E-9
        li=data.ranges


    rospy.Subscriber('/joy_teleop/joy', Joy, joystick, queue_size=1)
    rospy.Subscriber('/camera1/usb_cam/image_raw', Image, camera1, queue_size=1)
    rospy.Subscriber('/camera2/usb_cam2/image_raw', Image, camera2, queue_size=1)
    rospy.Subscriber('/camera3/usb_cam3/image_raw', Image, camera3, queue_size=1)
    rospy.Subscriber('/husky_velocity_controller/odom', Odometry, husky_odom, queue_size=1)
    rospy.Subscriber('/scan', LaserScan, lidar, queue_size=1)

    return time


if __name__ == "__main__":
    
    timeX=[]
    jX=np.array([])
    c1X=np.array([])
    c2X=np.array([])
    c3X=np.array([])
    hX=np.array([])
    liX=np.array([])

    try:
        while not rospy.is_shutdown():
            print('recording')
            print('...')
	    print('.')
            timeX=getArray()
	    jX=np.append(jX,j,axis=0)
	    c1X=np.append(c1X,c1,axis=0)
	    c2X=np.append(c2X,c2,axis=0)
	    c3X=np.append(c3X,c3,axis=0)
	    hX=np.append(hX,h,axis=0)
	    liX=np.append(liX,li,axis=0)
            r.sleep()
	    print(max(timeX)-min(timeX))
    except KeyboardInterrupt:
        pass

    file_name = raw_input('\nname for file: ')
    if file_name != '':
        print("Saving...")
        np.savez(file_name,timeX,jX,c1X,c2X,c3X,hX,liX)
        print("Saved as %s.npz" % file_name)
    else:
        print("Information discarded.")
