import turtle
import random
import time

enemy_move_timer = 0
enemy_move_delay = 0.16

# Screen setup
screen = turtle.Screen()
screen.title("Space Invaders - Polished")
screen.bgcolor("black")
screen.setup(width=800, height=700)
screen.tracer(0)

# Score + Lives
score = 0
lives = 3
level = 1

pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(-340, 310)


def update_score():
    pen.clear()
    pen.write(f"Score: {score}   Lives: {lives}   Level: {level}",
              align="left", font=("Arial", 14, "normal"))


update_score()

# Player
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.setheading(90)
player.goto(0, -260)
player_speed = 25

# Bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(0.2, 0.8)
bullet.penup()
bullet.hideturtle()
bullet_speed = 30
bullet_state = "ready"

# Enemy Bullet
enemy_bullet = turtle.Turtle()
enemy_bullet.shape("square")
enemy_bullet.color("orange")
enemy_bullet.shapesize(0.2, 0.8)
enemy_bullet.penup()
enemy_bullet.hideturtle()
enemy_bullet_speed = 15
enemy_bullet_state = "ready"

# Bunkers (Defensive Barriers)
blocks = []


def create_bunkers():
    global blocks
    blocks = []

    # 3 bunkers spaced out across the screen
    bunker_x_positions = [-200, 0, 200]
    bunker_y = -150

    shape = [
        "XXXXX",
        "XXXXX",
        "XX XX",
        "XX XX"
    ]

    for bx in bunker_x_positions:
        for row_idx, row in enumerate(shape):
            for col_idx, char in enumerate(row):
                if char == "X":
                    block = turtle.Turtle()
                    block.shape("square")
                    block.color("green")
                    block.shapesize(0.5, 0.5)
                    block.penup()

                    x = bx - 25 + (col_idx * 12)
                    y = bunker_y - (row_idx * 12)
                    block.goto(x, y)
                    blocks.append(block)


create_bunkers()

# Enemies
enemies = []


def create_enemies():
    global enemies
    enemies = []
    rows = min(3 + level, 5)
    cols = 6

    for row in range(rows):
        for col in range(cols):
            enemy = turtle.Turtle()
            enemy.shape("circle")
            enemy.color("red")
            enemy.penup()
            enemy.goto(-180 + col * 60, 250 - row * 50)
            enemies.append(enemy)


create_enemies()
enemy_speed = 1.5


# Controls
def move_left():
    x = player.xcor() - player_speed
    if x > -330:
        player.setx(x)


def move_right():
    x = player.xcor() + player_speed
    if x < 330:
        player.setx(x)


def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()


def restart_game():
    global score, lives, level, enemy_speed, game_state, bullet_state, enemy_bullet_state, enemy_move_delay

    if game_state == "game_over":
        # 1. Hide leftover enemies and clear the list
        for enemy in enemies:
            enemy.hideturtle()
        enemies.clear()

        # 2. Hide leftover blocks and clear the list
        for block in blocks:
            block.hideturtle()
        blocks.clear()

        # 3. Hide bullets and clear the Game Over text
        bullet.hideturtle()
        bullet_state = "ready"
        enemy_bullet.hideturtle()
        enemy_bullet_state = "ready"
        game_over.clear()

        # 4. Reset all stats
        score = 0
        lives = 3
        level = 1
        enemy_speed = 1.5
        enemy_move_delay = 0.16

        # 5. Re-center player and spawn fresh assets
        player.goto(0, -260)
        create_enemies()
        create_bunkers()
        update_score()

        # 6. Flip the switch back to playing
        game_state = "playing"


screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")
screen.onkeypress(restart_game, "r")


# Collision
def is_collision(a, b):
    return a.distance(b) < 20


# Game Over Screen Setup
game_over = turtle.Turtle()
game_over.hideturtle()
game_over.color("white")

# Game loop
game_state = "playing"

while True:
    screen.update()
    time.sleep(0.017)

    if game_state == "playing":

        # Move enemies
        enemy_move_timer += 0.017

        if enemy_move_timer >= enemy_move_delay:
            edge_hit = False

            for enemy in enemies:
                enemy.setx(enemy.xcor() + enemy_speed)
                if enemy.xcor() > 330 or enemy.xcor() < -330:
                    edge_hit = True

            if edge_hit:
                enemy_speed *= -1
                for enemy in enemies:
                    enemy.sety(enemy.ycor() - 30)

            enemy_move_timer = 0

        # Move bullet
        if bullet_state == "fire":
            bullet.sety(bullet.ycor() + bullet_speed)

        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)

        # Enemy Firing Logic
        if enemy_bullet_state == "ready" and len(enemies) > 0:
            if random.randint(1, 50) == 1:
                shooter = random.choice(enemies)
                enemy_bullet.goto(shooter.xcor(), shooter.ycor() - 10)
                enemy_bullet.showturtle()
                enemy_bullet_state = "fire"

        # Move enemy bullet
        if enemy_bullet_state == "fire":
            enemy_bullet.sety(enemy_bullet.ycor() - enemy_bullet_speed)

        if enemy_bullet.ycor() < -300:
            enemy_bullet.hideturtle()
            enemy_bullet_state = "ready"

        # Check if enemy bullet hits the player
        if is_collision(enemy_bullet, player):
            enemy_bullet.hideturtle()
            enemy_bullet_state = "ready"
            enemy_bullet.goto(0, -400)
            lives -= 1
            update_score()

        # Check if Player Bullet hits a Bunker
        for block in blocks[:]:
            if is_collision(bullet, block):
                bullet.hideturtle()
                bullet_state = "ready"
                bullet.goto(0, -400)

                block.hideturtle()
                blocks.remove(block)
                break

                # Check if Enemy Bullet hits a Bunker
        for block in blocks[:]:
            if is_collision(enemy_bullet, block):
                enemy_bullet.hideturtle()
                enemy_bullet_state = "ready"
                enemy_bullet.goto(0, -400)

                block.hideturtle()
                blocks.remove(block)
                break

        # Check collisions (Player Bullet vs Enemy / Player vs Enemy)
        for enemy in enemies[:]:
            if is_collision(bullet, enemy):
                bullet.hideturtle()
                bullet_state = "ready"
                bullet.goto(0, -400)

                enemy.hideturtle()
                enemies.remove(enemy)

                score += 10
                update_score()
                break

            if is_collision(player, enemy):
                lives -= 1
                update_score()

                enemy.hideturtle()
                enemies.remove(enemy)
                break

            if enemy.ycor() < -230:
                lives -= 1
                update_score()

                enemy.hideturtle()
                enemies.remove(enemy)
                break

        # Level cleared
        if len(enemies) == 0:
            level += 1
            enemy_speed = 1.5 if enemy_speed > 0 else -1.5
            enemy_move_delay = max(0.05, enemy_move_delay * 0.8)
            create_enemies()

            # Optional: You can rebuild bunkers here too if you want fresh defenses each wave!
            # for block in blocks: block.hideturtle()
            # create_bunkers()

            update_score()

        # Game over
        if lives <= 0:
            game_state = "game_over"
            game_over.write("GAME OVER\nPress 'r' to Restart", align="center", font=("Arial", 30, "bold"))