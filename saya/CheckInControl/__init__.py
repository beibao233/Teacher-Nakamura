import ast
import time

checkinlist = {}
data = {}


def checkInAction(action, key, num):
    data = {}
    if action == "delete":
        data["ltime"] = checkinlist[key]["ltime"]
        data['timestrip'] = checkinlist[key]['timestrip']
        data['num'] = checkinlist[key]['num'] - num
        data['name'] = checkinlist[key]['name']
        data['day'] = checkinlist[key]['day']
        checkinlist[key] = data
        with open("checkin.txt", "w+", encoding="utf-8") as f:
            f.write(str(checkinlist))
    elif action == "add":
        data["ltime"] = checkinlist[key]["ltime"]
        data['timestrip'] = checkinlist[key]['timestrip']
        data['num'] = checkinlist[key]['num'] + num
        data['name'] = checkinlist[key]['name']
        data['day'] = checkinlist[key]['day']
        checkinlist[key] = data
        with open("checkin.txt", "w+", encoding="utf-8") as f:
            f.write(str(checkinlist))
    return checkinlist


def checkIn(key, name):
    if key in checkinlist:
        if checkinlist[key]['day'] != time.strftime("%d", time.localtime(time.time())):
            data = {"ltime": time.strftime('%H:%M:%S', time.localtime(time.time())), 'timestrip': time.time(),
                    'num': checkinlist[key]['num'] + 1, 'name': name,
                    'day': time.strftime("%d", time.localtime(time.time()))}
            checkinlist[key] = data
            with open("checkin.txt", "w+", encoding="utf-8") as f:
                f.write(str(checkinlist))
            return checkinlist
        else:
            return "in"
    else:
        data = {}
        data["ltime"] = time.strftime('%H:%M:%S', time.localtime(time.time()))
        data['timestrip'] = time.time()
        data['num'] = 1
        data['name'] = name
        data['day'] = time.strftime("%d", time.localtime(time.time()))
        checkinlist[key] = data
        with open("checkin.txt", "w+", encoding="utf-8") as f:
            f.write(str(checkinlist))
        return checkinlist


def getMemberCheckData(qq):
    return checkinlist[qq]


def getCheckinList():
    return checkinlist


if checkinlist == {}:
    with open("checkin.txt", "w+", encoding="utf-8") as f:
        checkinlist = ast.literal_eval(f.read())
