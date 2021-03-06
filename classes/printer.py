import _thread
import time
import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys


class Printer:

    model = "biqu-printer"
    serial = "simulator-123456"
    status = "free"
    progress = 0
    temperature = 25
    token = "abcd"
    
    def __init__(self, model, serial, status, progess, temperature):
        self.model = model
        self.serial = serial
        self.status = status
        self.progess = progess
        self.temperature = temperature

    def threaded_prepare(self):
        self.status = "prepare"
        self.temperature = 50
        time.sleep(2)
        self.temperature = 100
        time.sleep(2)
        self.temperature = 200
        # Start printing
        self.status = "printing"

    def threaded_print(self):

        self.status = "printing"
        self.progess = 0
        time.sleep(10)
        self.progess = 30
        time.sleep(1)
        self.progess = 60
        time.sleep(10)
        self.progess = 100
        self.status = "done"

    def threaded_pause(self):
        self.status = "printing"

    def threaded_resume(self):
        self.status = "printing"

    def threaded_cancel(self):
        self.progess = 0
        self.status = "done"

    def prepare(self):
        logger.debug("start prepare")
        try:
            _thread.start_new_thread( self.threaded_prepare, () )
        except Exception as error:
            print ("Error: unable to start thread" + error)

    def print(self):
        logger.debug("start printing")
        try:
            _thread.start_new_thread( self.threaded_print, () )
        except Exception as error:
            print ("Error: unable to start thread" + error)

    def pause(self):
        try:
            _thread.start_new_thread( self.threaded_pause, () )
        except Exception as error:
            print ("Error: unable to start thread" + error)

    def cancel(self):
        try:
            _thread.start_new_thread( self.threaded_cancel, () )
        except Exception as error:
            print ("Error: unable to start thread" + error)

    def resume(self):
        try:
            _thread.start_new_thread( self.threaded_resume, () )
        except Exception as error:
            print ("Error: unable to start thread" + error)