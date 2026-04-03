import sqlite3

DBFILENAME = 'database.db'


def db_fetch(query, args=(), all=False, db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    conn.row_factory = sqlite3.Row 
    cur = conn.execute(query, args)
    
    if all:
      res = cur.fetchall()
      return [dict(e) for e in res] if res else [] 
    else:
      res = cur.fetchone()
      return dict(res) if res else None 
  return res


def db_insert(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.lastrowid


def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()


def db_update(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.rowcount
  



class EmergencyDB:
  
    def create_user(self, username, password):
            query = "INSERT INTO user (username, password) VALUES (?, ?)"
            return db_insert(query, (username, password))
  
    def get_user(self, username):
            query = "SELECT * FROM user WHERE username = ?"
            return db_fetch(query, (username,))
  

    def create_profile(self, user_id, condition, contact):
            query = "INSERT INTO emergency_profile (user_id, condition_name, emergency_contact) VALUES (?, ?, ?)"
            return db_insert(query, (user_id, condition, contact))

    def get_profile_by_username(self, username):
            query = """
                SELECT emergency_profile.* FROM emergency_profile 
                JOIN user ON user.id = emergency_profile.user_id 
                WHERE user.username = ?
            """
            return db_fetch(query, (username,))

    def add_instruction(self, profile_id, symptom, action):
            query = "INSERT INTO instructions (profile_id, symptom, action) VALUES (?, ?, ?)"
            return db_insert(query, (profile_id, symptom, action))

    def get_instructions(self, profile_id):
            query = "SELECT * FROM instructions WHERE profile_id = ?"
            return db_fetch(query, (profile_id,), all=True)

    def delete_instruction(self, instruction_id):
            query = "DELETE FROM instructions WHERE id = ?"
            return db_update(query, (instruction_id,))