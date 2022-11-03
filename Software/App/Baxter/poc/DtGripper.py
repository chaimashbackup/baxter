import sys
import enum
import rospy
import actionlib
import baxter_interface

from control_msgs.msg import (
    GripperCommandAction,
    GripperCommandGoal,
)

class DtGripper():
    """_summary_

    Returns:
        _type_: _description_
    """
    class gripperName(enum.Enum):
        left = 0
        right = 1
    leftGripper = 'robot/end_effector/left_gripper/gripper_action'
    rightGripper = 'robot/end_effector/right_gripper/gripper_action'
    _clientGripperLeft = None
    _clientGripperRight = None
    _leftGoal = None
    _rightGoal = None

    def __init__(self) -> None:
        for i in self.gripperName:
            if i == self.gripperName.left:
                self._clientGripperLeft = actionlib.SimpleActionClient(self.leftGripper, GripperCommandAction)
                self._leftGoal = GripperCommandGoal()
            elif i == self.gripperName.right:
                self._clientGripperLeft = actionlib.SimpleActionClient(self.rightGripper, GripperCommandAction)
                self._rightGoal = GripperCommandGoal()

    
    def command(self, name:gripperName, position, effort):
        """_summary_

        Args:
            name (gripperName): _description_
            position (_type_): _description_
            effort (_type_): _description_
        """
        if name == self.gripperName.left:
            self._leftGoal.command.position = position
            self._leftGoal.command.max_effort = effort
            self._clientGripperLeft.send_goal(self._leftGoal)
        elif name == self.gripperName.right:
            self._rightGoal.command.position = position
            self._rightGoal.command.max_effort = effort
            self._clientGripperRight.send_goal(self._rightGoal)

    def stop(self, name:gripperName):
        """_summary_

        Args:
            name (gripperName): _description_
        """
        if name == self.gripperName.left:
            self._clientGripperLeft.cancel_goal()
        elif name == self.gripperName.right:
            self._clientGripperRight.cancel_goal()

    def wait(self, name:gripperName, timeout = 5.0):
        """_summary_

        Args:
            name (gripperName): _description_
            timeout (float, optional): _description_. Defaults to 5.0.

        Returns:
            _type_: _description_
        """
        if name == self.gripperName.left:
            self._clientGripperLeft.wait_for_result(timeout=rospy.Duration(timeout))
            return self._clientGripperLeft.get_result()
        elif name == self.gripperName.right:
            self._clientGripperRight.wait_for_result(timeout=rospy.Duration(timeout))
            return self._clientGripperRight.get_result()

    def clear(self, name:gripperName):
        """_summary_

        Args:
            name (gripperName): _description_
        """
        if name == self.gripperName.left:
           self._leftGoal = GripperCommandGoal()
        elif name == self.gripperName.right:
            self._rightGoal = GripperCommandGoal()

