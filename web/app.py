import os
import shutil

from flask import Flask, render_template, request
from werkzeug import secure_filename
from similaritySearch import find_similar
from service import get_label

app = Flask(__name__)

uploadedImageFolder = "static/uploadedImages/"

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/testupload')
def test_upload_file():
   return render_template('test.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def save_file():
   if request.method == 'POST':
      f = request.files['file']
      
      f.save(secure_filename(f.filename))
      shutil.move(f.filename, uploadedImageFolder )
      return 'file uploaded successfully'


@app.route('/templatetest')
def template_test():
    return render_template('similarImagesResults.html', my_string="img.jpg!", my_list=['img.jpg'])


@app.route('/find_similar', methods = ['GET', 'POST'])
def find_similar_images():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		shutil.move(f.filename, uploadedImageFolder + f.filename)
		similar_images, label_name = get_label(f.filename)
		return render_template('similarImagesResults.html', input_label=label_name, similar_list=similar_images, input_file=f.filename)
    

		
if __name__ == '__main__':
   app.run(debug = True)