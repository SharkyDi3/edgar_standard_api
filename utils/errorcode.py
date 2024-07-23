import os,sys

class ErrorCodes:
    """
    class to define error codes
    """

    def __init__(self):

        self.Success = 200
        self.InternalError = 500
        self.ClassNotFound = 404
        self.BadRequest = 400
        self.SuccessMsg = "Success"
        self.FailureMsg = "Failure"

    def return_error_message(self, error_code):
        """

        :type error_code:

        """
        error_message = {
            200: "Successful",
            500: "Internal Server error",
            404: "Requested resource not found",
            400: "Bad Request",
        }
        return error_message[error_code]

    def exception_block_info(self):
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return (exc_type, fname, exc_tb.tb_lineno)
