from flask import Flask, request, render_template, jsonify
from scraper import find_empty_rooms
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def scrape():
    time_slot = request.args.get('time_slot')
    empty_rooms = find_empty_rooms(time_slot)

    # Dữ liệu cần truyền vào template
    data = {
        "time_slot": time_slot,
        "empty_rooms": empty_rooms
    }

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
