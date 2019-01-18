import dlib
import imutils
import cv2
import math
import serial
import struct
import time
import numpy as np

from tkinter import *
from imutils import face_utils
from PIL import Image
from PIL import ImageTk
from serial_helper import *

LEFTEYE_BALL = 0
RIGHTEYE_BALL = 1
LEFTEYE = 2
RIGHTEYE= 3
EYEBROW_LEFT_FIRST = 4
EYEBROW_LEFT_SECOND= 5
EYEBROW_RIGHT_FIRST = 6
EYEBROW_RIGHT_SECOND = 7
MOUTH = 8

thres = 43

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
cap = cv2.VideoCapture(0)

ser = serial.Serial(
    port='/dev/cu.usbmodem14201',
    baudrate=9600,
)

def process(data,result):
    result[LEFTEYE_BALL] = lefteye_ball(result[LEFTEYE_BALL])
    result[RIGHTEYE_BALL] = righteye_ball(result[RIGHTEYE_BALL])
    result[LEFTEYE] = lefteye(result[LEFTEYE])
    result[RIGHTEYE] = righteye(result[RIGHTEYE])
    result[EYEBROW_LEFT_FIRST] = eyebrow_left_first(result[EYEBROW_LEFT_FIRST])
    result[EYEBROW_LEFT_SECOND] = eyebrow_left_second(result[EYEBROW_LEFT_SECOND])
    result[EYEBROW_RIGHT_FIRST] = eyebrow_right_first(result[EYEBROW_RIGHT_FIRST])
    result[EYEBROW_RIGHT_SECOND] = eyebrow_right_second(result[EYEBROW_RIGHT_SECOND])
    result[MOUTH] = mouth(result[MOUTH])

    return result

def send(data, result):
    if ser.isOpen():
        ser.flushInput()  # flush input buffer, discarding all its contents
        ser.flushOutput()  # flush output buffer, aborting current output

        for item in result:
            # write data
            print(item)
            ser.write(struct.pack('B',item))
            time.sleep(2)  # give the serial port sometime to receive the data

def Analyze(data,img,result):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用 detector 检测器来检测图像中的人脸
    faces = detector(gray, 1)
    print("人脸数：", len(faces))
    if(len(faces) >= 1):
        face = faces[0]
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        rett, thresh_gray = cv2.threshold(gray, thres, 255, cv2.THRESH_BINARY)
        thresh_gray, contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_LIST,
                                                                           cv2.CHAIN_APPROX_SIMPLE)
        index = 0
        left_eyeball = (0,0,0)
        right_eyeball = (0,0,0)

        for contour in contours:
            area = cv2.contourArea(contour)
            rect = cv2.boundingRect(contour)
            x, y, width, height = rect
            radius = 0.25 * (width + height)
            lefteye_condition = (x > shape[36][0]) and (y > shape[37][1]) and (x < shape[39][0]) and (y < shape[40][1])
            righteye_condition = (x > shape[42][0]) and (y > shape[43][1]) and (x < shape[45][0]) and (
                        y < shape[46][1])
            if(lefteye_condition):
                print(area)
                if(left_eyeball[2] < area):
                    left_eyeball = (x,y,area)
                #cv2.drawContours(img, contours, index, (0, 255, 0), 1)
            if(righteye_condition):
                print(area)
                if (right_eyeball[2] < area):
                    right_eyeball = (x, y, area)
                #cv2.drawContours(img, contours, index, (0, 255, 0), 1)
            index = index + 1

        cv2.circle(img, (left_eyeball[0],left_eyeball[1]), 1, (0, 255, 255), -1)
        result[RIGHTEYE_BALL] = shape[27][0] - left_eyeball[0]
        cv2.circle(img, (right_eyeball[0],right_eyeball[1]), 1, (0, 255, 255), -1)
        result[LEFTEYE_BALL] = right_eyeball[0] - shape[27][0]

        # loop over the subset of facial landmarks, drawing the
        # specific face part
        # eyes
        for (x, y) in shape[36:48]:
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
        result[RIGHTEYE] = shape[40][1] - shape[38][1]
        result[LEFTEYE] = shape[47][1] - shape[43][1]

        # eyebrow
        for (x, y) in shape[17:27]:
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
        result[EYEBROW_RIGHT_FIRST] = shape[27][1] - shape[19][1]
        result[EYEBROW_RIGHT_SECOND] = shape[27][1] - shape[21][1]
        result[EYEBROW_LEFT_FIRST] = shape[27][1] - shape[22][1]
        result[EYEBROW_LEFT_SECOND] = shape[27][1] - shape[24][1]

        # mouth
        for (x, y) in shape[48:68]:
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
        result[MOUTH] = shape[66][1] -  shape[62][1]
        cv2.ellipse(img, (int(data.width/2), int(data.height/2)), (200, 300), 0, 0, 360, (0,255,255), 2)



####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.result = [0] * 9
    data.Capture_flag = 0
    ret, img = cap.read()
    Analyze(data, img, data.result)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    data.img = img


def mousePressed(event, data):
    # use event.x and event.y
    (cx, cy) = (150, data.height - 28)
    (margin, width, height) = (300, 100, 20)

    # Capture
    if (event.x > cx - width and event.x < cx + width and event.y > cy - height and event.y < cy + height):
        data.Capture_flag = 1

    # Recapture
    if (event.x > cx + margin - width - 15 and event.x < cx + margin + width + 15 and
            event.y > cy - height and event.y < cy + height):
        data.Capture_flag = 0

    # Send
    if (event.x > cx + 2 * margin - width and event.x < cx + 2 * margin + width and
            event.y > cy - height and event.y < cy + height):
        pass
        if(data.Capture_flag):
            print(data.result)
            send_data = data.result.copy()
            send_data = process(data, send_data)
            print(send_data)
            send(data, send_data)

    # QUIT
    if(event.x > cx + 3 * margin - width and event.x < cx + 3 * margin + width and
        event.y > cy - height and event.y < cy + height):
        cap.release()
        sys.exit()

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    if(data.Capture_flag == 0):
        ret, img = cap.read()
        Analyze(data, img, data.result)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        data.img = img

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_image(1220/2, 630/2,image=data.img)
    (cx, cy) = (150, data.height - 28)
    (margin, width, height) = (300, 100, 20)
    canvas.create_rectangle(cx - width, cy - height, cx + width, cy + height, fill="Gray", outline="light Green")
    canvas.create_text(cx, cy,text="CAPTURE", fill="light Green", font="Times 36 bold")
    canvas.create_rectangle(cx+margin - width - 15, cy - height, cx + margin + width + 15, cy + height,
                            fill="Gray", outline="light Green")
    canvas.create_text(cx + margin, cy,text="RECAPTURE", fill="light Green", font="Times 36 bold")
    canvas.create_rectangle(cx + 2*margin - width, cy - height, cx + 2*margin + width, cy + height,
                            fill="Gray", outline="light Green")
    canvas.create_text(cx + 2 * margin, cy, text="SEND", fill="light Green", font="Times 36 bold")
    canvas.create_rectangle(cx + 3*margin - width, cy - height, cx + 3*margin + width, cy + height,
                            fill="Gray", outline="light Green")
    canvas.create_text(cx + 3*margin, cy,text="QUIT", fill="light Green", font="Times 36 bold")

####################################
# use the run function as-is
####################################

def run(width=1220, height=730):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1220, 730)