ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys, random
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

"""
Description: the rotate base function works by making a linear
mapping between the values on the right potentiometer and angle 
at which the base is turned. It uses a scale factor of 350 to convert
between these two parameters.
"""

def rotate_base(color):
    time.sleep(1)
#temp stores the current value of the potentiometer.
    temp = potentiometer.right()
#total keeps track of the degrees rotated by the base.
    total = 0
#the base keeps turning until it is properly alligned.
    
    while(arm.check_autoclave(color)== False):
        if(arm.check_autoclave(color) == True):
            print("yay!")#confirms whether arm is in correct location
            break
        x = (potentiometer.right() - temp)*350
        arm.rotate_base(x-total)
        time.sleep(1)
        total += (x-total)

#for each increment of the right potentiometer,
#the variable x will store number of degrees rotated from the origin.
#Thus, the base must rotate (x-total) degrees as we only want to see
#the difference.

"""
Description: the drop off function works through case work. It first determines
the color of the container and based on the value of the left potentiometer, it will
either place it in the top or bottom container, depending on whether it is large or
small.
"""

def drop_off(color):
    if(color == 'red'):
        
#the left potentiometer value will be in this range if the container is small.
        if(potentiometer.left() >= 0.6 and potentiometer.left() < 1.0):
        #moves arm to top autoclave
            arm.activate_autoclaves()
            arm.move_arm(-0.605, 0.22, 0.274)
        #opens gripper
            arm.control_gripper(-30)
            time.sleep(2)
            arm.deactivate_autoclaves()
            
#the left potentiometer value will be in the range if the container is large.
        if(potentiometer.left() == 1.0):
            time.sleep(1)
            arm.activate_autoclaves()
            time.sleep(1)
            arm.open_autoclave('red')#open drawer
            time.sleep(1)
            arm.move_arm(-0.437, 0.159, 0.148)#moves to autoclave drawer
            time.sleep(1)
            arm.control_gripper(-30)
            time.sleep(1)
            arm.open_autoclave('red',False)#close drawer
            time.sleep(2)
            arm.deactivate_autoclaves()

            
    if(color == 'blue'):
        
#the left potentiometer value will be in this range if the container is small.
        if(potentiometer.left() >= 0.6 and potentiometer.left() < 1.0):
            time.sleep(1)
            arm.activate_autoclaves()
        #move to top autoclave
            arm.move_arm(0.0, 0.636, 0.28)
            time.sleep(1)
        #opens gripper
            arm.control_gripper(-30)
            time.sleep(2)
            arm.deactivate_autoclaves()
            
#the left potentiometer value will be in the range if the container is large.
        elif (potentiometer.left() == 1.0):
            time.sleep(1)
            arm.activate_autoclaves()
            time.sleep(1)
            arm.open_autoclave('blue')#open drawer
            time.sleep(1)
            arm.move_arm(0.0, 0.416, 0.163)#moves to autoclave drawer
            time.sleep(1)
            arm.control_gripper(-30)
        #opens gripper
            time.sleep(1)
            arm.open_autoclave('blue',False)#close drawer
            time.sleep(2)
            arm.deactivate_autoclaves()

    if(color == 'green'):
        
#the left potentiometer value will be in this range if the container is small.
        if(potentiometer.left() >= 0.6 and potentiometer.left() < 1.0):
            time.sleep(1)
            arm.activate_autoclaves()
        #move to top autoclave
            arm.move_arm(0.0, -0.655, 0.269)
            time.sleep(1)
        #opens gripper
            arm.control_gripper(-30)
            time.sleep(2)
            arm.deactivate_autoclaves()
            
#the left potentiometer value will be in the range if the container is large.
        elif(potentiometer.left() == 1.0):
            time.sleep(1)
            arm.activate_autoclaves()
            time.sleep(1)
            arm.open_autoclave('green')#open drawer
            time.sleep(1)
            arm.move_arm(0.023, -0.438, 0.145)#moves to autoclave drawer
            time.sleep(1)
            arm.control_gripper(-30)
        #opens gripper
            time.sleep(1)
            arm.open_autoclave('green',False)#close drawer
            time.sleep(2)
            arm.deactivate_autoclaves()
            
"""
Description: the pick_up function moves the arm to the pick up location,
closes the gripper and returns to the home position.
"""
def pick_up():
    #moves arm to pick location autoclave
    arm.move_arm(0.595, 0.052, 0.028)
    time.sleep(1)
    arm.control_gripper(40)    
    time.sleep(1)
    #returns arm to home
    arm.move_arm(0.406, 0.0, 0.483)

def main():
    
#the list ids holds the ids of all containers that have not been spawned
#at each iteration of the loop, a random value is chosen from the
#list and it is then removed from it in order to spawn all containers.
    container_count = 0
    ids = [1,2,3,4,5,6]
    
    while(container_count < 6):
        container = random.choice(ids)#randomly selects container id
        ids.remove(container)
        print(ids)
        arm.spawn_cage(container)
        time.sleep(1)

#defining color based on container id
        if(container == 1 or container == 4):
            color = 'red'
        elif(container == 2 or container == 5):
            color = 'green'
        else:
            color = 'blue'

#picking it up
    
        pick_up()
        time.sleep(1)
    
#rotating base
        while(arm.check_autoclave(color)== False):
            print("rotate base")
            rotate_base(color)
            time.sleep(2)

#drop_off
        if(container == 1 or container == 2 or container == 3):
            while(potentiometer.left() < 0.6 or potentiometer.left() == 1.0):
                print("adjust left potentiometer")
#moves arm to correct drop off location based on left potentiometer input
                time.sleep(2)

        if(container == 4 or container == 5 or container == 6):
            while(potentiometer.left() != 1.0):
                print("adjust left potentiometer")
                time.sleep(2)

        drop_off(color)

        
        container_count += 1
        time.sleep(2)
        arm.home()

        while(potentiometer.left() != 0.5 or potentiometer.right() != 0.5):
            print("Set potentiometers to 50%")#directs user to reset potentiometer
            time.sleep(2)
    

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

