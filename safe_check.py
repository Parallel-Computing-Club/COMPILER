import logging


MAX_STRING = 20
MAX_INT = 10000
MIN_INT = -10000

def validate_input(input_data):
    ip = input_data.split("\n")
    tip = []
    for i in range(len(ip)):
        ip[i] = ip[i].split()
        tip.extend(ip[i])
    for i in tip:
        if i.isdigit():
            if int(i) > MAX_INT or int(i) < MIN_INT:
                logging.info("Invalid Input "+i)
                return False
        elif len(i) > MAX_STRING:
            logging.info("Invalid Input "+i)
            return False
        logging.info("Valid Input")
    return True
