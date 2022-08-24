from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/energy')
def energy():
    return render_template('energy.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/image-classification')
def image_classification():
    return render_template('img-classif.html')




import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import keras,sys
import numpy as np

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
image_size = 50

app=Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            #ファイルを識別器に渡して答えを返す。学習済みの識別器は.h5が拡張子
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            model = load_model('./man_woman_cnn.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)#Xをリスト型からnumpyの型に変換

            result = model.predict([X])[0]
            predicted = result.argmax()
            percentage = float(result[predicted] * 100)

            resultmsg = exec(open('test.py').read())
            return render_template('img-classif.html', resultmsg=resultmsg, filepath=filepath)

    return render_template('index.html')


from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
 


if __name__ == "__main__":
    app.run(debug=True)