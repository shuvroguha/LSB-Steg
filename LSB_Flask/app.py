import LSB_Steg
import os
from flask import Flask, render_template, request, url_for, flash, redirect, send_file
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
UPLOAD_FOLDER = '/tmp/'

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        print 'post'
        if ('begin' in request.form):
            print 'if1'
            encoded = LSB_Steg.steg_in('/tmp/cover', '/tmp/message')
            print 'lsb ran'
            return send_file('/tmp/final.png')
        # check if the post request has the file part
        if ('cover' not in request.files) and ('message' not in request.files):
            print 'if2'
            flash('No file part')
            return redirect(request.url)
        if('cover' in request.files):
            print 'if3'
            file = request.files['cover']
            image_type = 'cover'
        else:
            print 'if4'
            file = request.files['message']
            image_type = 'message'
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print 'if5'
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print 'if6'
            filename = 'cover' if (image_type == 'cover') else 'message'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)

    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        print 'post'
        if ('begin' in request.form):
            print 'if1'
            encoded = LSB_Steg.steg_out('/tmp/decode_cover')
            print 'lsb ran'
            return send_file('/tmp/hidden_message.png')
        # check if the post request has the file part
        if ('cover' not in request.files):
            print 'if2'
            flash('No file part')
            return redirect(request.url)
        if('cover' in request.files):
            print 'if3'
            file = request.files['cover']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print 'if5'
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print 'if6'
            filename = 'decode_cover'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    return render_template('decode.html')


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug=True)
