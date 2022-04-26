import os
from utils import get_unique_identifier
import logging
import subprocess
from subprocess import PIPE
import file_ops
from safe_check import validate_input

SAFE_MODE = False

def serial_execute(data):
    #check for all arguments
    if "code" not in data or "input" not in data or "time_limit" not in data or "lang" not in data or "user_id" not in data:
        resp = {"status": "error", "output": "Missing Arguments", "id": "NULL"}
        


    exec_id = get_unique_identifier(data["user_id"])
    code = data["code"]
    input_data = data["input"]

    if SAFE_MODE:
        logging.info("Safe Mode enabled, validating Input")
        if not validate_input(input_data):
            resp = {"status": "Error", "output": "Invalid Input", "id": exec_id}
            file_ops.write_code(resp["output"],  "txt", exec_id, "outputs/")
            return resp


    code_path = file_ops.write_code(code, data["lang"], exec_id)
    logging.info("Code written to "+code_path)
    #compile the code
    logging.info("Compiling the code")
    
    compile_code=subprocess.run(["g++", code_path, "-o", exec_id],stderr=PIPE)
    has_compiled = compile_code.returncode
    compiled_file_path = './'+exec_id
    logging.info("File Compiled with return code "+str(has_compiled))
    
    if has_compiled != 0:
        err = compile_code.stderr.decode('utf-8')
        logging.info("Error in Compilation : "+err)
        file_ops.clean_up(code_path)
        resp = {"output" : err, "status": "Compilation Error", "id": exec_id}
        file_ops.write_code(resp["output"],  "txt", exec_id, "outputs/")
        return resp
    
    
    #run the code 
    logging.info("Running the code")
    try:
        runfile = subprocess.run([compiled_file_path], input=input_data.encode('utf-8'), stdout=PIPE, stderr=PIPE, timeout=float(data["time_limit"]))
        if runfile.returncode == 0:
            output = runfile.stdout.decode('utf-8')
            status = "code ok"
        else:
            output = "Error in Execution"
            status = "Runtime Error"
        resp = {"output": output, "status": status, "id": exec_id}
        file_ops.write_code(resp["output"],  "txt", exec_id, "outputs/")
        logging.info("Code Executed")


    except subprocess.TimeoutExpired:
        logging.info("Time Limit Exceeded")
        resp = {"output" : "Time Limit Exceeded", "status": "Time Limit Exceeded", "id": exec_id}
        file_ops.write_code(resp["output"],  "txt", exec_id, "outputs/")

    except:
        logging.info("Runtime Error-Segmentation Fault")
        resp = {"output": "segmentation fault", "status": "Runtime Error",  "id":  exec_id}
        file_ops.write_code(resp["output"], "txt",  exec_id, "outputs/")
    file_ops.clean_up(code_path)
    file_ops.clean_up(exec_id)

    return resp


    