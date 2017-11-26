import base64
import json
import shutil
import uuid

from flask import Flask, render_template, request
from werkzeug import secure_filename

from service import get_label, get_similar

app = Flask(__name__)

uploadedImageFolder = "static/uploadedImages/"


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/testupload')
def test_upload_file():
    return render_template('test.html')


@app.route('/uploader', methods=['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']

        f.save(secure_filename(f.filename))
        shutil.move(f.filename, uploadedImageFolder)
        return 'file uploaded successfully'


@app.route('/templatetest')
def template_test():
    return render_template('similarImagesResults.html', my_string="img.jpg!", my_list=['img.jpg'])


@app.route('/find_similar', methods=['GET', 'POST'])
def find_similar_images():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        shutil.move(f.filename, uploadedImageFolder + f.filename)
        similar_images, label_name = get_label(f.filename)
        return render_template('similarImagesResults.html', input_label=label_name, similar_list=similar_images,
                               input_file=f.filename)


_valid_json = '''
{
	"name": "Polo Shirt",
	"type": "Men's Shirt",
	"url": "/static/inputFiles/menShirt/n04197391_10607_0.jpg",
	"sales": {
		"week": 120,
		"month": 2000,
		"season": 4500
	},
	"cost-price": 100
}
'''


@app.route('/mobile/upload', methods=['POST'])
def mobile_upload():
    file_location = "static/uploadedImages/"
    request_data = base64.b64decode(request.values['image'])
    file_name = str(uuid.uuid4()) + ".jpg"

    with open(file_location + file_name, "w") as f:
        f.write(request_data)

    f.close()

    return '{"file_name": "' + file_name + '"}'


@app.route('/mobile/label', methods=['GET'])
def mobile_label():
    file_name = request.args['file_name']
    label_name = get_label(file_name)

    return '{"label_name": "' + label_name + '"}'


@app.route('/mobile/similar', methods=['GET'])
def mobile_similar():
    file_name = request.args['file_name']
    label_name = get_label(file_name)

    similar_images = get_similar(file_name, label_name)

    valid_json = json.loads(_valid_json)

    urls = []
    for url in similar_images:
        urls.append('static/inputFiles/' + label_name + "/" + url)

    valid_json['url'] = urls
    valid_json['name'] = label_name
    valid_json['type'] = label_name.upper()

    response_json = json.dumps(valid_json)

    return response_json


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
