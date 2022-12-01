#!/usr/bin/python3

import sys
import cv2
import torch
import numpy as np 
import onnx
import onnxruntime as rt
from dataclasses import dataclass
import imutils


class DtDetection(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    x1:int = None
    x2:int = None
    y1:int = None
    y2:int = None
    _confidence:float
    def __init__(self, modelLocation:str, workDirectory:str) -> None:
        if modelLocation == "" or workDirectory == "":
            print("path empty")
            sys.exit(0)
        self._model = torch.hub.load(workDirectory, 'custom', path=modelLocation, source='local')

    def getCoordinates(self, image:np.ndarray):
        if image is not None:
            result = self._model(image)
            if result.xyxy[0].size()[0] != 0:
                print(result.pandas().xyxy[0])
                self.x1 = int(result.xyxy[0][0][0].item())
                self.y1 = int(result.xyxy[0][0][1].item())
                self.x2 = int(result.xyxy[0][0][2].item())
                self.y2 = int(result.xyxy[0][0][3].item())
                return True, self.x1, self.x2, self.y1, self.y2
        return False, self.x1, self.x2, self.y1, self.y2