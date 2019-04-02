#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import face_recognition
import cv2
import os
from widget import *
class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.face_locations = []
        self.face_encodings = []
        self.known_face_names = []
        self.face_names = []
        self.counter = 0  # 计数
        self.SPEED = 10  # 每5帧图像检测一次
        self.known_face_names, self.known_face_encodings = self.load_image_floder('photos')
        # create a timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.ui.startBtn.clicked.connect(self.controlTimer)
    def viewCam(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        self.process_this_frame = (self.counter % self.SPEED == 0)
        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(small_frame)
            self.face_encodings = face_recognition.face_encodings(small_frame, self.face_locations)
            face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    print(name)
                face_names.append(name)
        self.counter +=1
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(qImg))

    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(2)
           # self.startBtn.setText('stop')  ????
        else:
            self.timer.stop()
            self.cap.release()
               # self.ui.startBtn.setText('start')  ?????

    def load_image_floder(self, path):
        known_face_encodings0 = []
        known_face_names0 = []
        rootDir = path
        lists = os.listdir(rootDir)
        for list in lists:
            print(path + '/' + list)
            image = face_recognition.load_image_file(path + '/' + list)
            faceEncoding = face_recognition.face_encodings(image)[0]
            known_face_encodings0.append(faceEncoding)
            #os.path.splitext(base)[0]
            known_face_names0.append(os.path.splitext(list)[0])

        return known_face_names0,known_face_encodings0



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Mainwindow()
    mainwindow.show()
 
    sys.exit(app.exec_())
