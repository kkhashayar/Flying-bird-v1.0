import turtle, random, math,  pygame, time, sys

WIDTH = 800
HEIGHT = 600

pygame.mixer.init()

images = ["b_down.gif","b_up.gif","b_up_left.gif",
          "b_down_left.gif","box_coin_gold_1.gif",
          "dead1.gif","c1.gif","c2.gif"]
for image in images:
    turtle.register_shape(image)

screen = turtle.Screen()
screen.bgcolor("blue")
screen.setup(WIDTH,HEIGHT)
screen.title("Flying bird 1")
screen.tracer(0)

bird_images_right = ["b_down.gif","b_up.gif",]
bird_images_left = ["b_up_left.gif","b_down_left.gif"]

cl_images = ["c1.gif","c2.gif"]

Gravity = 0.0007 

class Enemy(turtle.Turtle):
    def __init__(self, x,y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.shape("circle")
        self.x_size = 1
        self.y_size = 1
        self.shapesize(self.y_size,self.x_size,0)
        self.color("red")
        self.fillcolor("orange")
        self.setpos(x,y)
        self.setheading(180)
        self.speed = 00.4

    def update(self):
        self.forward(self.speed)
        if self.x_size == 1:
            self.x_size += 0.5
        if self.x_size == 2:
            self.x_size -= 0.5
        self.shapesize(self.y_size, self.x_size,0)


class Coin (turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape("box_coin_gold_1.gif")
        self.shapesize(0.5,0.5,0)
        #self.color("yellow")
        self.setpos(x,y)
        self.speed(0)
        self.setheading(-90)
        self.speed = 2

    def move(self):
        self.forward(self.speed)


class Energy_bar(turtle.Turtle):
    def __init__(self, h, w, x, y, color):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape("square")
        self.shapesize(h,w)
        self.color(color)
        self.setpos(x,y)
        self.setheading = 90
        self.h = h
        self.w = w

    def update(self):
        self.pensize(3)
        self.pendown()
        self.speed(5)
        self.forward(5)
        self.speed(0)
        self.penup()

class Platform(turtle.Turtle):
    def __init__ (self, h, w, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape("square")
        self.shapesize(h, w,2)
        self.setpos(x,y)
        self.color("black")
        self.fillcolor("green")
        self.speed(0)
        self.height = h

class Cloud(turtle.Turtle):
    def __init__ (self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape(random.choice(cl_images))
        self.setpos(x,y)
        self.shapesize(1)
        self.color("blue")
        self.fillcolor("blue")
        self.speed(0)
        self.setheading(180)
    
        
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("orange")
        self.shape("b_down.gif")
        self.fillcolor("blue")
        self.shapesize(2,2)
        self.setheading(90)
        self.penup()
        self.speed(0)
        self.thrust = 0.4
        self.dx = 0
        self.dy = 0
        self.terminal_velocity = -20
        self.jump = "yes"
        self.direction = "stop"
        self.speed = 0.2
        self.level_up = "no"
        self.life = "yes"

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2) + (b**2))
        if distance < 40:
            return True 
        else:
            return False
        
    def update(self):
        self.goto(self.xcor()+self.dx, self.ycor() + self.dy)

        #Set the ground level
        if self.ycor() <= -280 and self.life == "yes":
           self.dy = 0
           self.dx = 0
           self.sety(-280)
           self.jump = "yes"
           self.direction ="stop"
        if self.ycor() <= -280 and self.life == "no":
           self.dy = 0
           self.dx = 0
           self.sety(-330)
           self.jump = "yes"
           self.direction ="stop"
        if self.ycor() >= 280:
            self.sety(280)
        else:
            self.dy -= Gravity

        #Set Terminal velocity           
        if self.dy < self.terminal_velocity:
            self.dy = self.terminal_velocity
        if self.direction == "stop":
            self.speed = 0
        if self.direction == "left":
            self.speed = 0.09
            self.goto(self.xcor() - self.speed, self.ycor())
        if self.direction == "right":
            self.speed = 0.09
            self.goto(self.xcor() + self.speed, self.ycor())
        if self.xcor() > 150:
            self.setx(150)
        if self.direction == "left" and self.xcor() < -350:
            self.setx(-350)
        else:
            self.dy -= Gravity

    def accelerate_left(self):
        self.dx -= self.thrust * 0.18
    def accelerate_right(self):
        self.dx += self.thrust * 0.18

    def accelerate_up(self):
        if self.jump == "yes":
            self.dy += self.thrust

    def left(self):
        self.direction = "left"
    def right(self):
        self.direction = "right"  
    def stop(self):
        self.direction = "stop"     

# Objects

clouds = []
all_sprites = []
platforms = []
enemies = []
for cloud in range(4):
    clouds.append(Cloud(-280, 200))

#sounds
coin_sound = pygame.mixer.Sound("coin_s_1.wav")
hit_sound = pygame.mixer.Sound("vulture-1.wav")
enemy_sound = pygame.mixer.Sound("enemy1_coming.wav")
bg_sound = pygame.mixer.Sound("back_ground_1.ogg")

coins = []
for coin in range (1):
    coins.append(Coin(random.randrange(-200,-190 ), random.randrange(-100, 250)))

for platform in range(3):
    #(self, h, w, x, y)
    platforms.append(Platform(1, 5,
     random.randrange(100,400),-100))

for enemy in range (1):
    enemies.append(Enemy(random.randrange(420,430), random.randrange(-200,280)))
    
player = Player()
all_sprites.append(player)

# Key bindings
turtle.listen()
turtle.onkey(player.accelerate_left,"a")
turtle.onkey(player.accelerate_right,"d")
turtle.onkey(player.accelerate_up,"space")
turtle.onkey(player.left,"Left")
turtle.onkey(player.right,"Right")
turtle.onkey(player.stop,"Down")

# Infos , relative objects
#energy_bar = Energy_bar()
count = 0
hits = 0

#flying_bar = Bar(0.1,0.1,-227,290, "yellow")
p = turtle.Turtle()
p.hideturtle()
p.penup()
p.setpos(-227,270)
font = ("arial", "14", "bold")
font_game_over = ("arial", "26","bold")
p.color("gold")
p.write(" Flying bird  v1.0 by: Xerex Nar (K_N)", font = font)

def mouse_click_exit():
    p.color("black")
    p.setpos(-150,0)
    p.clear()
    p.write("mouse click to exit  ",font = font_game_over)

def pen_write_game_over():
    p.color("red")
    p.setpos(-100,0)
    p.clear()
    p.write(" GAME OVER ",font = font_game_over)

def pen_write_score():
    p.color("white")
    p.setpos(-227,270)
    p.clear()
    p.write("Score:  " + str(count),font = font ) # True, align = "center",

def pen_write_hits():
    p.color("black")
    p.setpos(-280, 270)
    p.clear()
    p.write("Hits: " + str(hits), font = font)

def pen_controllers():
    font_special = ("arial", "10", "bold")
    p.color("black")
    p.setpos(-250,280)
    p.clear()
    p.write("Space: fly    Left: left      Right: right   Down: stop flying   A: speedup to left    D: Speedup to right", font = font_special)

pen_controllers()
########################################
# Main function and game loop
def main():
    bg_sound.set_volume(0.01)
    bg_sound.play()
    
    global count, hits

    # Game loop
    running = True
    while running:
        screen.update()
        for cloud in clouds:
            cloud.forward(0.3)
            if cloud.xcor() < -450:
                cloud.hideturtle()
                clouds.remove(cloud)
                if len(clouds) < 2:
                    for cloud in range (2):
                        clouds.append(Cloud(random.randrange(450,1000,200), random.randrange(-300, -280)))
            
        for enemy in enemies:
            enemy.update()
            if enemy.xcor() < - 410:
                #enemy_sound.play()
                enemy.hideturtle()
                enemies.remove(enemy)
                if len(enemies)<1:
                    enemies.append(Enemy(random.randrange(420,430), random.randrange(-200,280)))
            if player.is_collision(enemy):
                enemy.hideturtle()
                enemy.goto(-400, -500)
                hits += 1                                
                hit_sound.play()
                pen_write_hits()

                if hits == 3:    
                    player.direction = "stop"
                    player.shape("dead1.gif")
                    player.sety(player.ycor()-20)
                    player.life = "no"
                    pen_write_game_over()
                    time.sleep(1)
                    running = False
                    mouse_click_exit()
                    screen.exitonclick()
                    quit()
                   
        for coin in coins:
            if player.is_collision(coin):
                coin_sound.play()
                count += 1
                coin.hideturtle()
                coin.setpos(-410,coin.ycor())
                pen_write_score()

        for platform in platforms:
            if player.is_collision(platform):
                ground = (platform.ycor() + (platform.height *20) +1)
                player.jump = "yes"
                player.dy = 0
                player.dx = 0 
                player.sety(ground)
                player.jump = "no"
                if player.direction == "right":
                    player.shape("b_down.gif")
                if player.direction == "left":
                    player.shape("b_down_left.gif")  
            else:
                if player.direction == "right":
                    player.shape(random.choice(bird_images_right))
                if player.direction == "left":
                    player.shape(random.choice(bird_images_left))
          
        if player.direction == "right":
            for platform in platforms:
                platform.goto(platform.xcor() - (player.speed), platform.ycor())
                if platform.xcor()<= -450:
                    platform.hideturtle()
                    platforms.remove(platform)
                    if len(platforms) <5:
                        platforms.append(Platform(1 , 5,
                            random.randrange(450,550,20), random.randrange(-200,200, 20)))
            for coin in coins:
                coin.goto(coin.xcor()-(player.speed)*2, coin.ycor())
                if coin.xcor() < -410:
                    coin.hideturtle()
                    coins.remove(coin)
                    if len(coins)< 3:
                        coins.append(Coin(random.randrange(410,500), random.randrange(-100, 250)))
        player.update()
    
if __name__ == "__main__":
    main()

