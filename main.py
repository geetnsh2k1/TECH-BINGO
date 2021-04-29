class Bingo:
    def __init__(self, data):
        self.matrix = data['matrix']
        self.completed = set(data['completed'])
        self.game = data['current']
        self.input = data['input']
        
        self.found = False
        
        self.play()

    def play(self):
        for i in range(0, 5):
            for j in range(0, 5):
                if self.matrix[i][j] == self.input:
                    self.found = True
                    self.matrix[i][j] = -1
                    vertical = self.check_up(i, j)+self.check_down(i, j)+1
                    horizontal = self.check_left(i, j)+self.check_right(i, j)+1
                    tl_br=0
                    bl_tr=0

                    if i==2 and j==2:
                        tl_br = self.check_tl_br()
                        bl_tr = self.check_bl_tr()
                    elif i==j:
                        tl_br = self.check_tl_br()
                    elif i+j == 4:
                        bl_tr = self.check_bl_tr()
                    
                    if vertical == 5:
                        if i+1 not in self.completed:
                            self.game = self.game[1:]
                            self.completed.add(j+1)
                    if horizontal == 5:
                        if j+1 not in self.completed:
                            self.game = self.game[1:]
                            self.completed.add(i+1+5)
                    if tl_br == 5:
                        if 11 not in self.completed:
                            self.game = self.game[1:]
                            self.completed.add(11)
                    if bl_tr == 5:
                        if 15 not in self.completed:
                            self.game = self.game[1:]
                            self.completed.add(15)
                            
    def check_up(self, i, j):
        i-=1
        count=0
        while i>=0 and self.matrix[i][j] == -1:
            i-=1
            count+=1
        return count
    
    def check_down(self, i, j):
        i+=1
        count=0
        while i<=4 and self.matrix[i][j] == -1:
            i+=1
            count+=1
        return count
    
    def check_left(self, i, j):
        j-=1
        count=0
        while j>=0 and self.matrix[i][j] == -1:
            j-=1
            count+=1
        return count
    
    def check_right(self, i, j):
        j+=1
        count=0
        while j<=4 and self.matrix[i][j] == -1:
            j+=1
            count+=1
        return count
    
    def check_tl_br(self):
        i, j, count = 0, 0, 0
        while i<=4 and j<=4 and self.matrix[i][j] == -1:
            i+=1
            j+=1
            count+=1
        return count
    
    def check_bl_tr(self):
        i, j, count = 4, 0, 0
        while i>=0 and j<=4 and self.matrix[i][j] == -1:
            i-=1
            j+=1
            count+=1
        return count

    def get_data(self):
        data = {
            "matrix":self.matrix,
            "completed":self.completed,
            "current":self.game,
            "found":self.found,
        }
        return data
