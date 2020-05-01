import pygame as pg
import subprocess as sp
from random import randint
from numpy import sqrt
import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BLUE = (112, 161, 215)
GREEN = (133, 202, 119)
RED = (255, 100, 90)


HEAD = (210, 145, 188)
BACKGROUND = (255, 244, 156)
BODY = (224, 187, 228)

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

    global level
    if randint(1, rows - 2) < level:    # < jumlah obstacle dlm 1 tempat
        self.obstacle = True

  def show(self, color):
    pg.draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

  def add_neighbors(self):
    if self.x > 1:
        self.neighbors.append(grid[self.x - 1][self.y])

    if self.y > 1:
        self.neighbors.append(grid[self.x][self.y - 1])

    if self.x < rows - 2:
        self.neighbors.append(grid[self.x + 1][self.y])

    if self.y < cols - 2:
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
  sizeBtwn = w / rows

  x = 0
  y = 0
  for i in range(rows):
    x += sizeBtwn
    y += sizeBtwn

    pg.draw.line(surface, WHITE, (x, 0), (x, w))
    pg.draw.line(surface, WHITE, (0, y), (w, y))
 
  pass

def redrawWindow(surface):
  global rows, width
  surface.fill(BACKGROUND)
  drawGrid(width, rows, surface)

############################ DECLARATION ###################################
pg.init()
root = Tk()
destroyed = False
toMainMenu = True

cols = 24
rows = 24

width = 720
height = 720
wr = width/cols
hr = height/rows
direction = 1
level = 1

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
food = grid[randint(1, rows-2)][randint(1, cols-2)]   # posisi awal makanan random di grid
current = snake[-1]                                   # posisi saat ini(head)

dir_array = getpath(food, snake)
score = 0

sp.call('clear',shell=True)
print("Score = ",score)
out = False
done = False
isSetup = True
#-------------------------------- END DECLARATION -------------------------------------#


################### END MESSAGE #####################################
def Again():
  global destroyed
  root.destroy()
  destroyed = True
  mainMenu()

def Exit():
  global done, out
  print('EXIT GAME')
  done = True
  out = True
  root.destroy()

def endMessage(content):
  root.title("\tSNAKE GAME - GAME OVER!!!")
  root.geometry('360x144')
  myLabel = Label(root, text=content)
  myLabel.pack()

  myYesButton = Button(root, text="Play again", command=Again)
  myYesButton.pack()

  myNoButton = Button(root, text="Exit", command=Exit)
  myNoButton.pack()

  root.mainloop()

def message_box(content):
  root.title("Key pressed")
  messageFrame = LabelFrame(root, padx=10, pady=10)
  messageFrame.pack(padx=10, pady=10)

  myLabel = Label(messageFrame, text=content)
  myLabel.pack()

  myNoButton = Button(messageFrame, text="OK", command=Exit)
  myNoButton.pack()

  root.mainloop()

#-------------------------- END MESSAGE -----------------------------------#

################################### MAIN MENU ######################################
def setLevel(l):
  global level
  level = l
  myLabel = Label(root, text="Level : " + str(level))
  myLabel.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

def setSize(s):
  global cols, rows
  cols = s
  rows = s
  myLabel = Label(root, text="Size : " + str(s))
  myLabel.grid(row=6, column=0, columnspan=5, padx=10, pady=10)

