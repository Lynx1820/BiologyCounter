from flask import Flask, request, redirect, url_for
from flask import send_from_directory
import mahotas as mh
import numpy as np
from pylab import imshow, gray, show, jet
import os 
from werkzeug.utils import secure_filename
#upload folder is where you store the files
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	f1 = mh.imread(filename)
	f0 = f1
	f = f0[:,:,0]
	f2 = mh.gaussian_filter(f, 8)
	f = (f2 < f2.mean())
	imshow(f)
	labeled, n_nucleus  = mh.label(f)
	print('Found {} nuclei.'.format(n_nucleus))
	imshow(labeled)
	print f2.shape
	dnaf = mh.gaussian_filter(f2, 16.5)
	rmax = mh.regmin(dnaf)
	imshow(mh.overlay(f2, rmax))
	show()
	seeds,nr_nuclei = mh.label(rmax)
	print nr_nuclei
    	return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #we redirect the user to url_for('uploaded_file', filename=filename)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>The Biology Counter</title>
    <h1>The Biology Counter</h1>
    <p1>Counting microscopic organisms is a tedious task that all biologist have.
    With The Biology Counter, you can count them instantly<p1>
    <h2>Upload New File<h2>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
if __name__ == '__main__':
   app.run(debug = True)