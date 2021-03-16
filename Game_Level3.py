#Color Switch
#Created by: Henok Guluma, Pearl Rwauya
import pygame
import pygame.gfxdraw
import math
import random

file='star.OGG'
file2='bling.OGG'
file3='colorswitch.OGG'
file4='background1.OGG'
#These are sound files
path='C:/Users/Henok Taddesse/Documents/Final Project/'
pygame.init()
pygame.mixer.init()
sound=pygame.mixer.Sound(path+file4)
for i in range(4):
    sound.play()
#We play the background song starting from this point.

pygame.font.init()
WID, HGT = 510,720
screen = pygame.display.set_mode((WID, HGT))
pygame.display.set_caption("Color Switch")
font = pygame.font.Font(None, 24)
menu_font = pygame.font.Font(None, 40)

P = (150, 25, 255)
Y = (250, 225, 15)
B = (0, 0, 0)
W = (255, 255, 255)
R = (255, 0, 128)
T = (53, 226, 242)
#These are the colors used.
circles = [] 
prizes = []
shifters = []
MENU, PLAY, PAUSE, GAMEOVER = range(4)
game = MENU
score = 0
high = 0

class Position:
    #This is to help us keep track of the ball and the objects falling. 
    def __init__(self):
        self.x = 0
        self.y = 0

pos = Position()
#The class is initialized.      
class Ball:
    def __init__(self, surface, x=250, y=400):
        self.x = x
        self.y = y
        self.rad = 10
        self.surface = surface
        self.vel = 8
        self.color = randcolor() #This is a function that will be declared later.
        self.over = False
        self.over_count = 0
        self.scatter = []
        
    def collide(self):
        if self.y>700:
            self.end()
            #If the ball falls off the screen, it dies. 
        global score   #obtains the score from global scope.
        x, y = self.x-pos.x, self.y-pos.y
        for prize in prizes:
            if(prize.y+16 >= self.y):
                prize.color = B
                #If the star is touched by the ball, it is eaten. 
                if(not prize.over):
                    score+=10
                    sound1=pygame.mixer.Sound(path+file)
                    sound1.play()
                    #beep sound played when the star is eaten. 
                prize.over = True
        for circle in circles:
            if(circle.y+int(circle.rad/2) >= self.y and circle.y+int(circle.rad/2)-25 <= self.y):
                #this case is when the ball is touching the bottom part of the circle. 
                if(self.color != Y and circle.angle > 90 and circle.angle <= 180):
                    self.end()
                    #This checks how much the circle has rotated from initial position using self.angle and determines what color should be at the bottom 
                    #of the circle. If the ball's color doesn't match this color then the ball dies. Notice later that self.angle is reset each time it 
                    #exceeds 360 degrees. 
                elif(self.color != P and circle.angle > 180 and circle.angle <= 270):
                    self.end()
                elif(self.color != R and circle.angle > 270 and circle.angle <= 360):
                    self.end()
                elif(self.color != T and circle.angle <= 90):
                    self.end()
            elif(circle.y-(circle.rad/2)+25 >= self.y-self.rad and circle.y-(circle.rad/2) <= self.y):
                #this case is when the ball is touching the top part of the circle. 
                if(self.color != R and circle.angle > 90 and circle.angle <= 180):
                    self.end()
                elif(self.color != T and circle.angle > 180 and circle.angle <= 270):
                    self.end()
                elif(self.color != Y and circle.angle > 270 and circle.angle <= 360):
                    self.end()
                elif(self.color != P and circle.angle <= 90):
                    self.end()
               
        for colors in shifters:
            if(colors.y >= self.y-self.rad*2):
                #if the shifters are touched by the ball then the color of the ball will change to the color assigned to the shifter which is randomly assigned.
                sound2=pygame.mixer.Sound(path+file3)
                sound2.play()
                self.color = colors.color
                shifters.remove(colors)
                
             
    def end(self):
        sound3=pygame.mixer.Sound(path+file2)
        #crushing sound 
        sound3.play()
        self.dying_count = 0
        self.over = True
        for i in range(50):
            temp = Scatter(self.surface, self.x, self.y)
            #This is a class that will be declared later. 
            self.scatter.append(temp)
        
    def update(self):
        if(not self.over):
            self.vel -= 0.4
            #each time the ball is updated it falls down by this speed. 
            self.y -= self.vel
            if(pos.y >= self.y-HGT/2):
                #This makes sure that the ball can't move more than half of the screen by updating the position object and fixing the ball in the process. The updated
                #position object will affect things like circles, stars and shifters. 
                pos.y = self.y-HGT/2
            self.collide()
        elif(self.over and self.over_count <= 80):
            self.over_count+=1
            for sc in self.scatter:
                sc.update()
        else:
            global score, high, game
            game = GAMEOVER
            if(score > high):
                high = score
        
    def draw(self):
        x = int(self.x-pos.x)
        y = int(self.y-pos.y)
        #This is where the ball fixation happens, by subtracting the position coordinate from the ball coordinate. 
        if(self.y > 10000):
            self.y = 9000
        if(not self.over):
            pygame.gfxdraw.aacircle(self.surface, x, y, self.rad, self.color)
            pygame.gfxdraw.filled_circle(self.surface, x, y, self.rad, self.color)
            #This is a method referenced from a source where it helps us draw filled circles with specific colors. 
        elif(self.over_count <= 80):
            dc = self.over_count
            for ball in self.scatter:
                ball.draw()


       
