import numpy as np
import random,time

#Seting up the grid
def SetupGrid():
    Grid = np.zeros([9,9])
    Grid[0,0] = 5
    Grid[0,1] = 3
    Grid[0,4] = 7
    Grid[1,0] = 6
    Grid[1,3] = 1
    Grid[1,4] = 9
    Grid[1,5] = 5
    Grid[2,1] = 9
    Grid[2,2] = 8
    Grid[2,7] = 6
    Grid[3,0] = 8
    Grid[3,4] = 6
    Grid[3,8] = 3
    Grid[4,0] = 4
    Grid[4,3] = 8
    Grid[4,5] = 3
    Grid[4,8] = 1
    Grid[5,0] = 7
    Grid[5,4] = 2
    Grid[5,8] = 6
    Grid[6,1] = 6
    Grid[6,6] = 2
    Grid[6,7] = 8
    Grid[7,3] = 4
    Grid[7,4] = 1
    Grid[7,5] = 9
    Grid[7,8] = 5
    Grid[8,4] = 8
    Grid[8,7] = 7
    Grid[8,8] = 9
    return Grid


class Solver:
    def __init__(self,Grid) -> None:

        self.Grid = Grid
        self.Paths = []
        while len(self.Grid[self.Grid == 0]) > 0:
            #print(Grid)
            #time.sleep(2)
            Position,Possibilities = self.FindLowestPossibility()
            choice = random.choice(list(Possibilities))
            #print(Position,choice)
            self.Grid[Position[0],Position[1]] = choice
        
        print(self.Grid)
    
    def Check_Horizontal(self,i):
        Row = self.Grid[i,:]
        return Row[Row !=0]


    def Check_Vertical(self,j):
        Collumn = self.Grid[:,j]
        return Collumn[Collumn != 0]

    def Check_Square(self,i,j):
        #want to get the correct cell
        x = i // 3
        y = j // 3

        values = []
        for i in range(3):
            for j in range(3):
                val = self.Grid[i+x*3,j+y*3]
                if val != 0:
                    values.append(val)

        return values
        pass

    def FindLowestPossibility(self):
        
        #Check through each element of the grid and find the element of the lowest guesses
        LowestValue = 10
        LowestCoord = [0,0]
        LowestPossibilities = []
        for i in range(9):
            for j in range(9):
                if self.Grid[i,j] != 0: continue

                possibilities = set(range(1,10)) #used for better lookup times
                known_values = set()
                for val in self.Check_Horizontal(i): known_values.add(val)
                for val in self.Check_Vertical(j): known_values.add(val)
                for val in self.Check_Square(i,j): known_values.add(val)

                result = possibilities.difference(known_values)

                if len(result) < LowestValue:
                    if len(result) == 1: #There is only one value this can be
                        return [i,j], result
                    else:
                        LowestCoord = [i,j]
                        LowestValue = len(result)
                        LowestPossibilities = result
            pass
            
        return LowestCoord, LowestPossibilities

Solver(SetupGrid())