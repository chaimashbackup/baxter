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
    joint_state_topic = ['joint_states:=/robot/joint_states']
    _robot = None
    _group = None
    _left_target_pose = None

    def __init__(self):
        moveit_commander.roscpp_initialize(self.joint_state_topic)
        self._robot = moveit_commander.RobotCommander()
        self._group = moveit_commander.MoveGroupCommander("both_arms")
        rospy.sleep(10)
        print("=====Reference frame: %s" % self._group.get_planning_frame())
        print("=====Reference frame: %s" % self._group.get_end_effector_link())
        print("=====Robot Groups:")
        print(self._robot.get_group_names())
        print("=====Printing robot state")
        print(self._robot.get_current_state())


    def getCurrentPose(self):
        return self._group.get_current_pose(end_effector_link='left_gripper').pose

    def setPose(self, _x = 0.0, _y = 0.0, _z = 0.0):
        lCurrentPose = self.getCurrentPose()
        self._left_target_pose = lCurrentPose
        self._left_target_pose.orientation.w = 1.0
        self._left_target_pose.position.x = (lCurrentPose.position.x + _x)
        self._left_target_pose.position.z = (lCurrentPose.position.z + _z)
        self._left_target_pose.position.z = (lCurrentPose.position.y + _y)
        self._group.set_pose_target(self._left_target_pose, end_effector_link='left_gripper')
        plan = self._group.plan()
        if not plan[1].joint_trajectory.points:
            print("trajectory not found")
        else:
            print(plan[1].joint_trajectory.points)
            self._group.go(wait=True)