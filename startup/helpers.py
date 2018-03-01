import logging

def setLogger(level):
    rl = logging.getLogger()
    rl.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(threadName)s|%(levelname)s|%(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    rl.addHandler(ch)
