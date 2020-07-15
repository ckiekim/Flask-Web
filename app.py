from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import datetime
import os
import cv2
from tensorflow import keras
from keras.applications.resnet50 import ResNet50, decode_predictions

app = Flask(__name__)
#app.config["IMAGE_UPLOADS"] = os.path.join(app.root_path, 'static/images/uploads')

resnet = ResNet50()
now = datetime.datetime.now()
dow = ['월', '화', '수', '목', '금', '토', '일']
today = ''

''' @app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values) '''

@app.route('/')
def index():
    global today
    today = now.strftime('%Y-%m-%d') + ' (' + dow[now.weekday()] + ')'
    menu = {'home':True, 'regression':False, 'jumbo':False, 'classification':False}
    return render_template('home.html', menu=menu, today=today)

@app.route('/regression', methods=['GET', 'POST'])
def regression():
    menu = {'home':False, 'regression':True, 'jumbo':False, 'classification':False}
    if request.method == 'GET':
        return render_template('regression.html', menu=menu, today=today)
    else:
        sp_names = ['Setosa', 'Versicolor', 'Virginica']
        slen = float(request.form['slen'])      # Sepal Length
        plen = float(request.form['plen'])      # Petal Length
        pwid = float(request.form['pwid'])      # Petal Width
        sp = int(request.form['species'])       # Species
        species = sp_names[sp]
        swid = 0.63711424 * slen - 0.53485016 * plen + 0.55807355 * pwid - 0.12647156 * sp + 0.78264901
        swid = round(swid, 4)
        iris = {'slen':slen, 'swid':swid, 'plen':plen, 'pwid':pwid, 'species':species}
        return render_template('reg_result.html', menu=menu, today=today, iris=iris)

@app.route('/classification', methods=['GET', 'POST'])
def classification():
    menu = {'home':False, 'regression':False, 'jumbo':False, 'classification':True}
    if request.method == 'GET':
        return render_template('classification.html', menu=menu, today=today)
    else:
        f = request.files['image']
        filename = os.path.join(app.root_path, 'static/images/uploads/') + secure_filename(f.filename)
        f.save(filename)

        img = cv2.imread(filename, -1)
        img = cv2.resize(img, (224, 224))
        yhat = resnet.predict(img.reshape(-1, 224, 224, 3))
        label = decode_predictions(yhat)
        return render_template('cla_result.html', menu=menu, today=today, 
                                filename=secure_filename(f.filename), label=label[0][0][1])

@app.route('/jumbotron')
def jumbotron():
    menu = {'home':False, 'regression':False, 'jumbo':True, 'classification':False}
    return render_template('jumbotron.html', menu=menu, today=today)

@app.route('/bottom')
def bottom():
    return render_template('bottom.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)