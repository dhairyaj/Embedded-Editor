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

		file = open("static/test.pls", "w")
		file.write(code)
		file.close()

		output = subprocess.getoutput('pulse static/test.pls')

		file = open("out.txt", "w")
		file.write(output)
		file.close()

		return jsonify({"done": "done"})
