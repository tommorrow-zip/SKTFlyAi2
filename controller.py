from flask import Flask, render_template, request, jsonify
import uuid, os

from DAO import DAO
from model import *
from config.BaseResponse import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


Dao = DAO()


# 메인화면
@app.route('/')
def index():
    return 'hello world'


'''
연결 확인 API
'''
@app.route('/test')
def testapi():
    return  "연결 성공"


'''
상품 조회 API
[GET] /api/products/<productIdx> : 
'''
@app.route('/api/products/<productIdx>', methods=['GET'])
def getProduct(productIdx):
    # req_data = request.get_json()
    getProductRes = Dao.getProduct(productIdx)

    #return json.dumps(BaseResponse(getProductRes.serialize()).serialize(), ensure_ascii=False, indent=4)
    return jsonify(BaseResponse(getProductRes.serialize()).serialize())


'''
이미지 업로드 API
[POST] /api/images
테스트 : curl -F "file=@test1.jpg" http://localhost:9875/api/images
'''
@app.route('/api/images', methods=['POST'])
def postImage():
    # TODO: 확장자 변경 및 이미지 저장 ############################
    # req 받아오기
    file = request.files['file']
    
    # uuid 생성
    file_uuid = uuid.uuid4() # 파일 Uuid 변환... (확장자X) ==> 사용자마다 다른 확장파일 ... 는 jpg 로 확정.

    # 이미지 서버 저장
    file.save(os.path.join('./UPLOAD_FOLDER', str(file_uuid)))
    #########################################################

    postImageRes = PostImageRes(file_uuid)

    return jsonify(BaseResponse(postImageRes.serialize()).serialize())




if __name__ == '__main__':
    app.run(debug=True, port=9876)