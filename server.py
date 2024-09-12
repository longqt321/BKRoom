from flask import Flask, request, render_template
from scraper import find_empty_rooms

app = Flask(__name__)

@app.route('/', methods=['GET'])
def scrape():
    time_slot = request.args.get('time_slot')
    if time_slot is None:
        time_slot = "7h00"
    empty_rooms = find_empty_rooms(time_slot)

    # Dữ liệu cần truyền vào template
    data = {
        "time_slot": time_slot,
        "empty_rooms": empty_rooms
    }

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
