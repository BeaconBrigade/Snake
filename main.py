import pygame
from guizero import App, Text, PushButton, Picture, Window, Box, question
from random import randrange
from csv import reader, writer

class follow :
  """
  Creates white rectangle that can follow the previous rectangle's path.

  Attributes:
    1. self.rect
      rect object
    2. self.x
      x coordinate to draw the rectangle
    3. self.y
      y coordinate to draw the rectangle
    4. self.ind
      Index in the list of follow objects (l_follow)
  
  Methods:
    1. __init__(self, x, y)
      Sets attributes and appends object to l_follow
    2. snake_update(self) 
      Takes x and y coordinates of the rectangle before.
    3. snake_draw(self)
      Draws the rectangle using the x and y coordinates.
  """
  def __init__(self, x, y) :
    #Create rect.
    self.rect = pygame.Rect(x, y, 20, 20)
    self.x = x
    self.y = y
    
    #Add to list
    l_follow.append(self)
    self.ind = l_follow.index(self)

  #Update x and y coordinates
  def snake_update(self) :
    if self.ind != 0 : 
      self.x = (oldX[self.ind - 1])
      self.y = (oldY[self.ind - 1])
    else :
      self.x = snakeX
      self.y = snakeY
    self.rect = pygame.Rect(self.x, self.y, 20, 20)

  #Draw rect
  def snake_draw(self) :
    pygame.draw.rect(screen, white, self.rect, width = 20)

#Game loop
def main_loop() :
  """
  Run the game. Runs everything from the food, 
  the snake location, the snake followers, 
  the collision detection, the end of the game and so on.
  """
  global snake_direction, oldX, oldY, score_value, foodX, foodY, snakeX, snakeY, snakeX_speed, snakeY_speed, colour, running, end, l_follow

  running = True
  while running :
    
    #Draw background
    screen.fill(black)
    draw_grid()

    #FPS
    clock.tick(5)

    #Snake collisions
    for i in range(len(l_follow)) :
      if snakeX == l_follow[i].x and snakeY == l_follow[i].y :
        game_over_text()

    for event in pygame.event.get() :
      
      #Close window
      if event.type == pygame.QUIT :
        running = False

      #Snake direction
      if event.type == pygame.KEYDOWN :
        if event.key == pygame.K_LEFT :
          if snake_direction != 'right' :  
            snakeX_speed = -20
            snakeY_speed = 0
            snake_direction = 'left'
            break
        elif event.key == pygame.K_RIGHT :
          if snake_direction != 'left' : 
            snakeX_speed = 20 
            snakeY_speed = 0
            snake_direction = 'right'
            break
        elif event.key == pygame.K_DOWN :
          if snake_direction != 'up' : 
            snakeY_speed = 20
            snakeX_speed = 0
            snake_direction = 'down'
            break
        elif event.key == pygame.K_UP :
          if snake_direction != 'down' : 
            snakeY_speed = -20 
            snakeX_speed = 0
            snake_direction = 'up'
            break

      #Game over
      if end :
        
        #Stop snake movement
        snakeX_speed = 0
        snakeY_speed = 0
        
        if event.type == pygame.MOUSEBUTTONDOWN :
          
          if main_menu_rect.collidepoint(pygame.mouse.get_pos()) :
            
            app.show()

            #Collect three initials from player
            initials = question(title = 'Initials', question = 'Type your initials:', initial_value = '---')
            if initials is not None :
              init = initials[:3].upper()
            else :
              init = '---'

            #Store score
            with open('scores.csv', 'a') as f:
              file = writer(f) 
              inputs = [score_value, init]
              file.writerow(inputs)
              f.close()

            #Reset variables for re-run
            running = False
            end = False
            l_follow = []
            oldX = []
            oldY = []
            snakeX = 200
            snakeY = 200
            foodX = randrange(0, w_width, 20)
            foodY = randrange(0, w_height, 20)
            snakeX_speed = 0
            snakeY_speed = 0
            snake_direction = ''
            score_value = 0

            
            app.display()


    #Main menu button colour
    if main_menu_rect.collidepoint(pygame.mouse.get_pos()) :
      colour = (255,0,255)
    else :
      colour = (255,255,0)

    #Draw
    food(foodX, foodY)
    snake(snakeX, snakeY)

    #Save previous positions
    oldX = [x.x for x in l_follow]
    oldY = [y.y for y in l_follow]
    
    #Re-draw followers
    for i in range(len(l_follow)) :
      l_follow[i].snake_draw()
      l_follow[i].snake_update()


    #Food collision
    collide = snake_rect.colliderect(food_rect)
    if collide :
      score_value += 1

      #Player wins
      if score_value >= 400 :
        game_over_text()
      
      #New food location
      foodX = randrange(0, w_width, 20)
      foodY = randrange(0, w_height, 20)
      if food_coord(foodX, foodY) :
        foodX = randrange(0, w_width, 20)
        foodY = randrange(0, w_height, 20)

      #Instantiate follow object
      if len(l_follow) == 0 :
        new_snek = follow(snakeX, snakeY)
      else :
        new_snek = follow(l_follow[-1].x, l_follow[-1].y)

    #Boundaries
    if snakeX < 0 or snakeX > 380 or snakeY < 0 or snakeY > 380 :
      game_over_text()

    #Movement
    snakeX += snakeX_speed
    snakeY += snakeY_speed

    #Score text
    score_update()

    pygame.display.update()

