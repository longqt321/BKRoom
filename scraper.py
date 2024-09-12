import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
response = requests.get("http://cb.dut.udn.vn/PageCNPhongHoc.aspx")

if response.status_code != 200:
    print(f"Failed to fetch data: {response.status_code}")  # Debug print
    sys.exit(1)

hours = {
    1: '7h00',
    2: '8h00',
    3: '9h00',
    4: '10h00',
    5: '11h00',
    6: '12h30',
    7: '13h30',
    8: '14h30',
    9: '15h30',
    10: '16h30',
    11: '17h30'
}

periods = {
    '07h00': 1,
    '08h00': 2,
    '09h00': 3,
    '10h00': 4,
    '11h00': 5,
    '12h30': 6,
    '13h30':7,
    '14h30': 8,
    '15h30': 9,
    '16h30': 10,
    '17h30': 11
}

param = {
    'id' : 'ctrCNPhongHoc_Grid'
}

my_dict = {}

# Neu time_slot > 16h30 thi code co the bi sai vi gio hoc cuoi cung la 17h30
def find_empty_rooms(time_slot):
    # Convert input time slot to datetime.time object
    time_slot = datetime.strptime(time_slot, "%Hh%M").time()

    empty_rooms = []

    for room, times in my_dict.items():
        for i in range(len(times) - 1):
            # If time_slot is between two consecutive times, add room to empty_rooms
            start = times[i].strftime("%Hh%M")
            end = times[i + 1].strftime("%Hh%M")
            if periods[end] - periods[start] == 1 and times[i] <= time_slot < times[i + 1]:
                empty_rooms.append(room)
                break  # No need to check the rest of the times

    return empty_rooms


if response.status_code == 200:
    soup = BeautifulSoup(response.text,'html.parser')
    print(soup)
    table = soup.find('table',param)
    trs = table.find_all('tr',{'class' : 'GridRow'})
    for tr in trs:
        room = tr.find('td').text.split('Số')[0]
        tds = tr.find_all('td',{'class' : 'GridCellC'})
        p = 1
        h = []
        for td in tds:
            if 'colspan' in td.attrs:
                colspan_value = td['colspan']
                p = p + int(colspan_value)
            else:
                if p <= 11:
                    time_object = datetime.strptime(hours[p], "%Hh%M").time()
                    h.append(time_object)
                p = p + 1
        if '(' in room:
            room = room[:-3]
        my_dict[room] = h
else:
    print("Error!")

print(f"Scraped data: {my_dict}")
data = find_empty_rooms("7h00")
print(f"Log of scraper: {data}")
