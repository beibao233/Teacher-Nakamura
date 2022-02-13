import sqlite3
import atexit

udb = sqlite3.connect(f"{__file__.replace('__init__.py','')}database.db")
uc = udb.cursor()

try:
    uc.execute('''CREATE TABLE Member
           (ID           INT        PRIMARY KEY     NOT NULL,
           Name          TEXT                       NOT NULL,
           Gender        INT                        NOT NULL,
           Coins         INT                        NOT NULL,
           Level         INT                        NOT NULL,
           Favor         INT                        NOT NULL,
           Birthday      INT                        NOT NULL
           );''')
    udb.commit()
    print("未检到用户数据表！已创建！")
except sqlite3.OperationalError:
    print("用户数据表检查成功！")

# PRISM

mdb = sqlite3.connect(f"{__file__.replace('__init__.py','')}messages.db")
mc = mdb.cursor()

try:
    mc.execute('''CREATE TABLE Messages
           (GID INT PRIMARY KEY      NOT NULL,
           GName          TEXT       NOT NULL,
           MID            INT        NOT NULL,
           MName          TEXT       NOT NULL,
           Message        TEXT       NOT NULL
           );''')
    mdb.commit()
    print("未检到群信息记录数据表！已创建！")
except sqlite3.OperationalError:
    print("群信息记录表检查成功！")


class Member:
    def __init__(self, name: str, gender: int, birthday: int,
                 coins: int = 0, level: int = 0, favor: int = 0, uid: int = None):
        self.__name = name
        self.__gender = gender
        self.__birthday = birthday
        if uid is None:
            self.__id = uc.execute("SELECT COUNT(*) FROM Member").fetchone()[0]+1
        else:
            self.__id = uid
        self.__coins = coins
        self.__level = level
        self.__favor = favor

        if uid is None:
            uc.execute(f"INSERT INTO Member (ID,Name,Gender,Coins,Level,Favor,Birthday) \
                       VALUES (?, ?, ?, ?, ?, ?)",
                       (self.__id, self.__name, self.__gender, self.__coins,
                        self.__level, self.__favor, self.__birthday))
            udb.commit()

    def add_coin(self, coins: int):
        self.__coins += coins
        uc.execute("UPDATE Member set Coins = ? where ID=?", (self.__coins, self.__id))
        udb.commit()

    def remove_coin(self, coins: int):
        self.__coins -= coins
        uc.execute("UPDATE Member set Coins = ? where ID=?", (self.__coins, self.__id))
        udb.commit()

    def level_up(self):
        self.__level += 1
        uc.execute("UPDATE Member set Level = ? where ID=?", (self.__coins, self.__id))
        udb.commit()

    def favor_up(self, favor: int):
        self.__favor += favor
        uc.execute("UPDATE Member set Favor = ? where ID=?", (self.__coins, self.__id))
        udb.commit()

    def favor_down(self, favor: int):
        self.__favor -= favor
        uc.execute("UPDATE Member set Favor = ? where ID=?", (self.__coins, self.__id))
        udb.commit()


class LoadMember(Member):
    def __int__(self, uid: int):
        uds = uc.execute("SELECT Name, Gender, Birthday, Coins, Level, Favor, ID  from Member")
        ud = uds[uid-1]
        super().__init__(name=ud[0], gender=ud[1], birthday=ud[2], coins=ud[4], level=ud[5], favor=ud[6], uid=ud[7])


@atexit.register
def close_databases():
    udb.close()
    mdb.close()
