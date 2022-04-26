import os
from utils import get_unique_identifier
import logging
import subprocess
from subprocess import PIPE
import file_ops
from safe_check import validate_input
import multiprocessing


SAFE_MODE = True



def parallel_execute(data):
    if "code" not in data or "input" not in data or "time_limit" not in data or "lang" not in data or "user_id" not in data:
        resp = {"status": "error", "output": "Missing Arguments", "id": "NULL"}
        

    logging.info("Running in parallel")
    exec_id = get_unique_identifier(data["user_id"])
    code = data["code"]
    input_data = data["input"]

    
    if SAFE_MODE:
        logging.info("Safe Mode enabled, validating Input")
        if not validate_input(input_data):
            resp = {"status": "Error", "output": "Invalid Input", "id": exec_id}
            file_ops.write_code(resp["output"],  "txt", exec_id, "outputs/")
            return resp

    m = multiprocessing.Manager()

    code_path = file_ops.write_code(code, data["lang"], exec_id)
    logging.info("Code written to "+code_path)
    #compile the code
    logging.info("Compiling the code")
    

