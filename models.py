import sqlite3
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

# -------- VOTER --------
def register_voter(name, age, username, password, sec_question, sec_answer):
    if not name or not username or not password or not sec_question or not sec_answer:
        return "All fields required"

    if age < 18:
        return "Underage"

    hashed_pw = generate_password_hash(password)
    sec_answer_sanitized = sec_answer.strip().lower()

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO voters (name, age, username, password, security_question, security_answer) VALUES (?, ?, ?, ?, ?, ?)",
                (name, age, username, hashed_pw, sec_question, sec_answer_sanitized)
            )
            conn.commit()
            return "Success"
    except sqlite3.IntegrityError:
        return "Username already exists"
    except Exception as e:
        return f"Database error: {str(e)}"

def login_voter(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM voters WHERE username=?",
            (username,)
        )
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            return user
        return None


# -------- ADMIN --------
def login_admin(username, password):
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "voteradmin123"

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    else:
        return None


# -------- CANDIDATE --------
def add_candidate(name, party):
    if not name.strip() or not party.strip():
        return False
        
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO candidates (name, party) VALUES (?, ?)",
            (name.strip(), party.strip())
        )
        conn.commit()
        return True

def get_candidates():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM candidates")
        return cursor.fetchall()

def delete_candidate(candidate_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates WHERE id=?", (candidate_id,))
        conn.commit()


# -------- VOTING --------
def cast_vote(voter_id, candidate_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT has_voted FROM voters WHERE id=?", (voter_id,))
        voter = cursor.fetchone()
        
        if voter['has_voted'] == 1:
            return "Already voted"

        cursor.execute(
            "INSERT INTO votes (voter_id, candidate_id) VALUES (?, ?)",
            (voter_id, candidate_id)
        )

        cursor.execute(
            "UPDATE voters SET has_voted=1 WHERE id=?",
            (voter_id,)
        )

        conn.commit()
        return "Success"


def is_voting_open():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT voting_open FROM system_control WHERE id=1")
        result = cursor.fetchone()
        return result['voting_open'] == 1 if result else False


def set_voting_status(status):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE system_control SET voting_open=? WHERE id=1",
            (status,)
        )
        conn.commit()


# -------- RESULTS --------
def get_results():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT candidates.name, COUNT(votes.id)
        FROM candidates
        LEFT JOIN votes ON candidates.id = votes.candidate_id
        GROUP BY candidates.name
        """)
        return cursor.fetchall()

def get_winner():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT candidates.name, COUNT(votes.id) as total
        FROM candidates
        LEFT JOIN votes ON candidates.id = votes.candidate_id
        GROUP BY candidates.name
        ORDER BY total DESC
        LIMIT 1
        """)
        return cursor.fetchone()

def get_voters():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, age, username, has_voted FROM voters")
        return cursor.fetchall()


# -------- NEW FEATURE --------
def get_user_vote(voter_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT candidates.name
        FROM votes
        JOIN candidates ON votes.candidate_id = candidates.id
        WHERE votes.voter_id=?
        """, (voter_id,))
        return cursor.fetchone()
# from database import get_connection

# # -------- VOTER --------
# def register_voter(name, age, username, password):
#     if not name or not username or not password:
#         return "All fields required"

#     if age < 18:
#         return "Underage"

#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute(
#             "INSERT INTO voters (name, age, username, password) VALUES (?, ?, ?, ?)",
#             (name, age, username, password)
#         )
#         conn.commit()
#         return "Success"
#     except:
#         return "Username already exists"


# def login_voter(username, password):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT * FROM voters WHERE username=? AND password=?",
#         (username, password)
#     )

#     return cursor.fetchone()


# # -------- ADMIN --------
# def login_admin(username, password):
#     ADMIN_USERNAME = "admin"
#     ADMIN_PASSWORD = "voteradmin123"

#     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#         return True
#     else:
#         return None


# # -------- CANDIDATE --------
# def add_candidate(name, party):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO candidates (name, party) VALUES (?, ?)",
#         (name, party)
#     )
#     conn.commit()


# def get_candidates():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM candidates")
#     return cursor.fetchall()


# def delete_candidate(candidate_id):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM candidates WHERE id=?", (candidate_id,))
#     conn.commit()


# # -------- VOTING --------
# def cast_vote(voter_id, candidate_id):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT has_voted FROM voters WHERE id=?", (voter_id,))
#     if cursor.fetchone()[0] == 1:
#         return "Already voted"

#     cursor.execute(
#         "INSERT INTO votes (voter_id, candidate_id) VALUES (?, ?)",
#         (voter_id, candidate_id)
#     )

#     cursor.execute(
#         "UPDATE voters SET has_voted=1 WHERE id=?",
#         (voter_id,)
#     )

#     conn.commit()
#     return "Success"


# def is_voting_open():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT voting_open FROM system_control WHERE id=1")
#     return cursor.fetchone()[0] == 1


# def set_voting_status(status):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "UPDATE system_control SET voting_open=? WHERE id=1",
#         (status,)
#     )
#     conn.commit()


# # -------- RESULTS --------
# def get_results():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     SELECT candidates.name, COUNT(votes.id)
#     FROM candidates
#     LEFT JOIN votes ON candidates.id = votes.candidate_id
#     GROUP BY candidates.name
#     """)

#     return cursor.fetchall()


# def get_winner():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     SELECT candidates.name, COUNT(votes.id) as total
#     FROM candidates
#     LEFT JOIN votes ON candidates.id = votes.candidate_id
#     GROUP BY candidates.name
#     ORDER BY total DESC
#     LIMIT 1
#     """)

#     return cursor.fetchone()


# def get_voters():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT id, name, age, username, has_voted FROM voters")
#     return cursor.fetchall()


# # -------- NEW FEATURE --------
# def get_user_vote(voter_id):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     SELECT candidates.name
#     FROM votes
#     JOIN candidates ON votes.candidate_id = candidates.id
#     WHERE votes.voter_id=?
#     """, (voter_id,))

#     return cursor.fetchone()