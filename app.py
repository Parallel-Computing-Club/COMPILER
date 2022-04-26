from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import logging
from utils import configure_logger
from serial_execution import serial_execute
from output import fetch_output, just_output
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    if request.method == "POST":
        data = request.form
        code = data["code"]
        input_data = data["input"]
        if data["type"] == "serial":
            resp = serial_execute(data)
        return render_template('index.html', code=code, output=resp["output"], input_data = input_data, status=resp["status"])
    return render_template('index.html')

@app.route('/run_api', methods=["POST"])
def run_api():
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')
        resp={"status": "pending", "output": "", "error": ""}
        
        try:
            data = request.form
            
            if data["type"]=="serial":
                resp=serial_execute(data)
                
                return jsonify(resp)
        except:
            return jsonify(resp)

@app.route('/get_status', methods=["GET"])
def get_status():
    if  request.type=="GET":
        exec_id = request.args.get('id')
        resp = fetch_output(exec_id)
        return jsonify(resp)

@app.route('/get_output', methods=["POST"])
def get_output():
    print("Damnn")
    if request.method == "POST":
        data = request.form
        print(data)
        exec_id = data["id"]
        if exec_id[-4:] == ".cpp":
            exec_id = exec_id[:-4]
        
        inp = data["input"]
        time_limit = data["time_limit"]
        
        resp = just_output(exec_id, inp, time_limit)

        return jsonify(resp)

@app.before_first_request
def logger_configuration():
    configure_logger()
                    
                    
if __name__ == "__main__":
    app.run(debug=True)
    