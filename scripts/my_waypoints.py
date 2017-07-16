#!/usr/bin/env python


import time
import threading
import rospy
import mavros
import thread


from math import *
from math import radians
from mavros.utils import *  
from mavros import setpoint
from tf.transformations import quaternion_from_euler


def getError(x, y=[0, 0, 0], bound=None):
    """Returns Euclidean error if bound is not given. If it is given then returns a boolean on if the error is within the bound."""
    distance = math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2 + (x[2] - y[2])**2)
    if bound is None:
        return distance
    return distance < bound


class a_trip:

    def __init__(self):
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.setpoint_x = 0.0
        self.setpoint_y = 0.0
        self.setpoint_z = 0.0

        # publisher for mavros/setpoint_position/pose
        self.setpoint_position = setpoint.get_pub_position_local(queue_size=1)

        # subscriber for mavros/local_position/pose
        self.sub = rospy.Subscriber(mavros.get_topic('local_position', 'pose'),
                                    setpoint.PoseStamped, self._hasReached, queue_size=1)

	try:
            thread.start_new_thread(self.navigate, ())
        except:
            fault("Error: Unable to start thread")

        # TODO(simon): Clean this up.
        self.done = False
        self.done_evt = threading.Event()

        
    def setTargetPoint(self, x, y, z, delay=0, confirm=True, verbose=True):
        """Goes to a specific x,y,z location"""
        if verbose:
            print 'Going to %.2f, %.2f, %.2f ...' % (x, y, z)
        self.done = False
        self.setpoint_x = x
        self.setpoint_y = y
        self.setpoint_z = z

        if confirm:
            rate = rospy.Rate(2)
            while not self.done and not rospy.is_shutdown():
                rate.sleep()

    def navigate(self):
        """ Continuously publishes position target to the flight controller"""
        rate = rospy.Rate(8)   # in Hz
        rate_mode_check = rospy.Rate(20)

        message_pos = setpoint.PoseStamped(
            header=setpoint.Header(
                frame_id="base_footprint",  # no matter, plugin doesn't use TF
                stamp=rospy.Time.now()),    # stamp should update
        )

        while not rospy.is_shutdown():
            message_pos.pose.position.x = self.setpoint_x
            message_pos.pose.position.y = self.setpoint_y
            message_pos.pose.position.z = self.setpoint_z

            yaw = 0
            quaternion = quaternion_from_euler(0, 0, yaw)
            message_pos.pose.orientation = setpoint.Quaternion(*quaternion)

            self.setpoint_position.publish(message_pos)
            rate.sleep()
    
    def _hasReached(self, topic):
        def is_near(msg, x, y):
            rospy.logdebug("Position %s: local: %d, target: %d, abs diff: %d",
                           msg, x, y, abs(x - y))
            return abs(x - y) < 0.5

        if is_near('X', topic.pose.position.x, self.setpoint_x) and \
           is_near('Y', topic.pose.position.y, self.setpoint_y) and \
           is_near('Z', topic.pose.position.z, self.setpoint_z):
            self.done = True
            self.done_evt.set()

if __name__ == '__main__':
    
    rospy.init_node('setpoint_position_demo')
    mavros.set_namespace() # initialize mavros module with default namespace
    
    rate = rospy.Rate(10)
    
    trip=a_trip()
	
    print "Time to fly!"
    try:
	rospy.loginfo("Taking off")
        trip.setTargetPoint(0,0,10,0)
    except rospy.ROSInterruptException:
        pass

    try:
        trip.setTargetPoint(5,5,10,20)
	rospy.loginfo("waypoint 1")
    except rospy.ROSInterruptException:
        pass


    try:
        trip.setTargetPoint(10,10,10,20)
	rospy.loginfo("waypoint 2")
    except rospy.ROSInterruptException:
        pass
    

    try:
        trip.setTargetPoint(0,0,10,20)
	rospy.loginfo("coming back")
    except rospy.ROSInterruptException:
        pass
    
    try:
        trip.setTargetPoint(0,0,0,20)
    except rospy.ROSInterruptException:
        pass
    
    rospy.loginfo("done")


