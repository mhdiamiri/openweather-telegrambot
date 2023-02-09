class UserBot:
    
    def __init__(self, user_id:int): 
        self.id = user_id
        try:
            with open(str(user_id), 'r') as f:
                self.menu = int(f.read())
        except:
            self.setMenu(0)
    
    def setMenu(self, menu):
        with open(str(self.id), 'w') as f:
            f.write(str(menu))
            self.menu = menu
    
    def getId(self):
        return self.id
    
    def getMenu(self):
        return self.menu
    