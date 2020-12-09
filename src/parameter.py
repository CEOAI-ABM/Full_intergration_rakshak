class Grid():
    def __init__(self, length, width, default=''):
        self.length = length
        self.width = width
        self.data = [[default for x in range(length)] for y in range(width)]

    def set(self, x, y, value):
        self.data[x][y] = value

    def get(self, x, y):
        return self.data[x][y]


class SubGrid(Grid):
    def __init__(self ,length, width, length1, width1, default=''):
        self.length1 = length1
        self.width1 = width1
        self.data1 = [[[[default for x in range(length)] for y in range(width)]for x in range(length1)] for y in range(width1)]

    def set(self, x, y, x1, y1, value):
        self.data1[x][y][x1][y1] = value

    def get(self, x, y, x1, y1):
        return self.data1[x][y][x1][y1]

class SubSubGrid(SubGrid):
    def __init__(self,length, width, length1, width1, length2, width2, default=''):
        self.length2 = length2
        self.width2 = width2
        self.data2 = [[[[[[default for x in range(length)] for y in range(width)]for x in range(length1)] for y in range(width1)]for x in range(length2)] for y in range(width2)]

    def set(self, x, y, x1, y1, x2, y2):
        self.data2[x][y][x1][y1][x2][y2] = value

    def get(self, x, y, x1, y1, x2, y2, value):
        return self.data2[x][y][x1][y1][x2][y2]
