import sys
import traceback
import os
import click
import logging
class Log:
    def __init__(self,name):
        self.quiet = False
        self.traceback = False
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        print(f"<<<<inside {name}")

        self.logger.info(f">>>>inside {name}")

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        self.logger.info(message)
        # click.echo(message)
    

