import httpx
import ast


def getqqname(qq):
    r = httpx.get("https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={}".format(qq))
    r.encoding = 'GBK'
    try:
        name = ast.literal_eval(r.text.replace("portraitCallBack(", "")[:-1])[str(qq)][6]
    except KeyError:
        name = ""
    if name.strip() == "":
        name = "空"
    return name


def isaqqnum(i):
    i = i.strip()
    if i[0] == "@" and i.replace("@", "").isdigit() == True:
        return getqqname(i.replace("@", ""))
    else:
        return False
