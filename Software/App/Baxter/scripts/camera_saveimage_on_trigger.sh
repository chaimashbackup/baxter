#!/bin/bash

# rosrun image_view image_saver image:=/cameras/left_hand_camera/image _save_all_image:=false __name:=image_saver
rosrun image_view image_saver image:=/cameras/left_hand_camera/image _save_all_image:=false _filename_format:=left_image.jpg __name:=image_saver_left &
rosrun image_view image_saver image:=/cameras/right_hand_camera/image _save_all_image:=false _filename_format:=right_image.jpg __name:=image_saver_right &

# To trigger a save call: rosservice call /image_saver_left/save or rosservice call /image_saver_right/save
