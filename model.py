from __future__ import annotations

class GetProductRes:
    def __init__(self, productIdx, productName, productPrice, productDescrip, productUrl, productImgs):
        self.productIdx = productIdx
        self.productName = productName
        self.productPrice = productPrice
        self.productDescrip = productDescrip
        self.productUrl = productUrl
        self.productImgs = productImgs

    def serialize(self):
        return {
            'productIdx': self.productIdx,
            'productName': self.productName,
            'productPrice': self.productPrice,
            'productDescrip': self.productDescrip,
            'productUrl': self.productUrl,
            'productImgs': self.productImgs
        }
    

class PostImageRes:
    def __init__(self, imageUuid, filePath):
        self.imageUuid = imageUuid
        self.filePath = filePath

    def serialize(self):
        return {
            'imageUuid': self.imageUuid,
            'filePath': self.filePath
        }
    


'''
    "label": "style_name1",
    "probability": 0.8
'''
class Style:
    def __init__(self, label, probability):
        self.label = label
        self.probability = probability

    def serialize(self):
        return {
            'label': self.label,
            'probability': self.probability
        }



'''
"idx": 1,
"img_path": "http://qwer.asdf1.jpg"}
'''
class Detect_furniture:
    def __init__(self, idx, img_path):
        self.idx = idx
        self.img_path = img_path

    def serialize(self):
        return {
            'idx': self.idx,
            'img_path': self.img_path
        }



'''
"furniture_idx": 123,
"name": "가구 이름",
"price": 12345,
"image": "http://qwer.asdf",
"description": "가구 설명",
"url": "http://naver.com",
"ar_path": "http://ar.asdf"
'''
class Recommend_furniture:
    def __init__(self, furniture_idx, name, price, image, description, url, ar_path):
        self.furniture_idx = furniture_idx
        self.name = name
        self.price = price
        self.image = image
        self.description = description
        self.url = url
        self.ar_path = ar_path

    def serialize(self):
        return {
            'furniture_idx': self.furniture_idx,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'description': self.description,
            'url': self.url,
            'ar_path': self.ar_path
        }
    
'''
형태 : style(list<Style>), detect(list<Detect_furniture>)
recommend_list(list<Recommend_furniture>), recommend_furniture(Recommend_furniture)
'''
class GetImageRes():
    def __init__(self, style: list[Style], detect: list[Detect_furniture], recommend_list: list[Recommend_furniture]):
        self.style = style
        self.detect = detect
        self.recommend_list = recommend_list
    #list(map(lambda x:x*x, range(1,6)))
    def serialize(self):
        return {
            'style': list(map(lambda x: x.serialize() , self.style)),
            'detect': list(map(lambda x: x.serialize() , self.detect)),
            'recommend_list': list(map(lambda x: x.serialize() , self.recommend_list)),
        }
