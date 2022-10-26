# Install Anaconda or Miniforge

First, we need to install anaconda in order to create an environment for the project.
> wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-\$(uname)-\$(uname -m).sh"
bash Mambaforge-\$(uname)-\$(uname -m).sh

if you don't have git on your computer

>sudo apt install git

For activate anaconda in your terminal
>source ~/mambaforge/bin/activate

>cd ~/Document/

>mkdir BaxterRobo

>cd BaxterRobo

Сreate an environment for our project
>conda create -n baxterRobo pip python=3.9

For activate the previously created environment
>conda activate baxterRobo

>pip install --ignore-installed --upgrade tensorflow==2.5.0

After installing tensorflow, check it works 

>python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

If you see this message, it means your processor does not support AVX.
>Illegal instruction (core dumped)
So you need to install tensorflow from source https://www.tensorflow.org/install/source

Next, you need to install tf models:
>git clone https://github.com/tensorflow/models

Check for protobuff with this command:

>pip show protobuf

If protobuf not instaled:

>sudo apt install protobuf-compiler

or https://github.com/protocolbuffers/protobuf/releases



>cd models/research/

>protoc object_detection/protos/*.proto --python_out=.

Install pycocotools

>cd ../../ 
>git clone https://github.com/cocodataset/cocoapi.git
>cd cocoapi/PythonAPI
>make
>cp -r pycocotools ../../models/research/

or use
>pip install pycocotools

Then
>cd models/research/
>cp object_detection/packages/tf2/setup.py .
>python -m pip install --use-feature=2020-resolver .


# Install yolo5

>cd ~/Document/BaxterRobo

>git clone https://github.com/ultralytics/yolov5

>cd yolov5

>pip install -r requirements.txt


# Instal LabelImg

For image annotation we may need LabelImg

>pip install labelImg



source /opt/ros/noetic/setup.bash

catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3


sudo apt-get install ros-noetic-moveit