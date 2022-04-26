import os
import logging

def output_exists(file_name,file_path='outputs/'):
    '''
    This function checks if the output file exists
    '''
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        
    if os.path.exists(file_path+file_name+".txt"):
        return True
    else:
        return False

def write_code(code: str, lang:str, exec_id: str, file_path = 'codes/') ->str:
    '''
    Arguements
    code: string(Actual code)
    lang : string (language of the code [To work the extension])
    exec_id : string (A unique execution id for the code. this will be the file
    name of the code)
    file_path : option parameter, pass the directory where the code is supposed 
    to be stored)

    returns
    the complete relative path for the code (can be used to compile and then run)
    '''

    #check if the file path directory exists. If not create it
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        logging.info("Directory Does not exist. Creating it")
    
    code_path = file_path+exec_id+'.'+lang
    if not os.path.exists(code_path):
        os.open(code_path, os.O_CREAT)
        logging.info("File Does not exist. Creating it")
    
    #write the code to the file
    fd=os.open(code_path,os.O_WRONLY)
    os.truncate(fd,0)
    contents=str.encode(code)
    os.write(fd,contents)
    os.close(fd)
    logging.info("Created file "+exec_id+'.'+lang+" at "+code_path)
    return code_path

def clean_up(code_path: str):
    
    ''' This code path is supposed to be the full code path'''
    logging.info("Removing Code "+code_path)
    if os.path.exists(code_path):
        os.remove(code_path)
        logging.info("Deleted file "+code_path)
    else:
        logging.info("Code File does not exist")
    
    
 
    