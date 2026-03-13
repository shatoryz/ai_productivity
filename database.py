import sqlite3
import threading


class Database:
    def __init__(self, db_path='ai_productivity.db'):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS schedule(
                id INTEGER PRIMARY KEY, user_id INTEGER, activity TEXT, category TEXT,
                start_time TEXT, end_time TEXT, difficulty REAL, priority REAL,
                last_time REAL, day_of_week INTEGER, estimated_duration INTEGER,
                scheduled_date TEXT)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS activity_history(
                id INTEGER PRIMARY KEY, user_id INTEGER, category TEXT, time_spent REAL,
                last_time REAL, date TEXT, activity_name TEXT)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS recommendation_history(
                id INTEGER PRIMARY KEY, user_id INTEGER, activity TEXT, category TEXT,
                score REAL, factors TEXT, timestamp REAL, accepted INTEGER,
                scheduled_time TEXT, actual_time_spent REAL, completed INTEGER,
                feedback_score REAL, context_data TEXT)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS user_coefficients(
                id INTEGER PRIMARY KEY, user_id INTEGER,
                w_eyes REAL, w_blink REAL, w_pose REAL,
                w_S REAL, w_E REAL, w_P REAL, w_C REAL,
                t_max_eyes REAL, f_opt_blink REAL,
                sigma_time REAL, cooldown_tau REAL,
                alpha_S REAL, alpha_E REAL, alpha_P REAL,
                history_size INTEGER,
                alpha REAL DEFAULT 0.1,
                gamma REAL DEFAULT 0.15)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS factor_history(
                id INTEGER PRIMARY KEY, user_id INTEGER,
                S_value REAL, E_value REAL, P_value REAL, C_value REAL,
                timestamp REAL, session_id TEXT)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS session_productivity(
                id INTEGER PRIMARY KEY, user_id INTEGER, session_id TEXT,
                productivity REAL, timestamp REAL)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS trend_history(
                id INTEGER PRIMARY KEY, user_id INTEGER,
                productivity REAL, trend REAL, score_trend REAL,
                timestamp REAL, session_id TEXT)''')
            conn.commit()
            conn.close()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        return conn


db = Database()
