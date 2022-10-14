import cv2
import imutils
import numpy as np

def get_perspective(img, location, height = 900, width = 900):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result


image  = cv2.imread("../dataset/grid0.jpg")
cv2.imshow("Image", image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
edged = cv2.Canny(bfilter, 30, 180)
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE,
cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
newimg = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)
cv2.imshow("Contour", newimg)

cv2.waitKey(0)
cv2.destroyAllWindows()