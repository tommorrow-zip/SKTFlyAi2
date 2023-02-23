from flask import Flask, render_template, request, jsonify
import uuid, os
from flask_cors import CORS, cross_origin

from DAO import DAO
from model import *
from config.BaseResponse import *
import config.config as conf

from PIL import Image
import pillow_heif
from PIL import UnidentifiedImageError

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

cors = CORS(app, resources={r"*": {"origins": "*"}})
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

    if isinstance(getProductRes, BaseResponseStatus):
        return jsonify(BaseResponse(None, status=getProductRes).serialize(False))

    #return json.dumps(BaseResponse(getProductRes.serialize()).serialize(), ensure_ascii=False, indent=4)
    return jsonify(BaseResponse(getProductRes.serialize()).serialize())


'''
이미지 업로드 API
[POST] /api/images
테스트 : curl -F "file=@test1.jpg" http://localhost:9875/api/images
'''
@app.route('/api/images', methods=['POST'])
def postImage():
    if 'file' not in request.files: # REQUEST_FORM_ERROR
        return jsonify(BaseResponse(None, status=BaseResponseStatus.REQUEST_FORM_ERROR).serialize(False))
    # req 받아오기
    file = request.files.get('file')

    # uuid 생성
    file_uuid = uuid.uuid4() # 파일 Uuid 변환... (확장자X) ==> 사용자마다 다른 확장파일 ... 는 jpg 로 확정.

    try:
        # 이미지 서버 저장 (확장자 변환)
        file_type = file.filename.split('.')[-1]
        if file_type.upper() == 'HEIC':
            heif_file = pillow_heif.read_heif(file)
            im = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
        else:
            im = Image.open(file).convert('RGB')
        
        file_name = f"/static/img/uploads/{file_uuid}.jpg"
        #file.save(os.path.join('./UPLOAD_FOLDER', str(file_uuid)))
        im.save(f".{file_name}", 'jpeg')

        file_path = f"http://{conf.db['host']}{file_name}"
        postImageRes = PostImageRes(file_uuid, file_path)

        return jsonify(BaseResponse(postImageRes.serialize()).serialize())
    
    except UnidentifiedImageError as e:
        print(e)
        return jsonify(BaseResponse(None, status=BaseResponseStatus.REQUEST_FORM_TYPE_ERROR).serialize(False))
    except Exception as e:
        print(e)
        return jsonify(BaseResponse(None, status=BaseResponseStatus.UNKNOWN_ERROR).serialize(False))


'''
이미지 결과 요청 API
[GET] /api/images/<uuid>
형태 : style(Style), detect(list<Detect_furniture>)
recommend_list(list<Recommend_furniture>), recommend_furniture(Recommend_furniture)
'''
@app.route('/api/images/<uuid>', methods=['GET'])
def getImage(uuid):
    # 1.
    # 받은 Uuid 로 다른 AI서버에 요청
    # 
    style = [Style("라벨1", 0.6), Style("라벨1", 0.4)]
    detect = [Detect_furniture(2, "http://img_path2"), Detect_furniture(4, "http://img_path4")]
    recommend_list = [Recommend_furniture(3, "가구 이름3", 333, "http://qwer3.asdf", "가구 설명3", "http://naver.com3", "http://ar.asdf3"),
                      Recommend_furniture(4, "가구 이름4", 444, "http://qwer4.asdf", "가구 설명4", "http://naver.com4", "http://ar.asdf4")]

    # style: Style, detect: list[Detect_furniture], recommend_list: list[Recommend_furniture]
    getImageRes = GetImageRes(style, detect, recommend_list)
    return jsonify(BaseResponse(getImageRes.serialize()).serialize())




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9875)
