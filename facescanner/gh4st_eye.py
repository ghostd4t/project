
class Camera:
    def __init__(self):
        self.data = None
        self.cam = cv2.VideoCapture(0)

        WIDTH = 1600
        HEIGHT = 1600
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        cascPath = os.path.join(dirname, "haarcascade_frontalface_default.xml")
        self = cv2.CascadeClassifier(cascPath)
        center_x = WIDTH / 2
        center_y = HEIGHT / 2
        self.touched_zoom = False

        self.image_queue = Queue()
        self.video_queue = Queue()

        self.scale = 1
        self.__setup()

        self.recording = False

    def __setup(self):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        time.sleep(2)

    def get_location(self, x, y):
        self.center_x = x
        self.center_y = y
        self.touched_zoom = True

    def stream(self):
        # streaming thread 함수
        def streaming():
            # 실제 thread 되는 함수
            self.ret = True
            while self.ret:
                self.ret, np_image = self.cam.read()
                if np_image is None:
                    continue
                self.data = np_image
                k = cv2.waitKey(1)
                if k == ord('q'):
                    self.release()
                    break
        Thread(target=streaming).start()

    def save_picture(self):
        # 이미지 저장하는 함수
        ret, img = self.cam.read()
        if ret:
            now = datetime.datetime.now()
            date = now.strftime('%Y%m%d')
            hour = now.strftime('%H%M%S')
            user_id = '00001'
            filename = './images/cvui_{}_{}_{}.png'.format(date, hour, user_id)
            cv2.imwrite(filename, img)
            self.image_queue.put_nowait(filename)

    def show(self):
        while True:
            frame = self.data
            if frame is not None:
                self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(self.gray, scaleFactor=1.1, minNeighbors=30, minSize=(50, 50))
                for (x, y, w, h) in faces:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0, 0), 2)
                cv2.imshow('SMS', frame)
                cv2.setMouseCallback('face detection', self.mouse_callback)
            key = cv2.waitKey(1)
            if key == ord('q'):
                # q : close
                self.release()
                cv2.destroyAllWindows()
                break
            elif key == ord('p'):
                # p : take picture and save image (image folder)
                self.save_picture()

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.get_location(x, y)
            self.zoom_in()
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.zoom_out()


if __name__ == '__main__':
    cam = Camera()
    cam.stream()
    cam.show()