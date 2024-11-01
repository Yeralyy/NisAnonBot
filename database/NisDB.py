import sqlite3
import os.path

class NisDB():
    def __init__(self, database="nis.db"):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "nis.db")
        self.con = sqlite3.connect(database=db_path)
        self.cur = self.con.cursor()

    # save data to db
    def save_data(
            self,
            user_id,
            name,
            parallel,
            group,
            sub=0,
            is_admin=0
    ) -> bool:
        with self.con:
            try:
                self.cur.execute(
                        '''INSERT INTO users 
                        ("telegram_id", "name", "parallel", "group", "admin", "sub")
                        VALUES(?, ?, ?, ?, ?, ?)''', (
                            user_id, 
                            name, 
                            parallel, 
                            group, 
                            is_admin,
                            sub
                            )
                            )
                print(f"[INFO] Succefully saved data for {user_id}")            
                return True
            except Exception:
                print(f"[INFO] Failed saving data for {user_id}")
                return False

    # update data
    def update_data(
        self,
        user_id,
        name,
        parallel,
        group
    ) -> bool:
        with self.con:
            try:
                self.cur.execute(
                    '''UPDATE users SET name = ?, parallel = ?, group = ? WHERE telegram_id = ?''',
                    (name, parallel, group, user_id)
                )
                print(f"[INFO] Succefully updated data for {user_id}")       
                return True
            except Exception:
                print(f"[INFO] Failed updating data for {user_id}")
                return False    


    def is_user_in_db(self, user_id):  
        with self.con:
            try:
                if self.cur.execute('''SELECT 1 FROM users WHERE telegram_id = ?''', (user_id,)).fetchone() is not None:
                    return True
                else:
                    return False
            except Exception as ex:
                return False

    def is_user_admin(self, user_id):
        with self.con:
            try: 
                res = (self.cur.execute('''SELECT admin FROM users WHERE telegram_id = ?''', (user_id,)).fetchall())
                if res == [(1, )]:
                    return True
                else:
                    return False    
            except Exception as ex:
                print(f"[DB EXCEPTION] {ex}")
                return False

    # Fetch all grades
    def get_grades(self):
        with self.con:
            try:
                return self.cur.execute(
                    '''SELECT DISTINCT "group" 
                    FROM users 
                    WHERE "group" IS NOT NULL 
                    ORDER BY parallel'''
                ).fetchall()
            except Exception as ex:
                print(f"[ERROR DB] Failed to fetch grades: {ex}")
                return []  # Optionally return an empty list on error

    def get_peoples_by_grade(self, grade, user_id):
        with self.con:
            try:
                return self.cur.execute(
                    '''SELECT name FROM users
                    WHERE "group"=? AND telegram_id != ?''', (grade, user_id,)
                ).fetchall()
            except Exception as ex:
                print(f"[ERROR DB] Failed to fetch people by grade: {ex}")
                return []  # Optionally return an empty list on error

    def get_person(self, person):
        with self.con:
            try:
                return self.cur.execute(
                    '''SELECT telegram_id FROM users
                    WHERE name=?''', (person,)
                ).fetchall()
            except Exception as ex:
                print(ex)
                
    def get_person_by_id(self, id: int):
        with self.con:
            try:
                return self.cur.execute(
                    '''SELECT name FROM users WHERE telegram_id=?''',
                    (id,)
                ).fetchall()[0]
            except Exception as ex:
                print(ex)
                return False
    def fetchall_grade_users(self, grade):
        with self.con:
            try:
                return self.cur.execute('''SELECT telegram_id FROM users WHERE "group"=?''', (grade,)).fetchall()
            except Exception as ex:
                print(ex)
                return False

    def fetchall_group_students(self, grade):
        with self.con:
            try:
                return self.cur.execute('''SELECT name FROM users WHERE "group"=?''', (grade,)).fetchall()
            except Exception as ex:
                print(ex)
                return False
    def fetchall_users(self):
        with self.con:
            try:
                return self.cur.execute('''SELECT telegram_id FROM users''').fetchall()
            except Exception as ex:
                print(ex)