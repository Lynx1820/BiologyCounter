
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
import mahotas as mh
import numpy as np
from pylab import imshow, gray, show, jet, title
import os 
from werkzeug.utils import secure_filename
#upload folder is where you store the files
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
SIGMA = 16.5
SIGMA2 = 12
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/uploads/<filename>')
def uploaded_file(filename):
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
        sigma = request.form['sig']
        SIGMA = sigma
        sigma2 = request.form['sig2']
        SIGMA2 = sigma2
        print sigma2
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #we redirect the user to url_for('uploaded_file', filename=filename)
        f1 = mh.imread(filename)
        f0 = f1
        f = f0[:,:,0]
        #the first gaussian determines the blur
        #the higher the sigma, the blurier the image
        f2 = mh.gaussian_filter(f, int(SIGMA2))
        f = (f2 < f2.mean())
        labeled, total  = mh.label(f)
        imshow(labeled)
        #lower the sigma, the more local min it finds
        dnaf = mh.gaussian_filter(f2, int(SIGMA))
        rmax = mh.regmin(dnaf)
        seeds, final_total = mh.label(rmax)
        title("Microscopic Organisms Found:{}".format(int(final_total)))
        imshow(mh.overlay(f2, rmax))
        show()
    return '''
    <!doctype html>
    <html>
    <title>The Biology Counter</title>
    <style>
    body {
    background-color: #f1ead5;
    margin-left: 100px;
    }
    h1,input,h3{
    color: #347e91;
    margin-left: 100px;
    }

    p, p1{
    color: #347e91;
    margin-left: 100px;
    }

    </style>
    <body>
    <h1>BioCounter</h1>
    <p>Counting microorganisms is a tedious task that biologist have.
    BioCounter allows you to count them instantly.<p>
    <p>The way it works:<p>
    <p>BioCounter treats the image as an array. It first performs a gaussian filter 
    to separate the background from the objects. Sigma1 determines the stardard deviation 
    of the gaussian.In simpler terms, it increase the blur in image. 
    Next, it performs a second gaussian filter to determine the local min int the image to 
    account for merged cells. The Sigma2 will affect the number of local min the image finds.
    <table>
    <th><form action="" method=post enctype=multipart/form-data></th>
    <tr><td> <h3>Select New File: <input type=file name=file></h3></td></tr>
    <tr><td>
    <h3>Select Sigma1: <input type=number name=sig2></h3>
    </td></tr>
    <tr><td>
    <h3>Select Sigma2: <input type=number name=sig></h3>
    </td></tr>
    <tr><td>
    <input type=submit value=Submit>
    </td></tr>
    </table>  
    </form>
    <body>
    </html>
    '''
if __name__ == '__main__':
    app.run(debug = True)