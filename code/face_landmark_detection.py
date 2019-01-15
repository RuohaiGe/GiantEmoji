import dlib
import numpy as np
import imutils
from imutils import face_utils
import cv2

# 使用 Dlib 的正面人脸检测器 frontal_face_detector
detector = dlib.get_frontal_face_detector()

# Dlib 的 68点模型
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#打开摄像头获取视频
cap = cv2.VideoCapture(0)

# 编译并输出保存视频
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while (True):
    # 获取视频及返回状态
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用 detector 检测器来检测图像中的人脸
    faces = detector(gray, 1)
    print("人脸数：", len(faces))

    # loop over the face detections
    for (i, face) in enumerate(faces):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        # print(shape)
        # print(len(shape))

        # loop over the subset of facial landmarks, drawing the
        # specific face part
        for (x, y) in shape:
            cv2.circle(img, (x, y), 8, (0, 0, 255), -1)

    # 显示原图像
    cv2.imshow('img', img)
    # 按q键退出while循环
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 释放摄像头
cap.release()
# 关闭视频输出
out.release()
# 关闭所有窗口
cv2.destroyAllWindows()