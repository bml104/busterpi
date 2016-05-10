from flask import Flask, render_template, Response
from camera_pi import Camera
import subprocess
import os
import datetime
import time


app = Flask(__name__)

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('index.html', **templateData)

@app.route("/l1/")
def l1():
   subprocess.call(['./l1.py'], shell=True)
   return render_template('index.html')	
@app.route("/r1/")
def r1():
   subprocess.call(['./r1.py'], shell=True)
   return render_template('index.html')

@app.route("/d1/")
def d1():
   subprocess.call(['./d1.py'], shell=True)
   return render_template('index.html')

@app.route("/u1/")
def u1():
   subprocess.call(['./u1.py'], shell=True)
   return render_template('index.html')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')








if __name__ == "__main__":
   app.run(host='0.0.0.0', threaded='true')
