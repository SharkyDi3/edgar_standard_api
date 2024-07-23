# app.py
import datetime
import logging
import os
import pandas as pd

from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Resource, Api

from operations import Operations
from utils.InputRequestValidation import InputRequestValidation
from utils.LogUtils import LogInitialization
from utils.errorcode import ErrorCodes

app = Flask(__name__)
api = Api(app)


class ReadRecords(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        log_name = 'EdgarAPI'
        LogInitialization().logger_func(log_name)
        self.errorCodes = ErrorCodes()

    def ResponseJsonObject(
            self,
            timetaken,
            status_code,
            status,
            output
    ):
        return {
            "status": status,
            "statusCode": status_code,
            "respTime": timetaken,
            "output": output
        }

    def post(self):
    
        start_time = datetime.datetime.now()
        self.logger.debug("Request processing started : Start Time : " + str(start_time))
    
        ### Generate Response Object
        timetaken = (datetime.datetime.now() - start_time).total_seconds()
        status_code = self.errorCodes.InternalError
        status = self.errorCodes.return_error_message(status_code)
        output = None
        response = self.ResponseJsonObject(timetaken, status_code, status, output)
    
        ### Read request json and validate
        json_data = request.json
        request_valid_flag = InputRequestValidation().request_validation(json_data)
        self.logger.debug("Input request validation : ")
        self.logger.debug(str(request_valid_flag))
    
        if request_valid_flag == "valid":
            op = Operations()
            output = op.query_records(json_data['id'])
            if output is not None:
                status_code = self.errorCodes.Success
                status = self.errorCodes.return_error_message(status_code)
            else:
                status_code = self.errorCodes.InternalError
                status = self.errorCodes.return_error_message(status_code)
            timetaken = (datetime.datetime.now() - start_time).total_seconds()
            output = output.to_dict(orient='records')
            response = self.ResponseJsonObject(timetaken, status_code, status, output)
        else:
            status_code = self.errorCodes.BadRequest
            status = self.errorCodes.return_error_message(status_code)
            output = None
            timetaken = (datetime.datetime.now() - start_time).total_seconds()
            output = output.to_dict(orient='records')
            response = self.ResponseJsonObject(timetaken, status_code, status, output)
    
        self.logger.debug("Request processing done : End time : " + str(datetime.datetime.now()))
        self.logger.debug(str(output))
        LogInitialization().close_logger(self.logger)
        # json_data = output.to_json(orient='records')
        # print(output)
        # print(type(response))
        return response
    
class UpdateRecord(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        log_name = 'EdgarAPI'
        LogInitialization().logger_func(log_name)
        self.errorCodes = ErrorCodes()

    def ResponseJsonObject(
            self,
            timetaken,
            status_code,
            status,
            output
    ):
        return {
            "status": status,
            "statusCode": status_code,
            "respTime": timetaken,
            "output": output
        }

    def put(self):
    
        start_time = datetime.datetime.now()
        self.logger.debug("Request processing started : Start Time : " + str(start_time))
    
        ### Generate Response Object
        timetaken = (datetime.datetime.now() - start_time).total_seconds()
        status_code = self.errorCodes.InternalError
        status = self.errorCodes.return_error_message(status_code)
        output = None
        response = self.ResponseJsonObject(timetaken, status_code, status, output)
    
        ### Read request json and validate
        json_data = request.json
        request_valid_flag = InputRequestValidation().update_request_validation(json_data)
        self.logger.debug("update request validation : ")
        self.logger.debug(str(request_valid_flag))
    
        if request_valid_flag == "valid":
            op = Operations()
            output = op.delete_record(json_data['id'], json_data['filings'], json_data['descr'], json_data['filed_effective'], json_data['file_film_number'])
            if output is not None:
                status_code = self.errorCodes.Success
                status = self.errorCodes.return_error_message(status_code)
            else:
                status_code = self.errorCodes.InternalError
                status = self.errorCodes.return_error_message(status_code)
            timetaken = (datetime.datetime.now() - start_time).total_seconds()
            # output = output.to_dict(orient='records')
            response = self.ResponseJsonObject(timetaken, status_code, status, output)
        else:
            status_code = self.errorCodes.BadRequest
            status = self.errorCodes.return_error_message(status_code)
            output = None
            timetaken = (datetime.datetime.now() - start_time).total_seconds()
            # output = output.to_dict(orient='records')
            response = self.ResponseJsonObject(timetaken, status_code, status, output)
    
        self.logger.debug("Request processing done : End time : " + str(datetime.datetime.now()))
        self.logger.debug(str(output))
        LogInitialization().close_logger(self.logger)
        return response
    
class DeleteRecord(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        log_name = 'EdgarAPI'
        LogInitialization().logger_func(log_name)
        self.errorCodes = ErrorCodes()

    def ResponseJsonObject(
            self,
            timetaken,
            status_code,
            status,
            output
    ):
        return {
            "status": status,
            "statusCode": status_code,
            "respTime": timetaken,
            "output": output
        }
    
    def delete(self):
        start_time = datetime.datetime.now()
        self.logger.debug("Request processing started : Start Time : " + str(start_time))
    
        ### Generate Response Object
        timetaken = (datetime.datetime.now() - start_time).total_seconds()
        status_code = self.errorCodes.InternalError
        status = self.errorCodes.return_error_message(status_code)
        output = None
        response = self.ResponseJsonObject(timetaken, status_code, status, output)
    
        ### Read request json and validate
        json_data = request.json
        request_valid_flag = InputRequestValidation().request_validation(json_data)
        self.logger.debug("delete request validation : ")
        self.logger.debug(str(request_valid_flag))
    
        if request_valid_flag == "valid":
            op = Operations()
            output = op.delete_record(json_data['id'])
            if output is not None:
                status_code = self.errorCodes.Success
                status = self.errorCodes.return_error_message(status_code)
            else:
                status_code = self.errorCodes.InternalError
                status = self.errorCodes.return_error_message(status_code)
            timetaken = (datetime.datetime.now() - start_time).total_seconds()
            # output = output.to_dict(orient='records')
            response = self.ResponseJsonObject(timetaken, status_code, status, output)
        else:
            status_code = self.errorCodes.BadRequest
            status = self.errorCodes.return_error_message(status_code)
            output = None
            timetaken = (datetime.datetime.now() - start_time).total_seconds()
            # output = output.to_dict(orient='records')
            response = self.ResponseJsonObject(timetaken, status_code, status, output)
    
        self.logger.debug("Request processing done : End time : " + str(datetime.datetime.now()))
        self.logger.debug(str(output))
        LogInitialization().close_logger(self.logger)
        return response


api.add_resource(ReadRecords, '/read')
api.add_resource(UpdateRecord, '/update')
api.add_resource(DeleteRecord, '/delete')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=port, debug=False)
