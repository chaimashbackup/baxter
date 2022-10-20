import rospy
import sys
import image_geometry

from geometry_msgs.msg import Point, Pose
from std_msgs.msg import Bool
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo
from baxter_core_msgs.msg import EndpointState


camInfData = None
camStateInf = None




def camInf(data):
	global camInfData
	camInfData = data	
	#rospy.loginfo(data)

def camState(data):
	global camStateInf
	camStateInf = data
	
	camX = data.pose.position.x
	camY = data.pose.position.y
	camZ = data.pose.position.z
	
	rospy.loginfo("h = %s", camZ)
	
	
	
		
	
def geometry():
	cam = image_geometry.PinholeCameraModel()
	cam.fromCameraInfo(camInfData)
	

if __name__ == '__main__':
	rospy.init_node('geometryTest', anonymous=True) 
	left_w0 = rospy.get_param('left_w0',default = 0)
	left_w1 = rospy.get_param('left_w1',default = 0)
	left_w2 = rospy.get_param('left_w2',default = 0)
	left_e0 = rospy.get_param('left_e0',default = 0)
	left_e1 = rospy.get_param('left_e1',default = 0)
	left_s0 = rospy.get_param('left_s0',default = 0)
	left_s1 = rospy.get_param('left_s1',default = 0)
	print(left_e1)
	
	#rospy.Subscriber('/cameras/left_hand_camera/camera_info', CameraInfo, camInf)
	rospy.Subscriber('/robot/limb/left/endpoint_state', EndpointState, camState)
	rospy.spin()

