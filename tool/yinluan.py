import random
import jieba
import jieba.posseg as pseg

jieba.setLogLevel(20)


def wordchage(x, y, yinld):
    if random.random() > yinld:
        return x
    if x in {'，', '。'}:
        return '……'
    if x in {'!', '！'}:
        return '❤'
    if len(x) > 1 and random.random() < 0.5:
        return f'{x[0]}……{x}'
    else:
        if y == 'n' and random.random() < 0.5:
            x = '〇' * len(x)
        return f'……{x}'


def chs2yin(s, yinld=0.5):
    # return ''.join([wordchage(x, y, yinld) for x, y in pseg.cut(s)])
    return s
