import cv2
import gl

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        

    def __del__(self):
        self.video.release()        

    def get_frame(self,face_cascade):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV
        try :
            print("loop")
            height, width, channels = frame.shape
            print(height)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            print(gray)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print(faces)
            # Loop through all the faces detected 
            identities = []
            for (x, y, w, h) in faces:
                x1 = x
                y1 = y
                x2 = x+w
                y2 = y+h

                gl.message="message"
                print("Message updated")
                face_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]
                print("Face image obtained")
                
            frame = face_image
            ret1,jpeg1=cv2.imencode('.jpg',frame)
            gl.img=jpeg1.tobytes()
        except Exception as e:
            print(e)
            frame=frame

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
