import sqlite3
from sqlite3 import Connection, Cursor

import pandas as pd

from collect_data import collect_data
from utils import configure_database, store_data


class BoardGameManager:
    """
    Represents a board game collection manager that handles all database functions.
    """
    def __init__(self):
        self.database = 'boardgames.db'

    def collect_data(self, filename: str) -> None:
        """
        Loops through board games in the csv and adds each to the database with its attributes.
        """
        # create database and tables
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        configure_database(conn, cursor)

        # add board games and other data
        file_data = pd.read_csv(filename)
        for game_id in pd.Series(file_data['objectid']):
            game_data, attributes = collect_data(game_id)
            store_data(game_data, attributes, conn, cursor)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def new_entry(self):
        pass

    def query_data(self):
        pass

    def update_entry(self):
        pass

    def delete_entry(self):
        pass

    def export_data_as_csv(self):
        pass

