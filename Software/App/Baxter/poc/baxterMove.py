import sys
import copy
import rospy
import moveit_commander
import geometry_msgs.msg
import baxter_interface
from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest)
from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.msg import RobotTrajectory, Grasp, PlaceLocation, Constraints
from sensor_msgs.msg import JointState

class baxterMove():
    # print("start moveTest")
    ns = "ExternalTools/left/PositionKinematicsNode/IKService"
    joint_state_topic = ['joint_states:=/robot/joint_states']
    # robot = None
    # group = None
    # scene = None
    # left_target_pose = None
    # moveService = None
    # ikReq = None
    # left_current_pose = None

    def __init__(self):
        moveit_commander.roscpp_initialize(self.joint_state_topic)
        self.robot = moveit_commander.RobotCommander()
        self.group = moveit_commander.MoveGroupCommander("both_arms")
        # self.scene = moveit_commander.PlanningSceneInterface()
        # self.group.set_planning_time(10)
        
        # self.group.set_max_velocity_scaling_factor(0.5)
        # self.group.set_goal_orientation_tolerance(0.005)
        # self.group.clear_trajectory_constraints()
        # self.moveService = rospy.Service(self.ns, SolvePositionIK)
        # self.ikReq = SolvePositionIKRequest()
        # self.ikReq.pose_stamp()


    def getCurrentPose(self):
        return self.group.get_current_pose(end_effector_link='left_gripper').pose
    
    def setPose(self, _x = 0.0, _y = 0.0, _z = 0.0):
        lCurrentPose = self.getCurrentPose()
        # print(lCurrentPose)
        self.left_target_pose = lCurrentPose
        self.left_target_pose.position.x = (lCurrentPose.position.x + _x) 
        self.left_target_pose.position.z = (lCurrentPose.position.z + _z)
        self.left_target_pose.position.z = (lCurrentPose.position.y + _y)
        self.group.set_pose_target(self.left_target_pose, end_effector_link='left_gripper')
        plan = self.group.plan()
        if not plan[1].joint_trajectory.points:
            print("trajectory not found")
        else:
            print(plan[1].joint_trajectory.points)
            self.group.go(wait=True)  

