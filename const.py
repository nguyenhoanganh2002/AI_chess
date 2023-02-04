# Screen dimesions
WIDTH = 800
HEIGH = 800

#Board dimesions
ROWS = 8
COLS = 8
SQSIZE = WIDTH // COLS

COLOR1 = (234, 235, 200)
COLOR2 = (119, 154, 88)

#pos(col, row)
#rect top, left, bottom, right

class Const:
    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4,
        "5": 3, "6": 2, "7": 1, "8": 0
    }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {
        "a": 0, "b": 1, "c": 2, "d": 3,
        "e": 4, "f": 5, "g": 6, "h": 7 
    }
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def indexToColRow(idx):
        row =  7 - idx // 8
        col = idx % 8
        return (col, row)

    def colRowToIndex(pos):
        return (7 - pos[1])*8 + pos[0]
    
   
    
    def posToindex(pos):
        return pos[0] + (7 - pos[1])*8
    
    
    


