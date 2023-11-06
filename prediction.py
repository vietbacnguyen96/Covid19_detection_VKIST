from tensorflow import keras
import cv2
import numpy as np
import base64


model = keras.models.load_model("model/CNN_Model_2c_6_11_25_epoch.h5")
resize = 150

def preprocess_image(image):
    image_ = cv2.imread(image)
    image = cv2.cvtColor(image_, cv2.COLOR_BGR2RGB) 
    image = cv2.resize(image, (resize, resize)) /255
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    return image

def prediction(image):
    image = preprocess_image(image)
    output = model.predict(image)
    output = np.argmax(output,axis=1)
    if output == 0:
        return 'COVID-19'
    elif output == 1:
        return 'Normal'
    else:
        return 'Pneumonia'
    
def img2str(imgpath):
    image = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    _, encimg = cv2.imencode(".jpg", image)
    img_byte = encimg.tobytes()
    img_str = base64.b64encode(img_byte).decode('utf-8')
    new_img_str = "data:image/jpeg;base64," + img_str
    return new_img_str
