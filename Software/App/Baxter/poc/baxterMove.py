import sys
import copy
import rospy
import moveit_commander
import geometry_msgs.msg
import baxter_interface
from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.msg import RobotTrajectory, Grasp, PlaceLocation, Constraints
from sensor_msgs.msg import JointState

class baxterMove():
    # print("start moveTest")
    joint_state_topic = ['joint_states:=/robot/joint_states']
    robot = None
    group = None
    left_target_pose = None
    # left_current_pose = None

    def __init__(self):
        print("init baxterMove")
        moveit_commander.roscpp_initialize(self.joint_state_topic)
        # rospy.init_node('moveit_baxter_example', anonymous=True)
        self.robot = moveit_commander.RobotCommander()
        self.group = moveit_commander.MoveGroupCommander("left_arm")

    def getCurrentPose(self):
        return self.group.get_current_pose(end_effector_link='left_gripper').pose
    
    def setPose(self, x = 0.0, y = 0.0, z = 0.0):
        lCurrentPose = self.getCurrentPose()
        self.left_target_pose = lCurrentPose
        self.left_target_pose.position.x = lCurrentPose.position.x + x 
        self.left_target_pose.position.z = lCurrentPose.position.z + z
        self.left_target_pose.position.z = lCurrentPose.position.y + y
        self.group.set_pose_target(lCurrentPose, end_effector_link='left_gripper')
        plan = self.group.plan()
        if not plan[1].joint_trajectory.points:
            print("trajectory not found")
        else:
            print(plan[1].joint_trajectory.points)
            self.group.go(wait=True)  

