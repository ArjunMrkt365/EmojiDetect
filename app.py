# -*- coding: utf-8 -*-
import os
import time
import hashlib
import cv2
from flask import Flask, render_template, redirect, url_for, request, Response
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import camera
from camera import VideoCamera
import base64
video_stream = VideoCamera()

basedir = os.path.abspath(os.path.dirname(__file__))
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB



def gen(camera):
    while True:
        frame = camera.get_frame(face_cascade)        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Upload')


@app.route('/video_feed/',methods=['get','post'])
def video_feed():
    try:
      if(request.json['val']==1):
        print("No way")
    except:
      pass    
    return Response(gen(video_stream),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    img1=""
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):
            name = hashlib.md5(('admin' + str(time.time())).encode('utf-8')).hexdigest()[:15]
            photos.save(filename, name=name + '.')
        print(filename,name)
        success = True
	
	//path="uploads/"+name+".png"
        //call function here
        // predict
        // success=output(String)
        with open("uploads/"+name+".png", "rb") as imageFile:
            img1=base64.b64encode(imageFile.read()).decode("utf-8")
    else:
        success = False
    return render_template('index.html', form=form, success={"success":success,"image":img1})




@app.route('/manage')
def manage_file():
    files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('manage.html', files_list=files_list)


@app.route('/open/<filename>')
def open_file(filename):
    file_url = photos.url(filename)
    return render_template('browser.html', file_url=file_url)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = photos.path(filename)
    os.remove(file_path)
    return redirect(url_for('manage_file'))


if __name__ == '__main__':
    app.run(debug=True)



'''from flask import Flask, render_template, Response, jsonify
##from camera import VideoCamera
##import cv2
##import gl
#from waitress import serve


##face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

app = Flask(__name__)

##video_stream = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text',methods=['get'])
def indexNew1():
    print(12345)
    return jsonify({"text":"text123"})

##@app.route('/new')
##def indexNew():
##    return render_template('new.html',context={"message":gl.message,"image":gl.img})

##def gen(camera):
##    while True:
##        frame = camera.get_frame(face_cascade)        
##        yield (b'--frame\r\n'
##               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

##@app.route('/video_feed/',methods=['get'])
##def video_feed():
##    
##    return [Response(gen(video_stream),mimetype='multipart/x-mixed-replace; boundary=frame')]

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="5000")
'''