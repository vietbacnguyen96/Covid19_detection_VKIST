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
        return jsonify({"result": {'message': 'okay', 'imgpath': imgpath, 'prediction' : output}}), 200
      
@app.route('/getData', methods=[ 'POST', 'GET'])
def getData():
  if request.method == 'POST':

    data = request.form  # Access form data sent in the request

    # Accessing form data elements
    filename = data.get('filename')
    print(filename)
    if 'img' not in request.files:
        return 'No file part'

    file = request.files['img']

    if filename == '':
        return 'No selected file'

    if file:
        # Read the uploaded image and print its shape
        img = Image.open(io.BytesIO(file.read()))
        # img_shape = img.size  # Getting the shape (width, height)

        imgpath = save_path + filename
        img.save(os.path.join(app.config["Uploaded_images"], filename))
        output = prediction.prediction(imgpath)
    return jsonify([{'prediction' : output}]), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7002)) #Define port so we can map container port to localhost
    app.run(host='0.0.0.0', port=port, debug=True)  #Define 0.0.0.0 for Docker
