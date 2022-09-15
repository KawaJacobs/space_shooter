
import pygame, random, string
pygame.display.set_caption("Space Shooter")
HEIGHT = 500
WIDTH = 500
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullets = []
enemies = []

class Circle:
    def __init__(self,x,y,radious):
        self.x = x
        self.y = y
        self.radious = radious
        self.r = 255
        self.g = 255
        self.b = 255
    def draw(self):
        return pygame.draw.circle(screen,(self.r,self.g,self.b),(self.x,self.y),self.radious)

class Bullet:
    def __init__(self, posx, posy, velx, vely):
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.txt = pygame.Rect(self.posx, self.posy, 5, 5)
        self.display_texture = True
        self.check_for_collisions = True

    def draw(self):
        return pygame.draw.rect(screen, (int("e6",16),int("ff",16),int("03",16)), self.txt)
    def update(self):
        self.txt = pygame.Rect(self.posx, self.posy, 5, 5)
    def destroy(self):
        self.display_texture = False
        self.check_for_collisions = False


class Ship:
    def __init__(self, posx, posy, shoting_mode, team):
        self.sizex = 20
        self.sizey = 20
        self.posx = posx
        self.posy = posy
        self.team = team
        self.enemy_shoot_timer = 0
        self.shoting_mode = shoting_mode
        self.txt = pygame.Rect(self.posx, self.posy, self.sizex,self.sizey)
        self.shot_timer = 0
        self.check_for_collisions = True
        self.display_texture = True
        self.color = RED
    def draw(self):
        return pygame.draw.rect(screen, self.color, self.txt)
    def shot(self,offset):
        self.direction = 4.0
        if self.team == 1:
            self.direction = -self.direction
        if self.shoting_mode == "--":
            bullets.append(Bullet(self.posx+self.sizex/2-5, self.posy-self.sizey+offset+10, 0.0,self.direction))
        elif self.shoting_mode == "-:":
            for i in range(-2,3):
                bullets.append(Bullet(self.posx+self.sizex/2-5, self.posy - self.sizey+10+offset,float(i),self.direction))
    def update(self):
        self.txt = pygame.Rect(self.posx, self.posy, self.sizex,self.sizey)
    def move_right(self):
        self.posx += 5.0
    def move_left(self):
        self.posx -= 5.0
    def destroy(self):
        self.check_for_collisions = False
        self.display_texture = False

player = Ship(float(WIDTH/2),float(HEIGHT-30),"-:", 1,)
exp = []

def explode(x,y):
    exp.append(Circle(x,y,random.randint(18,25)))

def redraw_window():
    screen.fill(BLACK)
    for e in enemies:
        if e.display_texture:
            e.draw()
            e.update()
    for b in bullets:
        if b.display_texture:
            b.draw()
    for particle in exp:
        particle.draw()
    player.draw()
    pygame.display.update()

def Main():
    points = 0
    run = True
    x,y = pygame.mouse.get_pos()
    spawn_timer = 0
    spawn_time = 100
    break_timer = 0
    while run:
        clock.tick(FPS)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player.shot_timer >= 30:
            player.shot(0)
            player.shot_timer = 0
        elif keys[pygame.K_d]:
            player.move_right()
        elif keys[pygame.K_a]:
            player.move_left()

        for b in bullets:
            b.posy += int(b.vely)
            b.posx += int(b.velx)
            b.update()
            for e in enemies:
                if b.posx + 5 >= e.posx and b.posx  <= e.posx +20 and b.posy >= e.posy and b.posy <= e.posy +20 and e.check_for_collisions and b.check_for_collisions:
                    e.destroy()
                    b.destroy()
                    explode(e.posx, e.posy)
                    points += 1
                    print(points)
            if b.posx + 5 >= player.posx and b.posx  <= player.posx +20 and b.posy >= player.posy and b.posy <= player.posy +20 and player.check_for_collisions and b.check_for_collisions:
              run = False
        if spawn_timer >= spawn_time:
            if break_timer < 3600:
                shoting_mode = random.randint(1,5)
                if shoting_mode == 1:
                    enemies.append(Ship(random.randint(0,WIDTH-20),-40,"-:",2))
                else:
                    enemies.append(Ship(random.randint(0, WIDTH - 20), -40, "--", 2))
                spawn_timer = 0
                if spawn_time >= 11:
                    spawn_time -= 1
            else:
                if break_timer >= 4100:
                    break_timer = 0
                    for i in range(0,len(enemies)-1):
                        enemies.pop(0)
                    for j in range(0,len(bullets)-1):
                        bullets.pop(0)
                    for k in range(0, len(exp)-1):
                        exp.pop(0)
        for enemy in enemies:
            enemy.posy += 1
            if player.posx + 5 >= enemy.posx and player.posx <= enemy.posx + 20 and enemy.posy <= player.posy <= enemy.posy + 20 and enemy.check_for_collisions:
                run = False
            if enemy.check_for_collisions:
                if enemy.enemy_shoot_timer == spawn_timer:
                    enemy.shot(30)
                    enemy.enemy_shoot_timer = 0
                enemy.enemy_shoot_timer += 1

        for explosion in exp:
            explosion.radious -= 1

        if player.posx + player.sizex >= WIDTH:
            player.posx = WIDTH - player.sizex
        if player.posx <= 0:
            player.posx = 0


        break_timer += 1
        spawn_timer += 1
        player.shot_timer += 1
        player.update()
        redraw_window()
Main()
