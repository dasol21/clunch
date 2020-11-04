import requests
import pprint
from pymongo import MongoClient
import time

# 맛집 데이터는 seoul_matjip 이라는 데이터베이스에 저장하겠습니다.
client = MongoClient('localhost', 27017)
db = client.seoul_matjip

# 서울시 구마다 맛집을 검색해보겠습니다.
seoul_station = ["서울역"]

# 네이버 검색 API 신청을 통해 발급받은 아이디와 시크릿 키를 입력합니다.
client_id = "NeWxGvcETd24jUyfpIOT"
client_secret = "RxU3pp1ujV"

# 검색어를 '강남구 맛집'으로 하겠습니다.
keyword = '서울역 맛집'
foods = ['족발', '국밥', '돈까스', '국수', '삼겹', '파스타', '피자', '햄버거','일식','찌개','중식','샌드위치','빵','삼계탕','치킨','떡볶이','마라','초밥','카레','양','덮밥','닭','샐러드','맥주']

# url에 전달받은 검색어를 삽입합니다.

# 아이디와 시크릿 키를 부가 정보로 같이 보냅니다.
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }

dict = {}

for food in foods:
    keyword = "서울역 "+food
    api_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=5&start=1&sort=random"
    print(api_url)

    # 검색 결과를 data에 저장합니다.
    resp = requests.get(api_url, headers=headers)
    # 받아온 JSON 결과를 딕셔너리로 변환합니다.
    data = resp.json()

    if 'items' not in data:
        print(data)
        continue

    items = data["items"]

    for item in items:
        dict[item["address"]] = item

    time.sleep(0.5)

restaurants = list(dict.values())
db.restaurants.insert_many(restaurants)

pprint.pprint(len(dict))
# pprint.pprint(dict)
