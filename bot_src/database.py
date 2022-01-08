"""
Database for the bot
"""
from sqlalchemy import create_engine
from sqlalchemy import Float, String, MetaData, Table, Integer, Column


class SQLiteDatabase(object):
    """
    sqlite db utility to ease working with the bot
    """
    def __init__(self, db_path='sqlite:///bot.db', initiate=False):
        self.engine = create_engine(db_path, echo=True)
        self.conn = self.engine.connect()
        self.meta = MetaData()
        # TODO: name is becoming id here, so we need discord_Id and username fields separately now
        # TODO: so that we can show them on ui
        self.discord_users = Table(
            'discord_users', self.meta,
            Column('id', Integer, primary_key=True),
            # discord user nickname
            Column('name', String),
            # discord user id, used to fetch users, can't get nickname with this
            Column('uid', Integer),
            Column('balance', Float(precision=10)),
        )

        if initiate:
            self.initiate()

    def initiate(self):
        """
        CREATE TABLE discord_users (
            id INTEGER NOT NULL,
            name VARCHAR,
            uid INTEGER,
            balance FLOAT,
            PRIMARY KEY (id)
        )
        COMMIT
        :return: None
        """
        self.meta.create_all(self.engine)

    def insert_users(self, user_list: list):
        """
        create users using this command:
        INSERT INTO discord_users (name, balance) VALUES (?, ?)
        (('KiLJ4EdeN', 1000.0), ('Insane', 1111.0), ('Rippah', 0.0), ('mr np', 40000000.0))
        COMMIT
        :return: None
        """
        # TODO: check names here of there are duplicates throw an error
        self.conn.execute(self.discord_users.insert(),
                          user_list)

    def fetch_all(self):
        """
        SELECT discord_users.id, discord_users.name, discord_users.uid, discord_users.balance
        FROM discord_users
        :return: result of the query
        """
        cmd = self.discord_users.select()
        result = self.conn.execute(cmd)
        return result

    def fetch_user_balance(self, user_id):
        """
        SELECT discord_users.id, discord_users.name, discord_users.uid, discord_users.balance
        FROM discord_users
        WHERE discord_users.uid = ?
        (12,)
        :return: user balance
        """
        cmd = self.discord_users.select().where(self.discord_users.c.uid == user_id)
        result = self.conn.execute(cmd)
        return result.first().balance

    def update_user_balance(self, user_id, value: float):
        """
        UPDATE discord_users SET balance=? WHERE discord_users.uid = ?
        (0.0, 12)
        COMMIT
        :return: None
        """
        cmd = self.discord_users.update().where(self.discord_users.c.uid == user_id).values(balance=value)
        self.conn.execute(cmd)
        return

    def drop_user(self, user_id):
        """
        DELETE FROM discord_users WHERE discord_users.uid = ?
        (12,)
        :return: None
        """
        cmd = self.discord_users.delete().where(self.discord_users.c.uid == user_id)
        result = self.conn.execute(cmd)
        return


# if __name__ == '__main__':
#     db = SQLiteDatabase(initiate=False)
    # insertion
    # db.insert_users(user_list=[{'uid': 12, 'name':'KiLJ4EdeN', 'balance': 1000},
    #                            {'uid': 13, 'name':'Insane', 'balance': 1111},
    #                            {'uid': 14, 'name':'Rippah', 'balance': 0},
    #                            {'uid': 15, 'name':'mr np', 'balance': 40000000},
    #                            ])
    # fetching all
    # res = db.fetch_all()
    # for row in res:
    #     print(row)
    # fetchone
    # bal = db.fetch_user_balance(user_id=12)
    # print(bal)
    # updates
    # db.update_user_balance(user_id=12, value=0)
    # bal = db.fetch_user_balance(user_id=12)
    # print(bal)
    # dropping
    # db.drop_user(user_id=12)
    # must throw error
    # bal = db.fetch_user_balance(user_id=12)
    # print(bal)
