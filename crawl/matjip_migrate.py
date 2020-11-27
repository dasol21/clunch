from pymongo import MongoClient

# 맛집 데이터는 seoul_matjip 이라는 데이터베이스에 저장하겠습니다.
client = MongoClient('mongodb://dada:1234@13.209.26.249', 27017)
db = client.seoul_matjip

localc = MongoClient('localhost', 27017)
localdb = localc.seoul_matjip

datas = list(localdb.restaurants.find({}, {'_id': False}))
db.restaurants.insert_many(datas)