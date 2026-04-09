from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# Voters
cursor.execute("""
CREATE TABLE IF NOT EXISTS voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    username TEXT UNIQUE,
    password TEXT,
    has_voted INTEGER DEFAULT 0
)
""")



# Candidates
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    party TEXT
)
""")

# Votes
cursor.execute("""
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voter_id INTEGER,
    candidate_id INTEGER
)
""")

# System Control (⚠️ THIS MUST BE BEFORE CLOSE)
cursor.execute("""
CREATE TABLE IF NOT EXISTS system_control (
    id INTEGER PRIMARY KEY,
    voting_open INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO system_control (id, voting_open)
VALUES (1, 1)
""")

# ✅ CLOSE ONLY AT END
conn.commit()
conn.close()

print("DB Ready")
# from database import get_connection

# conn = get_connection()
# cursor = conn.cursor()

# # Voters
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS voters (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     age INTEGER,
#     username TEXT UNIQUE,
#     password TEXT,
#     has_voted INTEGER DEFAULT 0
# )
# """)

# # Admin
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS admin (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE,
#     password TEXT
# )
# """)

# # Candidates
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS candidates (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     party TEXT
# )
# """)

# # Votes
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS votes (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     voter_id INTEGER,
#     candidate_id INTEGER
# )
# """)

# conn.commit()
# conn.close()

# print("DB Ready")

# # System control (for voting status)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS system_control (
#     id INTEGER PRIMARY KEY,
#     voting_open INTEGER
# )
# """)

# # Insert default (voting open)
# cursor.execute("""
# INSERT OR IGNORE INTO system_control (id, voting_open)
# VALUES (1, 1)
# """)