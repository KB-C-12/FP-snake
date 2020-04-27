import pygame as pg
import subprocess as sp
from random import randint
from numpy import sqrt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (200, 0, 0)

DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

# semua objek dalam screen adalah spot
class Spot:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.f = 0
    self.g = 0
    self.h = 0
    self.neighbors = []
    self.camefrom = []
    self.obstacle = False

    if randint(1, 101) < 3:
        self.obstacle = True

  def show(self, color):
    pg.draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

  def add_neighbors(self):
    if self.x > 0:
        self.neighbors.append(grid[self.x - 1][self.y])

    if self.y > 0:
        self.neighbors.append(grid[self.x][self.y - 1])

    if self.x < rows - 1:
        self.neighbors.append(grid[self.x + 1][self.y])

    if self.y < cols - 1:
        self.neighbors.append(grid[self.x][self.y + 1])

def getpath(food1, snake1):
  food1.camefrom = []     # init food camefrom

  for s in snake1: s.camefrom = []    #init snake camefrom

  openset = [snake1[-1]]  #openset diinisiasi dengan kepala snake
  closedset = []
  dir_array1 = []

  while 1:
    if not openset:
      print("No way to Food")
      break

    current1 = min(openset, key=lambda x: x.f)    #current 1 = nilai minimum f dalam openset

    temp = []
    for i in range(len(openset)):
      if openset[i] != current1:
        temp.append(openset[i])
    
    openset = temp              # keluarin current 1 dari open set
    closedset.append(current1)  # masukin current 1 ke closed set
    
    for neighbor in current1.neighbors:
      if neighbor not in closedset and not neighbor.obstacle and neighbor not in snake1:
        tempg = neighbor.g + 1

        if neighbor in openset:
          if tempg < neighbor.g:
            neighbor.g = tempg

        else:
          neighbor.g = tempg
          openset.append(neighbor)

        neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
        neighbor.f = neighbor.g + neighbor.h
        neighbor.camefrom = current1

    if current1 == food1: break

  while current1.camefrom:
    if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
      dir_array1.append(UP)

    elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
      dir_array1.append(DOWN)

    elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
      dir_array1.append(LEFT)

    elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
      dir_array1.append(RIGHT)
        
    current1 = current1.camefrom

  #print(dir_array1)

  for i in range(rows):
    for j in range(cols):
      grid[i][j].camefrom = []
      grid[i][j].f = 0
      grid[i][j].h = 0
      grid[i][j].g = 0
      
  return dir_array1

def drawGrid(w, rows, surface):
  sizeBtwn = w // rows

  x = 0
  y = 0
  for i in range(rows):
    x += sizeBtwn
    y += sizeBtwn

    pg.draw.line(surface, GRAY, (x, 0), (x, w))
    pg.draw.line(surface, GRAY, (0, y), (w, y))
 
  pass

def redrawWindow(surface):
  global rows, width
  surface.fill(BLACK)
  drawGrid(width, rows, surface)
  pg.display.update()

################################## MAIN PROGRAM ############################################
pg.init()
cols = 30
rows = 30

width = 720
height = 720
wr = width/cols
hr = height/rows
direction = 1

screen = pg.display.set_mode([width, height])
pg.display.set_caption("SNAKE GAME")
clock = pg.time.Clock()

#buat grid
grid = []
for i in range(rows):
  grid.append([])
  for j in range(cols):
    grid[i].append(Spot(i,j))

#tiap grid tau neighbornya
for i in range(rows):
  for j in range(cols):
    grid[i][j].add_neighbors()


snake = [grid[rows//2][cols//2]]                      # posisi awal snake di tengah grid
food = grid[randint(0, rows-1)][randint(0, cols-1)]   # posisi awal makanan random di grid
current = snake[-1]                                   # posisi saat ini(head)

dir_array = getpath(food, snake)
score = 0

sp.call('clear',shell=True)
print("Score = ",score)
out = False
done = False

while not done:
  pg.time.delay(0) #makin besar makin lambat
  clock.tick(20)        #kecepatan game, makin besar makin cepat
  redrawWindow(screen)  #background color map

  direction = dir_array.pop(-1)
  
  if direction == DOWN:
    snake.append(grid[current.x][current.y + 1])
  
  elif direction == RIGHT:
    snake.append(grid[current.x + 1][current.y])
  
  elif direction == UP:
    snake.append(grid[current.x][current.y - 1])
  
  elif direction == LEFT:
    snake.append(grid[current.x - 1][current.y])
  
  current = snake[-1]

  # kali dia makan, skor++
  if current.x == food.x and current.y == food.y:
    score = score + 1
    sp.call('clear',shell=True)
    print("Score = ",score)
    while 1:
      food = grid[randint(0, rows - 1)][randint(0, cols - 1)]   # posisi makanan baru dirandom
      if not (food.obstacle or food in snake): break
        
    dir_array = getpath(food, snake)
  
  else: snake.pop(0)      #pop bagian belakang

  # warna badan ular
  for spot in snake:
    spot.show(WHITE)

  # warna obstacle
  for i in range(rows):
    for j in range(cols):
      if grid[i][j].obstacle:
        grid[i][j].show(RED)

  food.show(GREEN)
  snake[-1].show(BLUE)
  pg.display.flip()

  if not dir_array:
    print("GAME OVER!!!")
    pg.display.set_caption("SNAKE GAME - GAME OVER!!!")
    
    while True:
      for event in pg.event.get():
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_q or event.key == pg.K_ESCAPE:
            print("ESC or Q pressed, EXIT GAME")
            done = True
            out = True
            break
      if out : break


  for event in pg.event.get():
    if event.type == pg.QUIT:
      done = True

    elif event.type == pg.KEYDOWN:
      if event.key == pg.K_q or event.key == pg.K_ESCAPE:
        print("ESC or Q pressed, EXIT GAME")
        done = True
########################################END OF MAIN####################