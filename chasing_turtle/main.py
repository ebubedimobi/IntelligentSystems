#!/usr/bin/python3

import rospy
from turtlesim.msg import *
from turtlesim.srv import *
from geometry_msgs.msg import Twist
from std_srvs.srv import *
import random
from math import atan2,pi, sqrt, pow, cos
import sys


# global variables
# victim position
victimX = 0.0
victimY = 0.0
victimTheta = 0.0

# turtle position
turtleX = 0.0
turtleY = 0.0
turtleTheta = 0.0

def configureVictimPosition(data):
    global turtleX, turtleY, turtleTheta
    victimX = data.x
    victimY = data.y
    victimTheta = data.theta

def configureTurtlePosition(data):
    global turtleX, turtleY, turtleTheta
    turtleX = data.x
    turtleY = data.y
    turtleTheta = data.theta

def getEstimatedDistance(turtlePoseX, turtlePoseY, victimPoseX, victimPoseY):
    return sqrt(pow((victimPoseX - turtlePoseX), 2) + pow((victimPoseY - turtlePoseY), 2))

def runToTurtle(pub):
    global turtleX, turtleY, turtleTheta

    msg = Twist()

    while not rospy.is_shutdown():
        steeringAngle = atan2(victimY - turtleY, victimX - turtleX) - turtleTheta
        msg.angular.z = 6.0 * steeringAngle

        distance = getEstimatedDistance(turtleX, turtleY, victimX, victimY)
        msg.linear.x = 1.5 * distance * cos(steeringAngle)


        pub.publish(msg)


        if (distance <= 0.02):
            break


rospy.init_node('commander_on_chasing_turtle')

# create a publisher object
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)

# subscribe to turtles pose
rospy.Subscriber("/turtle1/pose", Pose, configureTurtlePosition)
rospy.Subscriber("/victim/pose", Pose, configureVictimPosition)

# get clear function
service = '/clear'
rospy.wait_for_service(service)
clear = rospy.ServiceProxy(service, Empty)
clear()

# get kill function
service = '/kill'
rospy.wait_for_service(service)
killTurtleService = rospy.ServiceProxy(service, Kill)
try:
    killTurtleService("victim")
except:
    pass

# get spawn function
service = '/spawn'
rospy.wait_for_service(service)
spawnTurtleService = rospy.ServiceProxy(service, Spawn)
# spawn turtle at random position
[victimX, victimY] = random.sample(range(2, 9), 2)
try:
    spawnTurtleService(victimX,
                       victimY,
                        0,
                       "victim")
except:
    pass


configureTurtlePosition(Pose())
runToTurtle(pub)
