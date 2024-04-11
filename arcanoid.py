import pygame
pygame.init()

back = (200,255,255)
mw = pygame.display.set_mode((500,500))
mw.fill(back)
clock = pygame.time.Clock()

#змінні, що відповідають за координати платформи
platform_x =200
platform_y =330

#змінні, відповідальні за напрями переміщення м'яча
dx = 3
dy = 3

#фраги, які відповідають за рух платформи вправо/ліворуч
move_right = False
move_left = False

#прапор закінчення гри
game_over =False

#клас із попереднього проекту
class Area():
    def __init__(self, x=0, y=0, width =10, height =10, color=None):
        #запам'ятовуємо прямокутник:
        self.rect = pygame.Rect(x, y, width, height)
        # колір заливки - або переданий параметр, або загальний колір тла
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw,self.fill_color,self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

#клас для об'єктів-картинок
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width =10, height =10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)
 
    def draw(self):
        mw.blit(self.image, (self.rect.x,self.rect.y))
        
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
      self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

#створення м'яча та платформи
ball = Picture('ball.png',160,200,50,50)
platform = Picture('platform (1).png', platform_x, platform_y,90,9  )

#Створення ворогів
start_x =5
start_y =5
count = 9
monsters = []

for j in range(3):
    y = start_y + (55* j)
    x = start_x + (27.5* j)

    for i in range(count):
        d = Picture ('monster.png', x, y,50,50)
        monsters.append(d)
        x = x +55
    count = count -1
    

while not game_over:
    ball.fill()                                           
    platform.fill()
    if ball.rect.y > 350:
        text_lose = Label(150, 150, 50, 50)
        text_lose.set_text("lozer", 60,(200, 0, 0))
        text_lose.draw(10,10)
        game_over = True

    if len(monsters) == 0:
        text_lose = Label(150, 150, 50, 50)
        text_lose.set_text("winer", 60,(80, 64, 91))
        text_lose.draw(10,10)
        game_over = True
            



    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            game_over = True

        if event.type== pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:#якщо натиснута клавіша
                move_right = True #піднімаємо прапор

            if event.key == pygame.K_LEFT:
                move_left = True #піднімаємо прапор

        elif event.type== pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False #опускаємо прапор

            if event.key == pygame.K_LEFT:
                move_left =False #опускаємо прапор
 
    if move_right:#прапор руху вправо
        platform.rect.x += 5
        
    if move_left:#прапор руху вліво
        platform.rect.x -= 5

    #додаємо постійне прискорення м'ячу по x і y
    ball.rect.x += dx
    ball.rect.y += dy

    #якщо м'яч досягає меж екрана, міняємо напрямок його руху
    if ball.rect.y < 0:
        dy *=-1
    if ball.rect.x >450 or ball.rect.x <0:
        dx *=-1
    #якщо м'яч торкнувся ракетки, міняємо напрямок  руху
    if ball.rect.colliderect(platform.rect):
        dy *=-1

    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *=-1 




  



    platform.draw()
    ball.draw()
    
    pygame.display.update()
    clock.tick(40)