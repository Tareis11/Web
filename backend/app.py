from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Kết nối MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['smart_lockers']
lockers = db['lockers']  # Bảng tủ
history = db['history']  # Bảng lịch sử

# Khởi tạo tủ nếu chưa có
def init_lockers():
    if lockers.count_documents({}) == 0:
        for i in range(1, 4):
            lockers.insert_one({
                'number': i,
                'isLocked': True,
                'code': ''
            })

# API lấy danh sách tủ
@app.route('/api/lockers', methods=['GET'])
def get_lockers():
    try:
        # Lấy tất cả tủ từ database
        all_lockers = list(lockers.find({}, {'_id': 0}))
        return jsonify({'lockers': all_lockers})
    except Exception as e:
        return jsonify({'error': 'Lỗi server'}), 500

# API mở/đóng tủ
@app.route('/api/lockers/toggle', methods=['POST'])
def toggle_locker():
    try:
        # Lấy số tủ và hành động từ request
        data = request.json
        locker_number = data.get('number')
        action = data.get('action')  # 'lock' hoặc 'unlock'

        if not locker_number or not action:
            return jsonify({'error': 'Thiếu thông tin'}), 400

        # Cập nhật trạng thái tủ
        result = lockers.find_one_and_update(
            {'number': locker_number},
            {'$set': {'isLocked': action == 'lock'}},
            return_document=True
        )

        if not result:
            return jsonify({'error': 'Không tìm thấy tủ'}), 404

        # Ghi lịch sử
        history.insert_one({
            'lockerNumber': locker_number,
            'action': action,
            'time': datetime.now()
        })

        return jsonify({'message': 'Thành công', 'locker': result})
    except Exception as e:
        return jsonify({'error': 'Lỗi server'}), 500

# API đặt mã khóa
@app.route('/api/lockers/set-code', methods=['POST'])
def set_code():
    try:
        data = request.json
        locker_number = data.get('number')
        code = data.get('code')

        if not locker_number or not code:
            return jsonify({'error': 'Thiếu thông tin'}), 400

        # Cập nhật mã khóa
        result = lockers.find_one_and_update(
            {'number': locker_number},
            {'$set': {'code': code}},
            return_document=True
        )

        if not result:
            return jsonify({'error': 'Không tìm thấy tủ'}), 404

        return jsonify({'message': 'Đã đặt mã khóa', 'locker': result})
    except Exception as e:
        return jsonify({'error': 'Lỗi server'}), 500

# API lấy lịch sử
@app.route('/api/lockers/history', methods=['GET'])
def get_history():
    try:
        # Lấy lịch sử 100 hoạt động gần nhất
        recent_history = list(history.find(
            {},
            {'_id': 0}
        ).sort('time', -1).limit(100))

        # Chuyển đổi thời gian thành chuỗi
        for item in recent_history:
            item['time'] = item['time'].strftime('%d/%m/%Y %H:%M:%S')

        return jsonify({'history': recent_history})
    except Exception as e:
        return jsonify({'error': 'Lỗi server'}), 500

# Khởi tạo tủ khi chạy server
init_lockers()

if __name__ == '__main__':
    app.run(debug=True, port=5000) 