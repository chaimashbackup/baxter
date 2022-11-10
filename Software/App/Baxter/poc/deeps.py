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
    @dataclass
    class _coord: 
        """_summary_
        """
        x1:int = None
        x2:int = None
        y1:int = None
        y2:int = None
        def clear(self):
            """_summary_
            """
            self.x1 = None
            self.y1 = None
            self.x2 = None
            self.y2 = None

    _cord = _coord()
    _confidence:float
    def __init__(self) -> None:
        # self._model = torch.hub.load('../../../ThirdParty/yolov5/', 'custom',
        self._model = torch.hub.load('/home/lev/BaxterRobo/yolov5', 'custom',

        path='roboBaxter.onnx', source='local')

    def getCoordinates(self, image:np.ndarray):
        if image is not None:
            result = self._model(image)
            if result.xyxy[0].size()[0] != 0:
                print(result.pandas().xyxy[0])
                self._cord.x1 = int(result.xyxy[0][0][0].item())
                self._cord.y1 = int(result.xyxy[0][0][1].item())
                self._cord.x2 = int(result.xyxy[0][0][2].item())
                self._cord.y2 = int(result.xyxy[0][0][3].item())
                return True, self._cord
        self._cord.clear()
        return False, self._cord
 


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

if __name__ == '__main__':

    img = './camTest.jpg'
    image1 = cv2.imread(img)
    DtD = DtDetection()
    cord = DtD.getCoordinates(image1)
    if cord[0] is True:
        print(cord[1])
        cv2.rectangle(image1, (cord[1].x1, cord[1].y1), (cord[1].x2, cord[1].y2), (0,255,0), 1)
        cv2.imshow("",image1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        # squares = find_squares(image1)
        # cv2.drawContours( image1, squares, -1, (0, 255, 0), 1)
        # cv2.imshow('squares', image1)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()			
    else:
        print("----")