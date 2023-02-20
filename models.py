import json

class Cds:
    def __init__(self):
        try:
            with open("cd's.json", "r") as f:
                self.cds = json.load(f)
        except FileNotFoundError:
            self.cds = []
    
    def all(self):
        return self.cds
    
    def get(self, id):
        cds = [cds for cds in self.all() if cds['id'] == id]
        if cds:
            return cds[0]
        return []
    
    def create(self, data):
        self.cds.append(data)
        self.save_all()

    def save_all(self):
        with open("cd's.json", "w") as f:
            json.dump(self.cds, f)
    
    def update(self, id, data):
        data.pop('csrf_token')
        self.cds[id] = data
        self.save_all()

    def delete(self, id):
        cd = self.get(id)
        if cd:
            self.cds.remove(cd)
            self.save_all()
            return True
        return False
    
    def update(self, id, data):
        cd = self.get(id)
        if cd:
            index = self.cds.index(cd)
            self.cds[index] = data
            self.save_all()
            return True
        return False

cds = Cds()