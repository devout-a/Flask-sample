import json
from pathlib import Path

db_file = Path(__file__).parent.parent / "database" / "data.json"


class Usermanager:
    def __init__(self):
        self.db = self.load_db()

    def load_db(self):
        if db_file.exists():
            with open(db_file, "r") as file:
                return json.load(file)
        return {}
    
    def save_db(self):
        with open(db_file, "w") as file:
            json.dump(self.db, file, indent=2)
    
    def register(self, user, password):
        if user in self.db:
            return False
        self.db[user] = {
            "password": password,
            "tasks": [],
            "finished": [],
            "journals": [],
            }
        self.save_db()
        return True

    def authenticate(self, user, password):
        if user in self.db and password == self.db[user]["password"]:
            return True
        return False
    
    def user_data(self, user):
        self.db = self.load_db()
        user_record = self.db.get(user)
        if not user_record:
            return None

        return {
            "tasks": user_record.get("tasks", []),
            "finished": user_record.get("finished", []),
            "journals": user_record.get("journals", []),
        }
    
    def add_task(self, user, task):
        if not task:
            return False
        
        self.db[user]["tasks"].append(task)
        self.save_db()
        return True
    
    def mark_as_done(self, user, task):
        if not task:
            return False
        
        self.db[user]["tasks"].remove(task)
        self.db[user]["finished"].append(task)
        self.save_db()
        return True
    
    def remove_task(self, user, task):
        if not task:
            return False
        
        self.db[user]["tasks"].remove(task)
        self.save_db()
        return True


usermanager = Usermanager()