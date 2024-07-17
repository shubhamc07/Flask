from flask import Flask,jsonify,request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/file',methods=["POST"])
def file_validation():
    file = request.files['file']
    filename= secure_filename(file.filename)
    file_size= len(file.read())
    file_path = 'static/'+filename

    if file:
        if file_size > 200000:
            return jsonify({"error":"select file less than 2 mb"})
        else:
            return jsonify({"sucess":filename,"file_path":file_path})
    else:
        return jsonify({"error":"select file"})



if __name__ == '__main__':
    app.run(debug=True)