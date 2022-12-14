import sqlite3

class Database:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def futbolchi_kiritish(self,ismi,raqami,telefon_raqam,jamoa):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'futbolchilar'(ismi,raqami,telefon_raqam,jamoa) VALUES (?,?,?,?)",(ismi,raqami,telefon_raqam,jamoa,))

    def player_exists(self,ismi,raqami,telefon_raqam,jamoa):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'futbolchilar' WHERE ismi=? AND raqami=? AND telefon_raqam=? AND  jamoa=? ",(ismi,raqami,telefon_raqam,jamoa,)).fetchall()
            return bool(len(result))

    def delete_players(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM 'futbolchilar'")

    def get_player(self,ismi):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'futbolchilar' WHERE ismi = ? ",(ismi,)).fetchall()
