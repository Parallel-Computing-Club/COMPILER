import os, subprocess
from datetime import datetime
import logging
import filecmp

def configure_logger(file_name = "event_log.txt"):
    logging.basicConfig(filename=file_name, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Logger Initiated")
    
def compare_files(file1, file2):
    return filecmp.cmp(file1, file2)
    
def get_unique_identifier(param:str):
    t = datetime.now().strftime("%y%m%H%M%S%f")
    return t+"-"+param


def output_exists(file_name,file_path='output/', ext = '.txt'):
    '''
    This function checks if the output file exists
    '''
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        
    if os.path.exists(file_path+file_name+ext):
        return True
    else:
        return False

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

pwd = ""
def get_this_package(pkg):
    if is_tool(pkg):
        return 
    
    os.popen("sudo apt install g++").write(pwd).write("y")