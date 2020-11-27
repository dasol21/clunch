from random import shuffle

from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb://dada:1234@13.209.26.249', 27017)
#client = MongoClient('mongodb://dada:1234@localhost', 27017)
db = client.seoul_matjip


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def showrestaurant():
    restaurant = shuffle(list(db.restaurants.find({},{'_id': False}).sort('like', -1)))

    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'msg': restaurant})


@app.route('/api/like', methods=['POST'])
def like_restaurant():
    name_receive = request.form['name_give']
    restaurant = db.restaurants.find_one({'title': name_receive})
    new_like = restaurant['like'] + 1
    db.restaurants.update_one({'title': name_receive},{'$set': {'like': new_like}})
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '좋아요'})


@app.route('/api/delete', methods=['POST'])
def hate_restaurant():
    name_receive = request.form['name_give']
    restaurant = db.restaurants.find_one({'title': name_receive})
    new_hate = restaurant['hate'] + 1
    db.restaurants.update_one({'title':name_receive},{'$set':{'hate': new_hate}})

    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '싫어요'})

# 수정기록 남기는 테스트입니다.
# 슬랙 연결 노티가 올까요?

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)