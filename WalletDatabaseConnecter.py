from orm_models.db_session import global_init, create_session
from orm_models.WalletModel import Wallet


class WalletDatabaseConnecter:
    def __init__(self):
        global_init("players_data/Wallets.db")
        self.db_sess = create_session()

    def player_is_exist(self, player_name):
        if self.execute_player_orm_object(player_name):
            return True
        return False

    def execute_player_balance(self, player_name):
        if not self.player_is_exist(player_name):
            return -1
        player = self.execute_player_orm_object(player_name)
        return player.execute_balance()

    def add_player(self, player_name, start_balance):
        self.db_sess = create_session()
        if not self.player_is_exist(player_name):
            wallet = Wallet(
                player_name=player_name,
                balance=start_balance
            )
            self.db_sess.add(wallet)
            self.db_sess.commit()

    def save_to_player_balance(self, player_name, new_balance):
        self.db_sess = create_session()
        player = self.execute_player_orm_object(player_name)
        player.balance = new_balance
        self.db_sess.commit()

    def execute_player_orm_object(self, player_name):
        return self.db_sess.query(Wallet).filter(Wallet.player_name == player_name).first()


dbc = WalletDatabaseConnecter()
print(dbc.player_is_exist('Test'))
dbc.add_player('Test', 1000)
print(dbc.execute_player_balance('Test'))
dbc.save_to_player_balance('Test', 1005)
print(dbc.execute_player_balance('Test'))
dbc.save_to_player_balance('Test', 1010)
print(dbc.execute_player_balance('Test'))
dbc.save_to_player_balance('Test', 1020)
print(dbc.execute_player_balance('Test'))
