import sqlite3


db_file = ('DB_FILE')


class ConnectionClosure:
    def __init__(self):
        self.connect = sqlite3.connect("Database.db")
        self.cursor = self.connect.cursor()

    def close(self):
        self.connect.close()


class CreateDatabase(ConnectionClosure):
    def __init__(self):
        super().__init__()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS User(
                        id INTEGER PRIMARY KEY,
                        message TEXT,
                        total_gpt_tokens INTEGER,
                        tts_symbols INTEGER,
                        stt_blocks INTEGER)""")
        self.connect.commit()

    def check_user_exists(self, user_id):
        self.cursor.execute(
            "SELECT id FROM User "
            "WHERE id = ? ",
            (user_id,))
        data = self.cursor.fetchone()
        return data is not None

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO User VALUES(?, ?, ?, ?, ?);",
                            (user_id, '', 1500, 1500, 1))
        self.connect.commit()


class MessageAdd(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def message_select(self, user_id):
        self.cursor.execute("SELECT message FROM User WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Unknown error!'
        return result

    def add_message(self, text_promt, user_id):
        self.cursor.execute("UPDATE User SET message = ? WHERE id = ?", (text_promt, user_id))
        self.connect.commit()


class MessageInfo(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def select_message(self, id):
        self.cursor.execute(f"SELECT message FROM User WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if not row[0]:
            return
        else:
            return row[0]


class TotalGptTokensAdd(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def total_gpt_tokens_select(self, user_id):
        self.cursor.execute("SELECT total_gpt_tokens FROM User WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Unknown error!'
        return result

    def add_total_gpt_tokens(self, tokens, user_id):
        self.cursor.execute("UPDATE User SET total_gpt_tokens = ? WHERE id = ?", (tokens, user_id))
        self.connect.commit()


class TotalGptTokensInfo(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def total_gpt_tokens_user(self, id):
        self.cursor.execute(f"SELECT total_gpt_tokens FROM User WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if not row[0]:
            return
        else:
            return row[0]


class TtsSymbolsAdd(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def tts_symbols_select(self, user_id):
        self.cursor.execute("SELECT tts_symbols FROM User WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Unknown error!'
        return result

    def add_tts_symbols(self, symbols, user_id):
        self.cursor.execute("UPDATE User SET tts_symbols = ? WHERE id = ?", (symbols, user_id))
        self.connect.commit()


class TtsSymbolsInfo(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def tts_symbols_user(self, id):
        self.cursor.execute(f"SELECT tts_symbols FROM User WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if not row[0]:
            return
        else:
            return row[0]


class SttBlocksAdd(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def stt_blocks_select(self, user_id):
        self.cursor.execute("SELECT stt_blocks FROM User WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Unknown error!'
        return result

    def add_stt_blocks(self, blocks, user_id):
        self.cursor.execute("UPDATE User SET stt_blocks = ? WHERE id = ?", (blocks, user_id))
        self.connect.commit()


class SttBlocksInfo(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def stt_blocks_user(self, id):
        self.cursor.execute(f"SELECT stt_blocks FROM User WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if not row[0]:
            return
        else:
            return row[0]


class tokens_user(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def tts_symbols_user(self, id):
        self.cursor.execute(f"SELECT tts_symbols FROM User WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if not row[0]:
            return
        else:
            return row[0]


class tokens_add(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def tts_symbols(self, id):
        self.cursor.execute("SELECT id, tts_symbols FROM User WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Ошибка, при запросе к БД.'
        return result

    def add_tts_symbols(self, tokens, user_id):
        self.cursor.execute("UPDATE User SET tts_symbols = ? WHERE id = ?", (tokens, user_id))
        self.connect.commit()


class message_add(ConnectionClosure):
    def __init__(self):
        super().__init__()

    def text_add(self, id):
        self.cursor.execute("SELECT id, message FROM User WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Ошибка, при запросе к БД.'
        return result

    def add_text(self, text, user_id):
        self.cursor.execute("UPDATE User SET message = ? WHERE id = ?", (text, user_id))
        self.connect.commit()