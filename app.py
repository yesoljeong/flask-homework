from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def write_review():
    order_pname = request.form['order_pname']
    order_count = request.form['order_count']
    order_adr = request.form['order_adr']
    order_phone = request.form['order_phone']

    doc = {
        'order_pname': order_pname,
        'order_count': order_count,
        'order_adr': order_adr,
        'order_phone': order_phone
    }

    db.orders.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '주문서가 작성되었습니다'})


@app.route('/orders', methods=['GET'])
def read_reviews():
    orders = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'msg': '리뷰를 받아왔습니다!', 'orders': orders})


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run('localhost', port=5000, debug=True)
