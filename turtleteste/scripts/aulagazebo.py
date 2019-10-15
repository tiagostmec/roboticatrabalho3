#!/usr/bin/env python

import rospy
#from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import numpy as np



#Laser_msg = None
#anglemin = None
#anglemax = None
#ranges = None
#angles = None
xr=None
yr=None
thr=None

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass
 
       
#def callback_laser(msg): 
 #   global Laser_msg
 #   global ranges
 #   Laser_msg=msg
 #   ranges = Laser_msg.ranges
    

def callback_odom(msg): 
    global xr
    global yr
    global thr
    xr=float(msg.x)
    yr=float(msg.y)
    thr = float(msg.theta)

    
def talker():
         
    ###### SETUPPP #########
    pub_vel = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 1)
    rospy.init_node('aulagazebo', anonymous=False)
    #rospy.Subscriber('/scan', LaserScan, callback_laser) 
    rospy.Subscriber('/turtle1/pose', Pose,callback_odom)  
    rate = rospy.Rate(10) # 10hz
    
    # Velocity Message    
    twist = Twist()
    twist.linear.x = 0 
    twist.linear.y = 0 
    twist.linear.z = 0
    twist.angular.x = 0 
    twist.angular.y = 0 
    twist.angular.z = 0
    rospy.sleep(2) 
    
    
   # # Rangefinder Angles
    #min_angle=Laser_msg.angle_min
   # max_angle=Laser_msg.angle_max
    #increment=Laser_msg.angle_increment
    #n_angles=int(round((max_angle-min_angle)/increment)+1)
    #angles=min_angle+np.array(range(n_angles))*(max_angle-min_angle)/(n_angles-1)
    


    
    ######## LOOOP  ########
    while not rospy.is_shutdown(): 

        # Goal
        xg = 7
        yg=  7
        thg = 2

        # Gains
        kp=0.2
        ka=0.4
        kb=-0.2

        erro = abs(float(xg)-xr)+abs(float(yg)-yr)+(float(thg)-thr)
        

        if erro > 0.3:
            # Controle
            dx = xg-xr
            dy = yg-yr
            rho = np.sqrt(dx**2+dy**2)
            gama = np.arctan2(dy,dx)
            alpha = gama-thr
            beta = thg - gama
            v=0
            w=0
            v=kp*rho
            w=ka*alpha + kb*beta

        else:
            v=0
            w=0



        twist.linear.x = v
        twist.angular.z = w
        pub_vel.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
