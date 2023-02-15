from config.BaseResponseStatus import *


class BaseResponse() :
    def __init__(self, result):
        self.isSuccess = BaseResponseStatus.SUCCESS.isSuccess
        self.message = BaseResponseStatus.SUCCESS.message
        self.code = BaseResponseStatus.SUCCESS.code
        self.result = result

    def serialize(self):
        return {
            'isSuccess': self.isSuccess,
            'message': self.message,
            'code': self.code,
            'result': self.result,
        }
