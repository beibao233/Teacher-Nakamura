import string
from zhon.hanzi import punctuation


def remPunc(text):
    for Puncs in string.punctuation:
        text = text.replace(Puncs, '')
    for Puncs in punctuation:
        text = text.replace(Puncs, '')
    return text
