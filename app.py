from flask import Flask, request, render_template, redirect, flash, jsonify, send_from_directory
import subprocess
import os
import json
import boto3

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'my-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'

def timeout_command(command, timeout):
  import subprocess, datetime, os, time, signal
  start = datetime.datetime.now()
  process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  while process.poll() is None:
    time.sleep(0.1)
    now = datetime.datetime.now()
    if (now - start).seconds > timeout:
      os.kill(process.pid, signal.SIGKILL)
      os.waitpid(-1, os.WNOHANG)
      return "Infinite loop"
  return subprocess.getoutput(" ".join(command))

@app.route('/', methods=['GET'])
def index():

	if request.method == 'GET':
		version = subprocess.getoutput('./pulse version')

		version = version.split("\n")[3]

		return render_template('index.html', version=version)

@app.route('/run', methods=['POST'])
def run():

	if request.method == 'POST':

		code = request.form['code']
		filename = "static/codes/" + request.form['filename']

		file = open(filename, "w")
		file.write(code)
		file.close()

		text = timeout_command(["./pulse", filename], 3)

		icon = 'error'
		title = 'Error'
		if('[line' not in text and '== code ==' in text):
			icon = 'success'
			title = 'Success'

	return jsonify({"icon": icon, "title": title, "text": text})

@app.route('/submit', methods=['POST'])
def submit():

	if request.method == 'POST':

		S3_BUCKET = os.environ.get('S3_BUCKET')

		code = request.form['code']
		filename = "static/codes/" + request.form['filename']
		file_type = "text/plain"

		file = open(filename, "w")
		file.write(code)
		file.close()

		text = timeout_command(["./pulse", filename], 3)

		icon = 'error'
		title = 'Error'
		if('[line' not in text and '== code ==' in text):
			icon = 'success'
			title = 'Success'
			text = 'Submitted successfully to S3!'

			s3 = boto3.resource('s3')

			bucket = s3.Bucket(S3_BUCKET)

			file_name = "codes/" + filename.split("/")[-1]

			objs = list(bucket.objects.filter(Prefix=file_name))

			if(file_name in [w.key for w in objs]):
				return jsonify({"icon": "error", "title": "File exists!", "text": "File already exists in S3"})

			bucket.upload_file(filename, file_name)

	return jsonify({"icon": icon, "title": title, "text": text})
