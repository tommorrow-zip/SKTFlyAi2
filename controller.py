from flask import Flask, render_template, request, jsonify
import requests
import uuid, os
from flask_cors import CORS, cross_origin

from DAO import DAO
from model import *
from config.BaseResponse import *
import config.config as conf

from PIL import Image
import pillow_heif
from PIL import UnidentifiedImageError

import cv2, numpy as np
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

cors = CORS(app, resources={r"*": {"origins": "*"}})
Dao = DAO()


CLASSIFIER_LABELS = [
    "Asian",
    "Beach",
    "Contemporary",
    "Craftsman",
    "Eclectic",
    "Farmhouse",
    "Industrial",
    "Mediterranean",
    "Midcentury",
    "Modern",
    "Rustic",
    "Scandinavian",
    "Southwestern",
    "Traditional",
    "Transitional",
    "Tropical",
    "Victorian",
]

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

        file_path = f"https://{conf.db['domain']}{file_name}"
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
    if 'type' not in request.args:
        type_ = 0
    else:
        type_ = request.form.get("type")

    url = "http://34.64.109.102:3000/unified"
    

    files = {'image': open(f'./static/img/uploads/{uuid}.jpg', 'rb')}
    res = requests.post(url, files=files)
    res = res.json()


    
    # 디텍션 결과
    #print(f'type: {type(res)}, len: {len(res)}')
    objects = res["detected_object_location"]
    detect = [Detect_furniture(0, "linkaaasdf")]

    
    input_img = Image.open(f'./static/img/uploads/{uuid}.jpg').convert("RGB")

    img = np.array(input_img, dtype=np.uint8)
    layers = make_bbox_images_json(objects, img)
    for i, ly in enumerate(layers):
        # {"label": label, "unique_id": obj_id, "img": clipped_result}
        idx = ly['label']
        img = ly['img']

        # uuid 사용
        file_uuid = uuid + str(i)
        # 파일 저장
        file_path = f"/static/img/detect/{file_uuid}.jpg"
        cv2.imwrite(file_path, img)
        
        detect.append(Detect_furniture(idx, file_path))
    
    

    # 스타일
    styles = res['style']
    style = []
    for i_, (stt) in enumerate(styles.items()):
        #print(stt)
        for i, st in enumerate(stt[1]):
            if st != 0.0:
                style.append(Style(CLASSIFIER_LABELS[i], st))
        break
    #print(style)
    


    # 리커멘드
    recomm = res['recom']
    recommend_list = []
    for i_, (stt) in enumerate(recomm.items()):
        for rl in stt[1]: # productName, productPrice, productDescrip, productUrl
            getprod = Dao.getProduct(rl)
            # productIdx, productName, productPrice, productDescrip, productUrl, productImgs
            recommend_list.append(Recommend_furniture(rl, getprod.productName, getprod.productPrice, getprod.productImgs[0], getprod.productDescrip, getprod.productUrl, ""))
        
        break


    
    
    
    # style: Style, detect: list[Detect_furniture], recommend_list: list[Recommend_furniture]
    getImageRes = GetImageRes(style, detect, recommend_list)
    return jsonify(BaseResponse(getImageRes.serialize()).serialize())



def make_bbox_images_json(detected_objects, img):
    layers = []

    for i_, (label, objs) in enumerate(detected_objects.items()):
        objs = dict(objs)

        for obj_id, segms in objs.items():
            x, y, w, h = segms["bbox"]
            clipped_result = np.zeros(shape=img.shape, dtype=np.uint8)

            for segm in segms["segms"]:
                s = np.array(
                    list(zip(segm["segm"]["x"], segm["segm"]["y"])), dtype=np.int32
                )
                mask = np.zeros_like(clipped_result)
                mask = cv2.fillPoly(mask, [s], (255, 255, 255))
                clipped_result = cv2.add(clipped_result, cv2.bitwise_and(img, mask))

            clipped_result = clipped_result[y: y + h, x: x + w]
            clipped_result = cv2.resize(clipped_result, (100, 100))

            layers.append({"label": label, "unique_id": obj_id, "img": clipped_result})
            
    return layers



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9875)
