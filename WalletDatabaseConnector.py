import sqlite3


class WalletDatabaseConnector:
    def __init__(self):
        self.database_file_path = "players_data/Wallets.db"

    def execute_player_balance(self, player_name):
        connector, cursor = self.connect_database()

        balance = cursor.execute(f"SELECT balance FROM wallets WHERE player_name == '{player_name}'").fetchall()
        connector.close()

        if balance:
            return balance[0][0]
        else:
            return -1

    def save_player_balance(self, player_name, new_player_balance):
        connector, cursor = self.connect_database()

        cursor.execute(f'UPDATE wallets SET balance == {new_player_balance} WHERE player_name == "{player_name}"')
        self.commit_and_close(connector)

    def add_player(self, player_name, start_balance):
        connector, cursor = self.connect_database()

        if self.execute_player_balance(player_name):
            return

        cursor.execute(f'INSERT INTO wallets(player_name, balance) VALUES("{player_name}", {start_balance})')
        self.commit_and_close(connector)

    def connect_database(self):
        connector = sqlite3.connect(self.database_file_path)
        cursor = connector.cursor()
        return connector, cursor

    def commit_and_close(self, connector):
        connector.commit()
        connector.close()


connect = WalletDatabaseConnector()
print(connect.execute_player_balance('Test'))
connect.add_players('f', 1000)
print(connect.execute_player_balance('f'))
