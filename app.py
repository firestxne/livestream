from flask import Flask, render_template, Response
from flask_ngrok import run_with_ngrok
import cv2
try:
    from flask import Flask,render_template,url_for,request,redirect, make_response
    import os
    import random
    import json
    from time import time
    from random import random
    from flask import Flask, render_template, make_response
    from flask_dance.contrib.github import make_github_blueprint, github
except Exception as e:
    print("Some Modules are Missings {}".format(e))

app = Flask(__name__)
run_with_ngrok(app)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.config["SECRET_KEY"]="SECRET KEY"

github_blueprint = make_github_blueprint(client_id='177beaa9b25e9c87ee76',
                                         client_secret='428d7ed3451f8ba1ba5c289921996bbcef550964')

app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/')
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            return render_template('index.html')

    return '<h1>Request failed!</h1>'

camera = cv2.VideoCapture(0)  # use 0 for web camera

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()