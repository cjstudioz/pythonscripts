import logging
import os
from threading import Thread
from time import sleep

def isWindows():
    return os.name == 'nt'    

def runInThreads(listOfTasks):
    for tasks in listOfTasks:
        taskTuple = (tasks,) if callable(tasks) else tasks
        threads = [Thread(target=task, name=str(task)) for task in taskTuple]
        for thread in threads:
            logging.info('running %s' % thread.name) 
            thread.start()
            
        list(map(Thread.join, threads)) # wait for all threads at this level to finish
        #TODO: check if completed successfully
        logging.info('done running %s' % str(tasks))    

########################## TEST ##########################        
def testRunInThreads():
    from functools import partial
    def ff(t):
        logging.info('sleeping %s' % t)    
        sleep(t)
        logging.info('wake up after %s' % t)    
    
    def f(t):
        return partial(ff, t
                       )
    tasks = [
        f(1),
        (f(2), f(4), f(6)),
        (f(3),),
    ]
    runInThreads(tasks)
