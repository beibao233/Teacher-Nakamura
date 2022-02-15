import sqlite3
import atexit
from loguru import logger

udb = sqlite3.connect(f"{__file__.replace('__init__.py','')}database.db")
uc = udb.cursor()

try:
    uc.execute('''CREATE TABLE Member
           (UID          INT        PRIMARY KEY     NOT NULL,
           Name          TEXT                       NOT NULL,
           Gender        INT                        NOT NULL,
           Coins         INT                        NOT NULL,
           Level         INT                        NOT NULL,
           Favor         INT                        NOT NULL,
           Birthday      TEXT                       NOT NULL
           );''')
    udb.commit()
    logger.info("未检到用户数据表！已创建！")
except sqlite3.OperationalError:
    logger.info("用户数据表检查成功！")

# PRISM

mdb = sqlite3.connect(f"{__file__.replace('__init__.py','')}messages.db")
mc = mdb.cursor()


class Member:
    def __init__(self, uid: int, name: str, gender: int, birthday: str,
                 coins: int = 0, level: int = 0, favor: int = 0, save: bool = True):
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.uid = uid
        self.__coins = coins
        self.__level = level
        self.__favor = favor

        if save:
            uc.execute(f"INSERT INTO Member (UID,Name,Gender,Coins,Level,Favor,Birthday) \
                       VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (self.uid, self.name, self.gender, self.__coins,
                        self.__level, self.__favor, self.birthday))
            udb.commit()

    def get_coins(self):
        return self.__coins

    def add_coin(self, coins: int):
        self.__coins += coins
        uc.execute("UPDATE Member set Coins = ? where UID=?", (self.__coins, self.uid))
        udb.commit()

    def remove_coin(self, coins: int):
        self.__coins -= coins
        uc.execute("UPDATE Member set Coins = ? where UID=?", (self.__coins, self.uid))
        udb.commit()

    def level_up(self):
        self.__level += 1
        uc.execute("UPDATE Member set Level = ? where UID=?", (self.__coins, self.uid))
        udb.commit()

    def favor_up(self, favor: int):
        self.__favor += favor
        uc.execute("UPDATE Member set Favor = ? where UID=?", (self.__coins, self.uid))
        udb.commit()

    def favor_down(self, favor: int):
        self.__favor -= favor
        uc.execute("UPDATE Member set Favor = ? where UID=?", (self.__coins, self.uid))
        udb.commit()


class LoadMember(Member):
    def __init__(self, uid: int):
        self.__uid = uid
        if self.exist(self.__uid):
            for row in uc.execute("SELECT * FROM Member WHERE ?", (uid,)):
                super().__init__(uid=self.__uid, name=row[0], gender=row[1], coins=row[2], level=row[3], favor=row[4],
                                 birthday=row[5], save=False)

    @staticmethod
    def exist(uid):
        for row in uc.execute("SELECT * FROM Member WHERE ?", (uid,)):
            return True
        return False


class GroupsTable:
    def __init__(self, gid: str):
        self.__gid = gid
        mc.execute(f'''CREATE TABLE _{self.__gid}
               (MID INT PRIMARY KEY      NOT NULL,
               GName          TEXT       NOT NULL,
               UID            INT        NOT NULL,
               UName          TEXT       NOT NULL,
               Message        TEXT       NOT NULL
               );''')
        mdb.commit()


class Message(GroupsTable):
    def __init__(self, gid: int, gname: str, uid: int, uname: str, message: str):
        self.__gid = str(gid)
        self.__gname = gname
        self.__uid = uid
        self.__uname = uname
        self.__message = message

        try:
            self.__mid = mc.execute(f"SELECT COUNT(*) FROM _{self.__gid}").fetchone()[0] + 1

            mc.execute(f"INSERT INTO _{self.__gid} (MID,GName,UID,UName,Message) \
                               VALUES (?, ?, ?, ?, ?)",
                       (self.__mid, self.__gname, self.__uid, self.__uname, self.__message))
            mdb.commit()
        except sqlite3.OperationalError:
            super().__init__(self.__gid)

            self.__mid = mc.execute(f"SELECT COUNT(*) FROM _{self.__gid}").fetchone()[0] + 1

            mc.execute(f"INSERT INTO _{self.__gid} (MID,GName,UID,UName,Message) \
                                           VALUES (?, ?, ?, ?, ?)",
                       (self.__mid, self.__gname, self.__uid, self.__uname, self.__message))
            mdb.commit()


@atexit.register
def close_databases():
    udb.close()
    mdb.close()
