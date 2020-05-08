from flask import Flask, request, render_template, redirect, flash, jsonify, send_from_directory
import subprocess

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

		code = request.form['code']
		filename = "static/codes/" + request.form['filename']

		file = open(filename, "w")
		file.write(code)
		file.close()

		text = subprocess.getoutput('pulse ' + filename)

		icon = 'error'
		title = 'Interpret Error'
		if('== code ==' in text):
			icon = 'success'
			title = 'Interpreted Successfully'

		return jsonify({"icon": icon, "title": title, "text": text})
