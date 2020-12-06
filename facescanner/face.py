import cv2
import time
import os
import datetime
from threading import Thread
from queue import Queue
import sys
import numpy
import face_recognition



def thread_stream():
    def face_detection():
        image_queue = Queue()
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        cascPath = os.path.join(dirname, "haarcascade_frontalface_default.xml")
        faceCascade = cv2.CascadeClassifier(cascPath)

        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=40, minSize=(50, 50))
            try:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0, 0), 2)
                    rectangle = True
            except Exception:
                continue
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('s'):
                if ret:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0, 0), 2)
                        rectangle = True
                    crop_frame = frame[y:y + h, x:x + w]
                    now = datetime.datetime.now()
                    date = now.strftime('%Y%m%d')
                    hour = now.strftime('%H%M%S')
                    user_id = '00001'
                    filename = './known_faces/cvui_{}_{}_{}.png'.format(date, hour, user_id)
                    cv2.imwrite(filename, crop_frame)
                    image_queue.put_nowait(filename)
                    print('face_saved')
        video_capture.release()
        cv2.destroyAllWindows()
    Thread(target=face_detection()).start()
thread_stream()
