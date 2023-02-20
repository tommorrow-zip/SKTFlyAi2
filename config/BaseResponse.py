from config.BaseResponseStatus import *


class BaseResponse() :
    def __init__(self, result, status=BaseResponseStatus.SUCCESS):
        self.isSuccess = status.isSuccess
        self.message = status.message
        self.code = status.code
        self.result = result

    def serialize(self, success=True):
        if success:
            return {
                'isSuccess': self.isSuccess,
                'message': self.message,
                'code': self.code,
                'result': self.result,
            }
        else:
            return {
                'isSuccess': self.isSuccess,
                'message': self.message,
                'code': self.code
            }
