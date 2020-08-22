class Falloff_Generator():
    def __init__(self,width,height):
        self.width = width
        self.height = height
    def island(self):
        new_level = [["" for i in range(self.height)]for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                x = i / float(self.width) * 2 - 1
                y = j / float(self.height) * 2 - 1

                value = max(abs(x),abs(y))
                new_level[i][j] = self.island_eq(value)
        return new_level
    
    def island_eq(self,val):
         a = 3
         b = 6
         return val**a/(val**a +(b-b*val)**a)
