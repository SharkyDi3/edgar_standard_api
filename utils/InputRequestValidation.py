import logging
import sys
import os
from datetime import date

class InputRequestValidation:
    """
    This class defines the functions for validating Input Json from Rest API
    """

    def __init__(self):
        """To initiate logger variable"""
        self.logger = logging.getLogger("Logs")
        extra = {
            "class_name": self.__class__.__name__,
        }
        self.logger = logging.LoggerAdapter(self.logger, extra)

    def request_validation(self, request):
        """
        :param request:
        :return:
        """
        # Validating Input Request Json
        input_signature = [
            "id"
        ]
        flag = 0
        try:
            if all(field in request for field in input_signature):
                if not(isinstance(request["id"], int)):
                    self.logger.error("id TypeError: Expecting Int")
                    flag = 1
            else:
                flag = 1
                self.logger.error("Missing required fields in input_signature")
            if flag == 1:
                return "not valid parameters"
            else:
                return "valid"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.error(str([exc_type, f_name, exc_tb.tb_lineno]))
            self.logger.error(str(e))
            return "internal error"
        
    def update_request_validation(self, request):
        """
        :param request:
        :return:
        """
        # Validating Input Request Json
        input_signature = [
            "target", "filings", "descr", "filed_effective", "file_film_number"
        ]
        flag = 0
        try:
            if all(field in request for field in input_signature):
                if not(isinstance(request["target"],int)):
                    self.logger.error("id TypeError: Expecting Int")
                    flag = 1
                if not(isinstance(request["filings"], str)):
                    self.logger.error("id TypeError: Expecting String")
                    flag = 1
                if not(isinstance(request["descr"], str)):
                    self.logger.error("id TypeError: Expecting String")
                    flag = 1
                if not(isinstance(request["filed_effective"], str)):
                    self.logger.error("id TypeError: Expecting String")
                    flag = 1
                if not(isinstance(request["file_film_number"], str)):
                    self.logger.error("id TypeError: Expecting String")
                    flag = 1
            else:
                flag = 1
                self.logger.error("Missing required fields in input_signature")
            if flag == 1:
                return "not valid parameters"
            else:
                return "valid"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.error(str([exc_type, f_name, exc_tb.tb_lineno]))
            self.logger.error(str(e))
            return "internal error"
