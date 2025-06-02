from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Kết nối MongoDB từ biến môi trường
MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['smart_lockers']
lockers = db['lockers']
history = db['history']

# Khởi tạo tủ nếu chưa có
def init_lockers():
    if lockers.count_documents({}) == 0:
        for i in range(1, 4):
            lockers.insert_one({
                'number': i,
                'isLocked': True,
                'code': ''
            })

@app.route('/api/lockers', methods=['GET'])
def get_lockers():
    try:
        all_lockers = list(lockers.find({}, {'_id': 0}))
        return jsonify({'lockers': all_lockers})
    except:
        return jsonify({'error': 'Lỗi server'}), 500

@app.route('/api/lockers/toggle', methods=['POST'])
def toggle_locker():
    try:
        data = request.json
        locker_number = data.get('number')
        action = data.get('action')
        if not locker_number or not action:
            return jsonify({'error': 'Thiếu thông tin'}), 400

        result = lockers.find_one_and_update(
            {'number': locker_number},
            {'$set': {'isLocked': action == 'lock'}},
            return_document=True
        )

        if not result:
            return jsonify({'error': 'Không tìm thấy tủ'}), 404

        history.insert_one({
            'lockerNumber': locker_number,
            'action': action,
            'time': datetime.now()
        })

        return jsonify({'message': 'Thành công', 'locker': result})
    except:
        return jsonify({'error': 'Lỗi server'}), 500

@app.route('/api/lockers/set-code', methods=['POST'])
def set_code():
    try:
        data = request.json
        locker_number = data.get('number')
        code = data.get('code')
        if not locker_number or not code:
            return jsonify({'error': 'Thiếu thông tin'}), 400

        result = lockers.find_one_and_update(
            {'number': locker_number},
            {'$set': {'code': code}},
            return_document=True
        )

        if not result:
            return jsonify({'error': 'Không tìm thấy tủ'}), 404

        return jsonify({'message': 'Đã đặt mã khóa', 'locker': result})
    except:
        return jsonify({'error': 'Lỗi server'}), 500

@app.route('/api/lockers/history', methods=['GET'])
def get_history():
    try:
        recent_history = list(history.find({}, {'_id': 0}).sort('time', -1).limit(100))
        for item in recent_history:
            item['time'] = item['time'].strftime('%d/%m/%Y %H:%M:%S')
        return jsonify({'history': recent_history})
    except:
        return jsonify({'error': 'Lỗi server'}), 500

# Chạy app và init locker
if __name__ == '__main__':
    init_lockers()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
