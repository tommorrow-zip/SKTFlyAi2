from enum import Enum

class BaseResponseStatus(Enum):
     # 1000 : 요청 성공
    SUCCESS = (True, 1000, "요청에 성공하였습니다.")


    # 2000 : Request 오류
    REQUEST_ERROR = (False, 2000, "입력값을 확인해주세요.")
    EMPTY_JWT = (False, 2001, "JWT를 입력해주세요.")
    INVALID_JWT = (False, 2002, "유효하지 않은 JWT입니다.")
    INVALID_USER_JWT = (False,2003,"권한이 없는 유저의 접근입니다.")

    # users
    USERS_EMPTY_USER_ID = (False, 2010, "유저 아이디 값을 확인해주세요.")

    # [POST] /users
    POST_USERS_EMPTY_EMAIL = (False, 2015, "이메일을 입력해주세요.")
    POST_USERS_INVALID_EMAIL = (False, 2016, "이메일 형식을 확인해주세요.")
    POST_USERS_EXISTS_EMAIL = (False,2017,"중복된 이메일입니다.")


    # 3000 : Response 오류
    RESPONSE_ERROR = (False, 3000, "값을 불러오는데 실패하였습니다.")

    # [POST] /users
    DUPLICATED_EMAIL = (False, 3013, "중복된 이메일입니다.")
    FAILED_TO_LOGIN = (False,3014,"없는 아이디거나 비밀번호가 틀렸습니다.")


    
    # 4000 : Database, Server 오류
    DATABASE_ERROR = (False, 4000, "데이터베이스 연결에 실패하였습니다.")
    SERVER_ERROR = (False, 4001, "서버와의 연결에 실패하였습니다.")

    # [PATCH] /users/{userIdx}
    MODIFY_FAIL_USERNAME = (False,4014,"유저네임 수정 실패")

    PASSWORD_ENCRYPTION_ERROR = (False, 4011, "비밀번호 암호화에 실패하였습니다.")
    PASSWORD_DECRYPTION_ERROR = (False, 4012, "비밀번호 복호화에 실패하였습니다.")

    # 9000
    UNKNOWN_ERROR = (False, 9999, "알 수 없는 에러가 발생했습니다.")

    
    def __init__(self, isSuccess, code, message):
        self.isSuccess = isSuccess
        self.code = code
        self.message = message
        
    # @property
    # def surface_gravity(self):
    #     # 중력 상수  (m3 kg-1 s-2)
    #     G = 6.67300E-11
    #     return G * self.mass / (self.radius * self.radius)
    