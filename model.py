class GetProductRes:
    def __init__(self, productIdx, productName, productPrice, productDescrip, productUrl):
        self.productIdx = productIdx
        self.productName = productName
        self.productPrice = productPrice
        self.productDescrip = productDescrip
        self.productUrl = productUrl

    def serialize(self):
        return {
            'productIdx': self.productIdx,
            'productName': self.productName,
            'productPrice': self.productPrice,
            'productDescrip': self.productDescrip,
            'productUrl': self.productUrl
        }
    

class PostImageRes:
    def __init__(self, imageUuid):
        self.imageUuid = imageUuid

    def serialize(self):
        return {
            'imageUuid': self.imageUuid
        }

    