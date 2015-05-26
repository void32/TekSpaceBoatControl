#!/usr/bin/python
import rospy
import serial
import time
from sensor_msgs.msg import Joy

ser = serial.Serial('/dev/antenna', 56700, timeout=1.0)
rudder = 0
motor = 0
prevRudder = rudder
prevMotor = motor
writeToBoat = True

def callback(data):
    global rudder, motor, prevRudder, prevMotor
    prevRudder = rudder
    prevMotor = motor
    rudder = 10*data.axes[0]
    motor = 50*data.axes[1]
    writeToBoat = abs(motor-prevMotor)>=5 or abs(rudder-prevRudder)>=1 or abs(motor) <= 0.01 or abs(rudder) < 0.01

def writeToBoat(te):
    #print "writeToBoat"
    if writeToBoat:
        print "set speed "+str(motor)
        #ser.write('mot: ' + str(motor) + '\r\n') # set speed
    
        print "set rudder "+str(rudder)
        ser.write('rud: ' + str(rudder) + '\r\n') # set rudder              

def readFromBoat(te):
    #print "ReadFromBoat"
    msg = ser.readline() # To text file..
    print msg

if __name__ == '__main__':
    rospy.init_node('serial2boat')
    rospy.Timer(rospy.Duration(0.1),writeToBoat)
    rospy.Timer(rospy.Duration(0.1),readFromBoat)
    rospy.Subscriber("joy", Joy, callback)
    rospy.spin()
    ser.write('mot: ' + str(0.0) + '\r\n') # set speed
    ser.write('rud: ' + str(-10.0) + '\r\n') # set rudder              
    ser.close()


