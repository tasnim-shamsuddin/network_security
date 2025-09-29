import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _, _, exc_tb = error_details
        if exc_tb is not None:
            self.line_number = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.line_number = None
            self.file_name = None

    def __str__(self):
        return f"Error occurred in script: [{self.file_name}] at line number: [{self.line_number}]. Error message: [{self.error_message}]"

if __name__ == "__main__":
    try:
        logger.logging.info("Starting the try block")
        a = 1 / 0
        print("This will not be printed", a)
    except Exception as e:
        raise NetworkSecurityException(e, sys.exc_info())