from flask import Flask, request, render_template, redirect, flash, jsonify, send_from_directory
import subprocess
import os
import json
import boto3

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'my-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods=['GET'])
def index():

	if request.method == 'GET':
		return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():

	if request.method == 'POST':

		S3_BUCKET = os.environ.get('S3_BUCKET')

		code = request.form['code']
		filename = "static/codes/" + request.form['filename']
		file_type = "text/plain"

		file = open(filename, "w")
		file.write(code)
		file.close()

		text = subprocess.getoutput('./pulse ' + filename)

		icon = 'error'
		title = 'Interpret Error'
		if('== code ==' in text):
			icon = 'success'
			title = 'Interpreted Successfully'

			s3 = boto3.client('s3')

			s3.Bucket(S3_BUCKET).upload_file(filename, "dump/file")

			# filename = filename.split('/')[-1]
			#
			# presigned_post = s3.generate_presigned_post(
		    #   Bucket = S3_BUCKET,
		    #   Key = filename,
		    #   Fields = {"acl": "public-read", "Content-Type": file_type},
		    #   Conditions = [
		    #     {"acl": "public-read"},
		    #     {"Content-Type": file_type}
		    #   ],
		    #   ExpiresIn = 3600
		    # )
			#
			# print(presigned_post)
			# print('https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, filename))

		return jsonify({"icon": icon, "title": title, "text": text})
