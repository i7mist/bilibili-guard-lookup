from flask import Flask
import requests
from flask_table import Table, Col

app = Flask(__name__)


class ItemTable(Table):
    username = Col('username')
    uid = Col('uid')
    medal_name = Col('medal_name')
    medal_level = Col('medal_level')


class Item(object):
    def __init__(self, username, uid, medal_name, medal_level):
        self.username = username
        self.uid = uid
        self.medal_name = medal_name
        self.medal_level = medal_level


@app.route("/")
def hello_world():
    URL = "https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList"
    PARAMS = {"roomid": 128308, "page": 1, "ruid": 941228, "page_size": 29}
    r = requests.get(url=URL, params=PARAMS)
    r_json = r.json()
    total_page_count = r_json["data"]["info"]["page"]
    guard_list = []
    for page in range(1, total_page_count + 1):
        PARAMS["page"] = page
        r = requests.get(url=URL, params=PARAMS)
        r_json = r.json()
        guard_list.extend(r_json["data"]["list"])
    items = []
    for guard in guard_list:
        items.append(Item(guard["username"], guard["uid"], guard["medal_info"]["medal_name"],
                          guard["medal_info"]["medal_level"]))
    table = ItemTable(items)

    return table.__html__()