class Circle:
    def __init__(self, surface, vel, rad, thick, x=250, y=150, angle = 0):
        self.x = x
        self.y = y
        self.rad = rad
        self.angle = angle
        self.surface = surface
        self.vel = vel
        self.thickness = thick
        
    def update(self):
        x, y = (self.x-float(self.rad/2)-pos.x, self.y-float(self.rad/2)-pos.y)
        if(y >= HGT):
            circles.remove(self)
            return
            #this removes each circle when they run out of bounds of the screen. 
        self.angle+=self.vel
        if(self.angle > 360):
            #here is where the angle is reset each time it does one full rotation. 
            self.angle-=360
        elif(self.angle <= 0):
            #This avoids negative angles. 
            self.angle+=360
            # self.vel*=-1
        
        
    def draw(self):
        x, y = (self.x-float(self.rad/2)-pos.x, self.y-float(self.rad/2)-pos.y)
        x, y = int(x), int(y)
        thick = self.thickness
        #This method allows us to draw arcs. Arcs corresponding to each color were drawn twice to give the circle a more graceful appearance.
        #Drawing arcs side to side and allowing them to rotate along with each other creates the illusion of a circle with different colors rotating.
        pygame.draw.arc(self.surface, P , (x, y, self.rad, self.rad), math.radians(0+self.angle) ,math.radians(90+self.angle), thick)
        pygame.draw.arc(self.surface, P , (x, y+1, self.rad, self.rad), math.radians(0+self.angle) ,math.radians(90+self.angle), thick)
        pygame.draw.arc(self.surface, Y , (x, y, self.rad, self.rad), math.radians(90+self.angle) , math.radians(180+self.angle), thick)
        pygame.draw.arc(self.surface, Y , (x, y+1, self.rad, self.rad), math.radians(90+self.angle) ,math.radians(180+self.angle), thick)
        pygame.draw.arc(self.surface, T , (x, y, self.rad, self.rad), math.radians(180+self.angle) ,math.radians(270+self.angle), thick)
        pygame.draw.arc(self.surface, T , (x, y+1, self.rad, self.rad), math.radians(180+self.angle) ,math.radians(270+self.angle), thick)
        pygame.draw.arc(self.surface, R , (x, y, self.rad, self.rad), math.radians(270+self.angle) ,math.radians(360+self.angle), thick)
        pygame.draw.arc(self.surface, R , (x, y+1, self.rad, self.rad), math.radians(270+self.angle) ,math.radians(360+self.angle), thick)
        
        
        pygame.gfxdraw.aacircle(self.surface, int(self.x-pos.x), int(self.y-pos.y), int(self.rad/2)+1, (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, int(self.x-pos.x), int(self.y-pos.y), int(self.rad/2), (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, int(self.x-pos.x), int(self.y-pos.y), int(self.rad/2)-thick-1, (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, int(self.x-pos.x), int(self.y-pos.y), int(self.rad/2)-thick, (20,20,20))
        #This extra graphics component maintains the smooth texture of the circle. 
class Circle1(Circle):
	def update(self):
		x, y = (self.x-float(self.rad/2)-pos.x, self.y-float(self.rad/2)-pos.y)
		if(y >= HGT):
			circles.remove(self)
			return
            #this removes each circle when they run out of bounds of the screen. 
		self.angle+=self.vel
		if(self.angle > 360):
			#here is where the angle is reset each time it does one full rotation. 
			self.angle-=360
		elif(self.angle==180):
			self.vel*=-1
		elif(self.angle <= 0):
			self.angle+=360
            #This avoids negative angles. 
class Prize:
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.surface = surface
        self.color = W
        self.over = False
        self.over_count = 0
        
    def update(self):
        if(self.over and self.over_count < 40):
            self.over_count+=1
        elif(self.over):
            prizes.remove(self)
        #This helps maintiain the prizes list. 
        
    def draw(self):
        x,y = self.x-pos.x,self.y-pos.y
        if(not self.over):
            pts = ((x,y-8),(x-3.5,y-2.5), (x-10,y-1.5), (x-5.5,y+4), (x-6.5, y+10.5), (x, y+8), (x+6.5, y+10.5), (x+5.5, y+4), (x+10, y-1.5), (x+3.5,y-2.5))
            #These are six different points for the coordinates of the star. 
            pygame.gfxdraw.aapolygon(self.surface, pts, self.color)
            pygame.gfxdraw.filled_polygon(self.surface, pts, self.color) 
        else:
            #When the star is eaten then the +10 mark will appear and fade eventually, the fading is accomplished by using a counter to control the color. 
            self.surface.blit(font.render("+10", True, (255-self.over_count*5, 255-self.over_count*5, 255-self.over_count*5)), (x-10,y-self.over_count))
      
def pizza(x, y, rad, sa, ea, color):
    #It draws a circle with slices of different color. 
    pts = [(x,y)]
    for n in range(sa, ea+1):
        f1 = x + int(rad*math.cos(math.radians(n)))
        f2 = y + int(rad*math.sin(math.radians(n)))
        #These are coordinates for drawing slices. 
        pts.append((f1, f2))
    pts.append((x,y))
    if(len(pts)>2):
        pygame.gfxdraw.aapolygon(screen, pts, color)
        pygame.gfxdraw.filled_polygon(screen, pts, color)
        
def randcolor():
    #It gives back a random color
    rand = random.randint(0,3)
    if(rand == 0):
        return P
    elif(rand == 1):
        return R
    elif(rand == 2):
        return T
    elif(rand == 3):
        return Y
      
class Shifter:
    def __init__(self, surface, x, y, color = randcolor()):
        self.x = x
        self.y = y
        self.surface = surface
        self.rad = 15
        self.color = color
        
    def draw(self):
        x, y = int(self.x-pos.x), int(self.y-pos.y)
        pizza(x, y, self.rad, 0, 90, R)
        pizza(x, y, self.rad, 90, 180, T)
        pizza(x, y, self.rad, 180, 270, Y)
        pizza(x, y, self.rad, 270, 360, P)
        #The four slices of the shifter have their own colors.
        pygame.gfxdraw.aacircle(self.surface, x, y,self.rad-1, (19,19,19))
        pygame.gfxdraw.aacircle(self.surface, x, y,self.rad, (19,19,19))
        

      
class Scatter:
    def __init__(self, surface, x=250, y=400):
        self.x = x
        self.y = y
        self.rad = random.randint(2,5)
        self.surface = surface
        self.vel = [random.randint(-25,25),random.randint(-25,25)]
        self.color = randcolor()
        
    def draw(self):
        x, y = int(self.x-pos.x), int(self.y-pos.y)
        #The position that these scatter balls are drawn is with respect to the coordinates of the position object. 
        pygame.gfxdraw.aacircle(self.surface, x, y, self.rad, self.color)
        pygame.gfxdraw.filled_circle(self.surface, x, y, self.rad, self.color)
        
    def update(self):
        X,Y = 0,1
        self.vel[Y] += 0.6
        self.x += self.vel[X]
        if(self.x >= WID or self.x <= 0):
            self.vel[X] = -self.vel[X]
            #This just gives the balls touching the walls a bouncing effect. 
        self.y += self.vel[Y]
        
color_switch = Shifter(screen, WID/2, 250)

def restart(): 
    #This function is called each time the game is initiated. Most of the initializations of the classes defined earlier happens here. 
    global pos, ball, circles, score, prizes
    pos = Position()
    ball = Ball(screen)
    del prizes[:]
    del circles[:]
    del shifters[:]
    #We reset the lists where we append other stuffs later. 
    randno=[[-3, 270, 22], [-2, 220, 19], [-1.5, 170, 16], [1.5, 170, 16], [2, 220, 19], [3, 270, 22]]
    #This is just to establish two ways of the circles rotation(clockwise and couterclockwise) and different sizes and speeds. 
    for i in range(100):
        r=randno[random.randint(0, 5)]
        s=r[0]
        t=r[1]
        u=r[2]
        ob=[Circle(screen, s, t, u, WID/2, -500*i), 
        Circle(screen, s, t, u, WID/2, -500*i), 
        Circle1(screen, s, t, u, WID/2, -500*i)]
        #Here we have appended 100 circle objects each with separation of 500 units. 
        a=random.randint(0, 2)
        circles.append(ob[a])
        temp_Shifter = Shifter(screen, WID/2, -500*i+300, randcolor())
        #Here we have appended 100 shifters each with separation of 500 units from each other and 300 units below each circle. 
        temp_prize = Prize(screen, WID/2, -500*i)
        prizes.append(temp_prize)
        shifters.append(temp_Shifter)
    #We also reset the score here.     
    score = 0
    
def state():
    global game
    for e in pygame.event.get():
        #depending on the key pressed different events occur. 
        if(e.type == pygame.QUIT):
            return False
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                return False
            elif(e.key == pygame.K_UP):
                if(game == PLAY):
                    ball.vel = 7
                elif(game == GAMEOVER):
                    restart()
                    game = PLAY
                elif(game == MENU):
                    restart()
                    game = PLAY
    return True

def draw_score():
    screen.blit(font.render("Score: "+str(score), True, W), (10, 10))
    #It draws score at the left top edge of the screen. 
    if(high >= 10):
        hig=high/10
        #This here draws broken lines to show where exactly the highscore position is. 
        w = WID/5
        for i in range(6):
            pygame.draw.line(screen, (100, 100, 100), (w*i-20-pos.x, -500*(hig-1)-pos.y), (w*i+20-pos.x, -500*(hig-1)-pos.y), 5)
    
x, y = int(WID/2), int(HGT/2)

def draw_menu():
    screen.fill((0, 0, 0))
    bg=pygame.image.load(path+"picture7.png").convert_alpha()
    #This displays the menu. 
    screen.blit(bg, (0, 0))
def draw_game_over():
    #when the game is over this picture is displayed along with score and highscore. 
    screen.fill((0, 0, 0))
    bg=pygame.image.load(path+"picture6.png").convert_alpha()
    screen.blit(bg, (0, 0))
    screen.blit(menu_font.render(str(score), True, W), (WID/2-150, 200))
    screen.blit(menu_font.render(str(high), True, W), (WID/2-150, 340))
    
clock = pygame.time.Clock()
while(state()):
    #The clock tick helps a smooth transition between one event run and the next within the while loop. 
    clock.tick(80)
    screen.fill((10,10,10))
    if(game == MENU):
        draw_menu()
    #after this, while the game state is play each object is updated and drawn. 
    elif(game == PLAY):
        for circle in circles:
            circle.update()    
        ball.update()
        for prize in prizes:
            prize.update()
            
        for circle in circles:
            if(circle.y+circle.rad/2-pos.y >= 0 and circle.y-circle.rad/2-pos.y <= HGT):
                circle.draw()
        for prize in prizes:
            if(prize.y+13-pos.y >= 0 and prize.y-13-pos.y <= HGT):
                prize.draw()
        for colors in shifters:
            if(colors.y+colors.rad-pos.y >= 0 and colors.y-colors.rad-pos.y <= HGT):
                colors.draw()
        ball.draw()
        draw_score()
        
    elif(game == GAMEOVER):
        draw_game_over()
        
    pygame.display.flip()
    
pygame.quit()