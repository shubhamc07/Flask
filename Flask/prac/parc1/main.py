import os
from flask import Flask,jsonify,request,send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

upload='\Users\Himanshu\Desktop\Flask\prac\parc1\static'
extitions =['txt','pdf']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in extitions

app.config['upload']=upload

@app.route('/img',methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error':'file not slected'}),400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'no file selected'}),400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['upload'],filename))
    return jsonify({'msg':'file uploaded succesfully'})


if __name__==('__main__'):
    app.run(debug=True)





