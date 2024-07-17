import os
from flask import Flask,jsonify,request,send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/Himanshu/Desktop/Flask/16-04-2024/task2/static'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload',methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error':'file not provided'}),400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'no file selected'}),400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return jsonify({'msg':'file uploaded succesfully'})

@app.route('/load_img/<img_name>')
def load_img(img_name):
    return send_from_directory('static',img_name)



if __name__ == ('__main__'):
    app.run(debug=True)