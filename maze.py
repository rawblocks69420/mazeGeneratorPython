import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Set the cell size of the grid
GRID_CELL_SIZE = 50

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window title
pygame.display.set_caption("Grid in Pygame")

# Define the colors
WHITE = (255, 255, 255)


#this object will determine where to put ones on the grid.
class Cursor:
    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        self.backlist = [[startx,starty]]

        self.linedest = []
    
    def squares_available(self, grid):
        #check surrounding 4 squares to see if any are available.
        #returns a list off all of the positions like 'down','up','left','right'
        directions = []
        #right
        try:
            if (grid[self.x+1][self.y] == 0):
                directions.append('right')
        except:
            nothinga = 0
        try:    
            if ((grid[self.x-1][self.y] == 0) and self.x >= 1):
                directions.append('left')
        except:
            nothinga = 0
        try:
            if (grid[self.x][self.y+1] == 0):
                directions.append('down')
        except:
            nothinga = 0
        try:
            if ((grid[self.x][self.y-1] == 0) and self.y >= 1):
                directions.append('up')
        except:
            nothinga = 0

        return directions

    def movement(self,grid):
        #i need to convert the grid coordinates to the line pixels
        # in order to figure out which line to move you have to know two coordinates, previous, and current position.
        #first find these two coordinates together, then  GRID_CELL_SIZE
        x = round((self.x * GRID_CELL_SIZE))
        y = round((self.y * GRID_CELL_SIZE))

        movements = self.squares_available(grid)
        move = ""

        try:
            move = random.choice(movements)
        except:
            print("exception")

        if (move == "right"):
            self.linedest.append(pygame.Rect(x+GRID_CELL_SIZE,y,1,GRID_CELL_SIZE))
            self.x += 1       
        elif (move == "left"):
            self.linedest.append(pygame.Rect(x,y,1,GRID_CELL_SIZE))
            self.x -= 1    
        elif (move == "up"):
            self.linedest.append(pygame.Rect(x,y,GRID_CELL_SIZE,1))
            self.y -= 1   
        elif (move == "down"):
            self.linedest.append(pygame.Rect(x,y+GRID_CELL_SIZE,GRID_CELL_SIZE,1))
            self.y += 1
        else:
            self.backtrack(grid)
            #i need it to backtrack and then call movement, and then move.

        self.backlist.append([self.x,self.y])
        grid[self.x][self.y] = 1

        
    def backtrack(self,grid):
        while(True):
            item = self.backlist.pop()
            self.x = item[0]
            self.y = item[1]

            movements = self.squares_available(grid)

            #if there is a way, then it returns
            if(len(movements)>0):
                return
                     
    def getLinedest(self):
        return self.linedest
    

# Create the grid

#this creates a two-d grid 
grid = []
for x in range(0, 15):#SCREEN_WIDTH // GRID_CELL_SIZE, GRID_CELL_SIZE):
    row = []
    for y in range(0, 15):#SCREEN_HEIGHT // GRID_CELL_SIZE, GRID_CELL_SIZE):
        row.append(0)
    grid.append(row)
  
# Main game loop
running = True

#main list
linelist = []

curse = Cursor(3,4)
clock = pygame.time.Clock()
while running:
    # Fill the screen with white
    screen.fill(WHITE)
    # Draw the grid
    rowcounter = 0
    cellcounter = 0
    for row in grid:
        rowcounter +=1
        cellcounter = 0
        for cell in row:
            cellcounter +=1
            x = round((cellcounter * GRID_CELL_SIZE)-GRID_CELL_SIZE)
            y = round((rowcounter * GRID_CELL_SIZE)-GRID_CELL_SIZE)
            
            #instead of drawing lines, i want to create rect objects.
            #draws the box

            #top line
            rect = pygame.Rect(x,y,GRID_CELL_SIZE,1)
            #bottom line
            rect2 = pygame.Rect(x,y+GRID_CELL_SIZE,GRID_CELL_SIZE,1)
            #left line
            rect3 = pygame.Rect(x,y,1,GRID_CELL_SIZE)
            #right line
            rect4 = pygame.Rect(x+GRID_CELL_SIZE,y,1,GRID_CELL_SIZE)

            if cell >= 1:
                pygame.draw.rect(screen,(255,200,255),pygame.Rect(x,y,GRID_CELL_SIZE,GRID_CELL_SIZE))
                if (rect not in linelist):
                    linelist.append(rect)
                if rect2 not in linelist:
                    linelist.append(rect2)
                if rect3 not in linelist:
                    linelist.append(rect3)
                if rect4 not in linelist:
                    linelist.append(rect4)
                

    #I could have a seperate list that removes all the current lines
    
    #this draws all of the lines to the screen.
    for rect in linelist:
        if (rect in curse.getLinedest()):
            continue
        pygame.draw.rect(screen,(255,0,5),rect)
        
    curse.movement(grid)
            
    # Update the screen
    pygame.display.flip()
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(10)
# Quit Pygame

pygame.quit()
