from pymongo import MongoClient

# 맛집 데이터는 seoul_matjip 이라는 데이터베이스에 저장하겠습니다.
client = MongoClient('mongodb://dada:1234@localhost', 27017)
db = client.seoul_matjip

db.restaurants.update_many({}, {'$set': {'hate':0, 'like':0}})