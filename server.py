from flask import Flask, render_template, redirect, request, url_for, send_file
from flask import jsonify, json
from werkzeug.utils import secure_filename
import prediction
import os


app = Flask("__main__", template_folder="templates")
Uploaded_images = "Uploaded_images"
app.config['Uploaded_images'] = Uploaded_images

save_path = 'Uploaded_images/'
if not os.path.exists(save_path):
    os.makedirs(save_path)

@app.route('/', methods=['POST', 'GET'])
def homepage():
  if request.method == 'GET':
    return render_template('index.html')

@app.route('/getFile', methods=['POST'])
def getOutput():
  output=""
  if request.method == 'POST':
        myimage = request.files.get('myfile')
        imgname = secure_filename(myimage.filename)
        imgpath = save_path + imgname
        myimage.save(os.path.join(app.config["Uploaded_images"], imgname))
        output = prediction.prediction(imgpath)
        return jsonify({"result": {'message': 'okay', 'imgpath': imgpath, 'prediction' : output, 'img' : prediction.img2str(imgpath)}}), 200
  

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000)) #Define port so we can map container port to localhost
    app.run(host='0.0.0.0', port=port, debug=True)  #Define 0.0.0.0 for Docker