def mainMenu():
  global destroyed, root
  if destroyed:
    root = Tk()
    destroyed = False

  root.title("\tSNAKE GAME - WELCOME!!!")
  root.geometry('650x810')
  my_img = ImageTk.PhotoImage(Image.open("assets/snake.png"))
  
  imageLabel = Label(image=my_img)
  imageLabel.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
  
  levelLabel = Label(root, text="Level:")
  levelLabel.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

  level_1 = Button(root, text="1", padx=40, pady=20, command=lambda: setLevel(1))
  level_2 = Button(root, text="2", padx=40, pady=20, command=lambda: setLevel(2))
  level_3 = Button(root, text="3", padx=40, pady=20, command=lambda: setLevel(3))
  level_4 = Button(root, text="4", padx=40, pady=20, command=lambda: setLevel(4))
  level_5 = Button(root, text="5", padx=40, pady=20, command=lambda: setLevel(5))

  level_1.grid(row=2, column=0)
  level_2.grid(row=2, column=1)
  level_3.grid(row=2, column=2)
  level_4.grid(row=2, column=3)
  level_5.grid(row=2, column=4)
  
  sizeLabel = Label(root, text="Size:")
  sizeLabel.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

  size_24 = Button(root, text="24x24", padx=40, pady=20, command=lambda: setSize(24))
  size_30 = Button(root, text="30x30", padx=40, pady=20, command=lambda: setSize(30))
  size_36 = Button(root, text="36x36", padx=40, pady=20, command=lambda: setSize(36))
  size_40 = Button(root, text="40x40", padx=40, pady=20, command=lambda: setSize(40))
  size_45 = Button(root, text="45x45", padx=40, pady=20, command=lambda: setSize(45))

  size_24.grid(row=4, column=0)
  size_30.grid(row=4, column=1)
  size_36.grid(row=4, column=2)
  size_40.grid(row=4, column=3)
  size_45.grid(row=4, column=4)

  levelDesc = Label(root, text="Level : " + str(level))
  levelDesc.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

  sizeDesc = Label(root, text="Size : " + str(cols))
  sizeDesc.grid(row=6, column=0, columnspan=5, padx=10, pady=10)

  saveButton = Button(root, text="PLAY!!!", padx=90, pady=20, command=lambda: goTosetup())
  saveButton.grid(row=7, column=0, columnspan=5, padx=10, pady=10)
  root.mainloop()

def goTosetup():
  root.destroy()
  global destroyed
  destroyed = True
  setup()

def setup():
  global cols, rows, width, height, wr, hr, direction, screen, clock, grid, snake, food, current, dir_array, score, out, done, isSetup

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
  food = grid[randint(1, rows-2)][randint(1, cols-2)]   # posisi awal makanan random di grid
  current = snake[-1]                                   # posisi saat ini(head)

  dir_array = getpath(food, snake)
  score = 0

  sp.call('clear',shell=True)
  print("Level = ",level)
  print("Size = ",cols)
  print("Score = ",score)
  out = False
  done = False
  isSetup = True
#-------------------------------- MAIN MENU ----------------------------------#


################################## MAIN PROGRAM ############################################
while not done:
  if toMainMenu:
    mainMenu()
    toMainMenu = False
  
  if isSetup:
    setup()
    isSetup = False

  if destroyed:
    root = Tk()
    destroyed = False

  pg.time.delay(0) #makin besar makin lambat
  clock.tick(100)        #kecepatan game, makin besar makin cepat
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
    print("Level = ",level)
    print("Size = ",cols)
    print("Score = ",score)
    while 1:
      food = grid[randint(1, rows - 2)][randint(1, cols - 2)]   # posisi makanan baru dirandom
      if not (food.obstacle or food in snake): break
        
    dir_array = getpath(food, snake)
  
  else: snake.pop(0)      #pop bagian belakang

  # warna badan ular
  for spot in snake:
    spot.show(BODY)

  # warna obstacle
  for i in range(rows):
    for j in range(cols):
      if grid[i][j].obstacle or i == 0 or j == 0 or i == rows-1 or j == cols-1:
        grid[i][j].show(RED)

  food.show(GREEN)
  snake[-1].show(HEAD)
  pg.display.flip()

  if not dir_array:
    print("GAME OVER!!!")
    pg.display.set_caption("SNAKE GAME - GAME OVER!!!")
    endMessage('GAME OVER!!!' + "\nSCORE : "+ str(score) +"\n")

  for event in pg.event.get():
    if event.type == pg.QUIT:
      done = True

    elif event.type == pg.KEYDOWN:
      if event.key == pg.K_q or event.key == pg.K_ESCAPE:
        print("ESC or Q pressed, EXIT GAME")
        message_box("ESC or Q pressed, EXIT GAME" + "\nSCORE : "+ str(score) +"\n")
        done = True
########################################END OF MAIN####################
    