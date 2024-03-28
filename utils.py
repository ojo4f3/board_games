from sqlite3 import Connection, Cursor

table_creation_commands = [
    '''CREATE TABLE IF NOT EXISTS BoardGames (
            id INTEGER PRIMARY KEY,
            name VARCHAR(150),
            expands INTEGER,
            yearpublished INTEGER,
            rank INTEGER,
            average FLOAT,
            avgweight FLOAT,
            minplayers INTEGER,
            maxplayers INTEGER,
            minplaytime INTEGER,
            maxplaytime INTEGER,
            minage INTEGER,
            short_description VARCHAR(1000),
            canonical_link VARCHAR(250)
        );''',
    '''CREATE TABLE IF NOT EXISTS Designers (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)
        );''',
    '''CREATE TABLE IF NOT EXISTS Artists (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)
        );''',
    '''CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)
        );''',
    '''CREATE TABLE IF NOT EXISTS Mechanics (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)
        );''',
    '''CREATE TABLE IF NOT EXISTS Families (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)
        );''',
    '''CREATE TABLE IF NOT EXISTS BoardGamesDesigners (
            game_id INTEGER,
            designer_id INTEGER,
            FOREIGN KEY (game_id) REFERENCES BoardGames(id),
            FOREIGN KEY (designer_id) REFERENCES Designers(id)
        );''',
    '''CREATE TABLE IF NOT EXISTS BoardGamesArtists (
            game_id INTEGER,
            artist_id INTEGER,
            FOREIGN KEY (game_id) REFERENCES BoardGames(id),
            FOREIGN KEY (artist_id) REFERENCES Artists(id)
        );''',
    '''CREATE TABLE IF NOT EXISTS BoardGamesCategories (
            game_id INTEGER,
            category_id INTEGER,
            FOREIGN KEY (game_id) REFERENCES BoardGames(id),
            FOREIGN KEY (category_id) REFERENCES Categories(id)
        );''',
    '''CREATE TABLE IF NOT EXISTS BoardGamesMechanics (
            game_id INTEGER,
            mechanic_id INTEGER,
            FOREIGN KEY (game_id) REFERENCES BoardGames(id),
            FOREIGN KEY (mechanic_id) REFERENCES Mechanics(id)
        );''',
    '''CREATE TABLE IF NOT EXISTS BoardGamesFamilies (
            game_id INTEGER,
            family_id INTEGER,
            FOREIGN KEY (game_id) REFERENCES BoardGames(id),
            FOREIGN KEY (family_id) REFERENCES Families(id)
        );'''
]


def configure_database(conn: Connection, cursor: Cursor):
    # Create all 11 tables
    for command in table_creation_commands:
        cursor.execute(command)


def store_data(game_data: list, game_attributes: list, conn: Connection, cursor: Cursor) -> None:
    """

    """
    # Add the board game into BoardGames
    insert_statement = f'''INSERT OR REPLACE INTO BoardGames (
    id, name, expands, yearpublished, rank, average, avgweight, minplayers, maxplayers, minplaytime, maxplaytime, 
    minage, short_description, canonical_link
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(insert_statement, tuple(game_data))
    print(f"{game_data[1]} was added to the BoardGames table.")

    # Add category attributes and link to the board game
    for index, attributes in enumerate(game_attributes):
        add_and_link_attributes(game_data[0], index, attributes, cursor)


def add_and_link_attributes(game_id: int, category: int, attributes: list, cursor: Cursor) -> None:
    table_dict = {0: 'Designers', 1: 'Artists', 2: 'Categories', 3: 'Mechanics', 4: 'Families'}
    id_dict = {0: 'designer_id', 1: 'artist_id', 2: 'category_id', 3: 'mechanic_id', 4: 'family_id'}

    # Insert each mechanic into Mechanics table if not already present and link to the board game
    for attribute in attributes:
        cursor.execute(f"INSERT OR IGNORE INTO {table_dict[category]} (name) VALUES (?)", (attribute,))
        cursor.execute(f"SELECT id FROM {table_dict[category]} WHERE name = (?)", (attribute,))
        attr_id = cursor.fetchone()[0]
        cursor.execute(f"INSERT INTO BoardGames{table_dict[category]} (game_id, {id_dict[category]}) VALUES (?, ?)", (game_id, attr_id))
