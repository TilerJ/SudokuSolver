import numpy as np
import random,time,math
import pygame

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
        self.Order = []
        self.Grid = Grid

    def Step(self):
        if len(solver.Grid[solver.Grid == 0]) > 0:
            Position,Possibilities = solver.FindLowestPossibility()
            if len(Possibilities) == 0:
                #need to back track
                newpathfound = False
                while not newpathfound:
                    Position,Possibilities = self.Order.pop()
                    print(Position,Possibilities)
                    solver.Grid[Position[0],Position[1]] = 0
                    if len(Possibilities) > 0:
                        choice = random.choice(list(Possibilities))
                        Possibilities.remove(choice)
                        solver.Grid[Position[0],Position[1]] = choice
                        self.Order.append([Position,Possibilities])
                        newpathfound = True


                pass
            else:
                choice = random.choice(list(Possibilities))
                Possibilities.remove(choice)
                solver.Grid[Position[0],Position[1]] = choice
                self.Order.append([Position,Possibilities])

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
    
    def GetPossibility(self,Position):
        possibilities = set(range(1,10)) #used for better lookup times
        known_values = set()
        for val in self.Check_Horizontal(Position[0]): known_values.add(val)
        for val in self.Check_Vertical(Position[1]): known_values.add(val)
        for val in self.Check_Square(Position[0],Position[1]): known_values.add(val)

        result = possibilities.difference(known_values)

        return result

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
    
    def CheckGrid(self):
                #Check through each element of the grid and find the element of the lowest guesses
        for i in range(9):
            for j in range(9):
                if self.Grid[i,j] != 0: continue

                possibilities = set(range(1,10)) #used for better lookup times
                known_values = set()
                for val in self.Check_Horizontal(i): known_values.add(val)
                for val in self.Check_Vertical(j): known_values.add(val)
                for val in self.Check_Square(i,j): known_values.add(val)

                result = possibilities.difference(known_values)

                if len(result) >0:
                    return False
            pass
            
        return True

grid = Grid = np.zeros([9,9])#SetupGrid()
solver = Solver(grid)

# pygame setup
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

buttonwidth = 200
buttonheight = 50

INSET = WINDOW_WIDTH*0.05
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font('freesansbold.ttf',40)
def drawGrid(grid,selectedSquare):
    blockSize = math.ceil((WINDOW_WIDTH -INSET*2)/ 9) #Set the size of the grid block

    #thicker lines
    for x in range(3):
        for y in range(3):
            rect = pygame.Rect(x*blockSize*3+INSET, y*blockSize*3+INSET, blockSize*3, blockSize*3)
            pygame.draw.rect(screen, (0,0,0), rect, 3)


    for x in range(9):
        for y in range(9):
            rect = pygame.Rect(x*blockSize+INSET, y*blockSize+INSET, blockSize, blockSize)
            pygame.draw.rect(screen, (0,0,0), rect, 1)
            numb = int(grid[y,x])
            if selectedSquare ==[x,y]:
                pygame.draw.rect(screen, (255,0,0), rect, 2)
            else:
                pygame.draw.rect(screen, (0,0,0), rect, 1)
            if numb != 0:
                value = font.render(str(numb),True,(0,0,0))
                screen.blit(value,(x*blockSize+blockSize*17.5/20,y*blockSize+blockSize*15/20))

tick = 0
selectedSquare = None
Started = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and not Started:
            pos = pygame.mouse.get_pos()
            #Normalizing the position
            x = math.floor((pos[0] - INSET)/math.ceil((WINDOW_WIDTH -INSET*2)/ 9))
            y = math.floor((pos[1] - INSET)/math.ceil((WINDOW_WIDTH -INSET*2)/ 9))
            if x < 0 or y < 0 or x>8 or y > 8:
                pass
            else:
                selectedSquare = [x,y]
            
            if WINDOW_WIDTH/2-buttonwidth/2 < pos[0] < WINDOW_WIDTH/2+buttonwidth/2 and WINDOW_HEIGHT-50-buttonheight/2 < pos[1] < WINDOW_HEIGHT-50+buttonheight/2:
                Started = True
                selectedSquare = [10,10]
        elif event.type == pygame.KEYDOWN:
            if selectedSquare != None and not Started:
                if event.key == pygame.K_0:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 0
                elif event.key == pygame.K_1:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 1
                elif event.key == pygame.K_2:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 2
                elif event.key == pygame.K_3:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 3
                elif event.key == pygame.K_4:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 4
                elif event.key == pygame.K_5:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 5
                elif event.key == pygame.K_6:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 6
                elif event.key == pygame.K_7:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 7
                elif event.key == pygame.K_8:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 8
                elif event.key == pygame.K_9:
                    solver.Grid[selectedSquare[1],selectedSquare[0]] = 9

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((200,200,200))

    # RENDER YOUR GAME HERE
    drawGrid(grid,selectedSquare)

    if not Started:

        rect = pygame.Rect(WINDOW_WIDTH/2-buttonwidth/2,WINDOW_HEIGHT-50-buttonheight/2,buttonwidth,buttonheight)
        pygame.draw.rect(screen, (46,46,46), rect)
        value = font.render("Start",True,(200,200,200))
        screen.blit(value,(WINDOW_WIDTH/2 - 50,WINDOW_HEIGHT-65))

    #Do Step
    if Started and tick% 1 ==0:
        solver.Step()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    tick+=1

pygame.quit()