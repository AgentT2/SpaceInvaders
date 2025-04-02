import tkinter as tk
from PIL import Image, ImageTk
import random

# Constants
WIDTH = 800
HEIGHT = 500
PLAYER_SPEED = 40
BULLET_SPEED = 10
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
ENEMY_SPEED = 1
ENEMY_FIRE_RATE = 2000
ENEMY_BULLET_SPEED = 10
ENEMY_SPAWN_RATE = 1000  # New constant: milliseconds between enemy spawns

root = tk.Tk()
root.title("Elite Invaders")

# Create canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Load and add background image
bg_image = Image.open("space1.png")
bg_resize = bg_image.resize((WIDTH, HEIGHT))
bg_photo = ImageTk.PhotoImage(bg_resize)
canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)

# Load and add player spaceship
original_img = Image.open("playerSpace.png")
resize_img = original_img.resize((80, 80))
spaceship_img = ImageTk.PhotoImage(resize_img)

player_x = WIDTH // 2
player_y = HEIGHT - 60
player = canvas.create_image(player_x, player_y, image=spaceship_img)

# ENEMY SPACESHIP
enemy_img = Image.open("enermy.png").resize((60,60))
rotate_img = enemy_img.rotate(270)
enemy_photo = ImageTk.PhotoImage(rotate_img)

bullets = []  # list for player bullets
enemies = []
enemy_bullets = []

# Move player function
def move_player(event):
    global player_x
    if event.keysym == "Left" and player_x > 40:
        player_x -= PLAYER_SPEED
    elif event.keysym == "Right" and player_x < WIDTH - 40:
        player_x += PLAYER_SPEED
    canvas.coords(player, player_x, player_y)

def shoot_bullets(event):
    bullet_x = player_x
    bullet_y = player_y - 40
    bullet = canvas.create_rectangle(
        bullet_x - BULLET_WIDTH // 2, bullet_y - BULLET_HEIGHT,
        bullet_x + BULLET_WIDTH // 2, bullet_y,
        fill="white"
    )
    bullets.append(bullet)
    mov_bullet(bullet)

def mov_bullet(bullet):
    if canvas.coords(bullet)[1] > 0:
        canvas.move(bullet, 0, -BULLET_SPEED)
        root.after(50, mov_bullet, bullet)
    else:
        canvas.delete(bullet)
        bullets.remove(bullet)

def spawn_enemy():
    enemy_x = random.randint(50, WIDTH-50)
    enemy_y = 50
    enemy = canvas.create_image(enemy_x, enemy_y, image=enemy_photo)
    enemies.append(enemy)
    move_enemy(enemy)
    # Schedule next enemy spawn
    root.after(ENEMY_SPAWN_RATE, spawn_enemy)

def move_enemy(enemy):
    if canvas.coords(enemy)[1] < HEIGHT - 60:
        canvas.move(enemy, 0, ENEMY_SPEED)
        root.after(50, move_enemy, enemy)
    else:
        canvas.delete(enemy)
        enemies.remove(enemy)

def enemy_shoot():
    if enemies:
        enemy = random.choice(enemies)
        enemy_x, enemy_y = canvas.coords(enemy)
        bullet = canvas.create_rectangle(
            enemy_x - BULLET_WIDTH // 2, enemy_y + BULLET_HEIGHT,
            enemy_x + BULLET_WIDTH // 2, enemy_y + BULLET_HEIGHT*2,
            fill="red"
        )
        enemy_bullets.append(bullet)  # Fixed: was appending to wrong list
        move_enemy_bullet(bullet)
    
    root.after(ENEMY_FIRE_RATE, enemy_shoot)

def move_enemy_bullet(bullet):
    if canvas.coords(bullet)[1] < HEIGHT:
        canvas.move(bullet, 0, ENEMY_BULLET_SPEED)
        root.after(50, move_enemy_bullet, bullet)
    else:
        canvas.delete(bullet)
        enemy_bullets.remove(bullet)

# Bind keys
root.bind("<Left>", move_player)
root.bind("<Right>", move_player)
root.bind("<Up>", shoot_bullets)

# Keep a reference to the images
canvas.bg_photo = bg_photo
canvas.spaceship_img = spaceship_img
canvas.enemy_photo = enemy_photo

# Start the game
spawn_enemy()  # Initial enemy spawn will trigger continuous spawning
enemy_shoot()

# Run game loop
root.mainloop()