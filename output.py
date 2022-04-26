import  os
from serial_execution import SAFE_MODE
from utils import output_exists
from file_ops import clean_up
import subprocess 
from subprocess import PIPE
import logging
from safe_check import validate_input
from serial_execution import SAFE_MODE


def fetch_output(exec_id):
    '''
    This function fetches the output of the code
    '''
    if output_exists(exec_id):
        with open(os.path.join('outputs',exec_id+'.txt'),'r') as f:
            output = f.read()
        status = "success"
    else:
        status = "No output found"
        output = " "
    clean_up(os.path.join('outputs',exec_id+'.txt'))
    return {"status": status, "output": output}

def just_output(exec_id, inp, time_limit):
    if not output_exists(exec_id, file_path = "compiled_files/", ext=""):
        resp = {"output": "File does not exits", "status": "error", "id": exec_id}
        return resp
    
    compiled_file_path = './compiled_files/'+exec_id
    input_data = inp

    logging.info("Running just the output on "+compiled_file_path)
    if SAFE_MODE:
        logging.info("Safe Mode enabled, validating Input")
        if not validate_input(input_data):
            resp = {"status": "Invalid Input", "output": "Invalid Input", "id": exec_id}
            return resp

    try:
        runfile = subprocess.run([compiled_file_path], input=input_data.encode('utf-8'), stdout=PIPE, stderr=PIPE, timeout=float(time_limit))
        if runfile.returncode == 0:
            output = runfile.stdout.decode('utf-8')
            status = "ok"
        else:
            output = "Error in Execution"
            status = "Runtime Error"
        resp = {"output": output, "status": status, "id": exec_id}
        
        logging.info("Code Executed")


    except subprocess.TimeoutExpired:
        logging.info("Time Limit Exceeded")
        resp = {"output" : "Time Limit Exceeded", "status": "Time Limit Exceeded", "id": exec_id}
        

    except:
        logging.info("Runtime Error-Segmentation Fault")
        resp = {"output": "segmentation fault", "status": "Runtime Error",  "id":  exec_id}

    logging.info("Just the output Fetched")
    return resp