#Start Pygame
pygame.init()

#Variables
white = (255,255,255)
black = (0,0,0)
w_width = 400
w_height = 400
end = False
clock = pygame.time.Clock()

#Screen
screen = pygame.display.set_mode((w_width, w_height))
screen.fill(black)
pygame.display.set_caption('Snake')

#Game over
game_font = pygame.font.Font('ARCADECLASSIC.TTF', 64)

#Blank return to main menu button
main_menu_rect = pygame.Rect(0, 0, 0, 0)
colour = (255,255,0)

def game_over_text() :
  global end, main_menu_text, main_menu_rect
  
  #Game over text
  if score_value != 400 :  
    over = game_font.render('GAME OVER', True, (255,255,0))
  else :
    over = game_font.render('YOU WIN!!', True, (255,255,0))
  screen.blit(over, (65,175))
  
  #Main menu text
  main_menu_text = font.render('Main Menu', True, colour)
  screen.blit(main_menu_text, (240,15))

  #Main menu button
  main_menu_rect = pygame.Rect(238, 18, 152, 26)
  pygame.draw.rect(screen, [255, 255, 255], main_menu_rect, -1)
  
  end = True

#Create the grid - for testing page size
def draw_grid() :
  w_spaces = 20  
  for x in range(0, w_width, w_spaces) :
    for y in range(0, w_height, w_spaces) :
      rect = pygame.Rect(x, y, w_spaces, w_spaces)
      pygame.draw.rect(screen, black, rect, 1)

#Score
score_value = 0
font = pygame.font.Font('ARCADECLASSIC.TTF', 32)

def score_update() :
  score = font.render('Score ' + str(score_value), True, (255,255,0))
  screen.blit(score, (15,15))

#Snake
snakeX = 200
snakeY = 200
snakeX_speed = 0
snakeY_speed = 0
snake_direction = None
l_follow = []

def snake(x, y) :
  global snake_rect
  snake_rect = pygame.Rect(x, y, 20, 20)
  pygame.draw.rect(screen, white, snake_rect, width = 20)

#Food
foodX = randrange(0, w_width, 20)
foodY = randrange(0, w_height, 20)

def food(x,y) :
  global food_rect
  food_rect = pygame.Rect(x, y, 20, 20)
  pygame.draw.rect(screen, (255,0,255), food_rect, width = 20)

def food_coord(x,y) :
  for i in range(len(l_follow)) :
    if x == l_follow[i].x and y == l_follow[i].y :
      return True
  
  return False


#User interface
def play() :
  #Start game
  app.hide()
  main_loop()

#Create leaderboard
def show_leaderboard() :
  
  global leader_list, header, top_leaders
  leader_list.destroy()
  
  with open('scores.csv', 'r') as f :
    
    #Read scores and initials
    file = dict(filter(None, reader(f)))
    leader_list = Box(leaderboard_window, align = 'top')
    
    #List of scores
    file_sort = [int(x) for x in file.keys()]
    file_sort.sort(reverse = True)



    x = 0
    if file is not None :  
      
      #Headers
      header = Text(leader_list, text = 'RANK NAME SCORE', size = 12, color = 'yellow', font = 'ARCADECLASSIC.TTF')

      for i in file_sort :

        #Write top ten leaderboard entries
        if x < 10 :  
          if x + 1 == 1 :
            suffix = 'ST'
          elif x + 1 == 2 :
            suffix = 'ND'
          elif x + 1 == 3 :
            suffix = 'RD'
          else :
            suffix = 'TH'

          top_leaders = Text(leader_list, text = f'{x + 1}{suffix} : {file[str(file_sort[x])]} : {file_sort[x]}', size = 12, font = 'ARCADECLASSIC.TTF', color = 'white')

        x += 1

    f.close()

def close_leaderboard() :
  #Open main menu from leaderboard
  leaderboard_window.hide()
  app.show()

def open_leaderboard() :
  #Open leaderboard page
  app.hide()
  leaderboard_window.show()
  show_leaderboard()

#Main page
app = App(title = 'Snake', width = 400, height = 400, bg = 'black')

title = Text(app, text = 'PLAY SNAKE NOW', font = 'ARCADECLASSIC.TTF', size = 32, align = 'top', color = 'white')

background = Picture(app, image = 'snake_background.jpg', width = 400, height = 181)

play_button = PushButton(app, text = 'PLAY', command = play) 
play_button.bg = 'red'
play_button.text_color = 'white'
play_button.text_size = '16'
play_button.font = 'ARCADECLASSIC.TTF'

play_button = PushButton(app, text = 'LEADERBOARD', command = open_leaderboard) 
play_button.bg = 'blue'
play_button.text_color = 'white'
play_button.text_size = '16'
play_button.font = 'ARCADECLASSIC.TTF'

#Leaderboard page
leaderboard_window = Window(app, title = 'Snake', width = 400, height = 400, bg = 'black')

leader_title = Text(leaderboard_window, text = 'LEADERBOARD', font = 'ARCADECLASSIC.TTF', size = 32, align = 'top', color = 'white')

leader_list = Box(leaderboard_window)

return_menu = PushButton(leaderboard_window, text = 'MAIN MENU', command = close_leaderboard)
return_menu.bg = 'blue'
return_menu.text_color = 'white'
return_menu.text_size = '16'
return_menu.font = 'ARCADECLASSIC.TTF'

leaderboard_window.hide()
app.display()