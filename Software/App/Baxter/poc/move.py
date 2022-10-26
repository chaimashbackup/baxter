import sys
import copy
import rospy
import moveit_commander
import geometry_msgs.msg
import baxter_interface
from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.msg import RobotTrajectory, Grasp, PlaceLocation, Constraints
from sensor_msgs.msg import JointState


def moveTest():
    print("start moveTest")
    joint_state_topic = ['joint_states:=/robot/joint_states']
    moveit_commander.roscpp_initialize(joint_state_topic)
    rospy.init_node('moveit_baxter_example', anonymous=True)

    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("both_arms")

    left_current_pose = group.get_current_pose(end_effector_link='left_gripper').pose

    left_target_pose = left_current_pose
    left_target_pose.position.x = left_current_pose.position.x - 0.5  
    left_target_pose.position.z = left_current_pose.position.z - 0.3
    left_target_pose.position.z = left_current_pose.position.y + 0.2

    group.set_pose_target(left_target_pose, end_effector_link='left_gripper')

    plan = group.plan()

    if not plan.joint_trajectory.points:
        print("trajectory not found")
    else:
        group.go(wait=True)

    moveit_commander.roscpp_shutdown()
    moveit_commander.os._exit(0)


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass