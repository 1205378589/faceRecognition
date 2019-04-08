import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import face_recognition
import cv2
import os
from new import *
# import qdarkstyle


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
        self.SPEED = 3  # 每5帧图像检测一次
        self.tolerance = 0.40
        self.known_face_names, self.known_face_encodings = self.load_image_floder('photos')
        self.name = ''

        #  self.ui.shotBtn.clicked(self.shotImage)
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
            # face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding,
                                                         tolerance=self.tolerance)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                print(name)
                if not name == 'Unknown' and name not in self.name.split():
                    self.name += name + '\n'
                self.showname()
                self.face_names.append(name)

       # image = cv2.resize(image, (780, 600))
        self.counter += 1
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.ui.videolabel.setPixmap(QPixmap.fromImage(qImg))
        self.ui.videolabel.setScaledContents(True) # 让qImage自动适应label大小

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
            # os.path.splitext(base)[0]
            known_face_names0.append(os.path.splitext(list)[0])

        return known_face_names0, known_face_encodings0

    def showname(self):
        self.ui.recoFaceLabel.setText(self.name)

    # def draw(self, face_locations, image):
    #     pil_image = Image.fromarray(image)
    #     draw = ImageDraw.Draw(pil_image)
    #     for (top, right, bottom, left) in face_locations:
    #         top *= 4
    #         right *= 4
    #         left *= 4
    #         bottom *= 4
    #         draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    #     ndImage = numpy.array(pil_image)
    #     return ndImage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Mainwindow()
    qssStyle = '''
                QPushButton{
                    background-color : blue
                }
                QLabel{
                    background-color :
                }
                
                '''

   # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
   #  mainwindow.setStyleSheet(qssStyle)
    mainwindow.show()
    sys.exit(app.exec_())
