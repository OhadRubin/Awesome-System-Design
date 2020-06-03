import sys
import traceback
import os
import click
import logging
class Log:
    def __init__(self,name=None):
        self.quiet = False
        self.traceback = False
        self.name = name
        
        
        

    def setName(self, name=None):
        # if name:
        # self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        # print(f"<<<<inside {name}")
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        # self.logger.
        self.logger.info(f">>>>inside {name}")
        


    def __call__(self, message):
        if self.quiet:
            return
        if not isinstance(message,str):
            message  = str(message)
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        self.logger.info(message)
        # click.echo(message)
    

