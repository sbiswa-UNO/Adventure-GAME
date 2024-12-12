import pygame
from coin import Coin
from slashProjectile import SlashProjectile
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
GRAVITY = 0.75

# Define player action variables
moving_left = False
moving_right = False

# Define colors
BG = (57, 170, 198)
RED = (66, 193, 62)

def draw_bg() -> None:
    """
    Draw the background of the game, including the ground line.
    """
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300), 20)

def save_data() -> None:
    """
    My Creation
    Save the current game data to a file.
    """
    print("save data called")
    with open("game_data.txt", "r+") as file:
        lines = file.readlines()
        lines[0] = f"Coin_Amount: {coin_amount}\n"
        file.seek(0)
        file.writelines(lines)
        file.truncate()

class Character(pygame.sprite.Sprite):
    def __init__(self, char_type: str, x: int, y: int, scale: float, speed: int) -> None:
        """
        Initialize a character sprite.

        Args:
            char_type (str): Type of the character (e.g., "Player").
            x (int): Initial x-coordinate.
            y (int): Initial y-coordinate.
            scale (float): Scale factor for the character's size.
            speed (int): Movement speed of the character.
        """
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.attacking = False
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.slash_projectiles_list = []
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        animations = ["Idle1", "Run", "Jump", "Attack1"]
        for animation in animations:
            temp_list = []
            for i in range(len(os.listdir(f'img/{self.char_type}/{animation}'))):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def get_data(self) -> list[int]:
        """
        My Creation.
        Retrieve saved game data.

        Returns:
            list[int]: A list containing game data (e.g., coin amount).
        """
        try:
            print("getting data")
            with open("game_data.txt", "r") as file:
                data = []
                lines = file.readlines()
                for line in lines:
                    output = line.split()
                    if output[0] == "Coin_Amount:":
                        data.append(int(output[1]))
                return data
        except FileNotFoundError:
            print("file not found")
            with open("game_data.txt", "w") as file:
                file.writelines("Coin_Amount: 0\n")
            return self.get_data()

    def move(self, moving_left: bool, moving_right: bool) -> None:
        """
        Handle the character's movement.

        Args:
            moving_left (bool): Whether the character is moving left.
            moving_right (bool): Whether the character is moving right.
        """
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self) -> None:
        """
        Update the character's animation by cycling through frames.
        """
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            if self.attacking:
                # My creation
                if self.frame_index == int(len(self.animation_list[self.action])/2):
                    temp_slash = SlashProjectile(self.rect.x, self.rect.y, 0.25, self.flip, screen)
                    self.slash_projectiles_list.append(temp_slash)

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def update_action(self, new_action: int) -> None:
        """
        Change the character's current action.

        Args:
            new_action (int): Index of the new action.
        """
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self) -> None:
        """
        Draw the character on the screen.
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class CoinCounter:
    def __init__(self) -> None:
        """
        My Creation
        Initialize the coin counter.
        """
        self.font = pygame.font.SysFont("Arial", 35)
        self.coin_counter = self.font.render(f"COINS: {coin_amount}", False, (255, 255, 255))

    def draw(self) -> None:
        """
        Draw the coin counter on the screen.
        """
        screen.blit(self.coin_counter, (350, 5))

            

player = Character("Player", 200, 200, 3, 5)

#My Creation
playerData = player.get_data()
coin_amount = playerData[0]
#Enemy = Character(400, 200, 3, 5, "Enemies/Hobbit/pngs/Hobbit - Idle1.png")
coins_arr = [Coin(random.randint(30, 780), random.randint(20, 280), 1.5, screen) for i in range(20)]

run = True
while run:
    """Game Loop"""

    clock.tick(FPS)

    draw_bg()

    #My Creation
    coin_counter = CoinCounter()
    coin_counter.draw()

    player.update_animation()

    #My creation
    if len(coins_arr) < 20:
       coins_arr.append(Coin(random.randint(30, 780), random.randint(20, 280), 1.5, screen))

    #My Creation
    for coin in coins_arr:
        coin.draw()
        coin.update_animation()
        coin.move()
        if player.rect.colliderect(coin.rect):
            coin_amount += 1
            coins_arr.remove(coin)

    #My Creation
    for slash in player.slash_projectiles_list:
        slash.draw()
        slash.move()
        if slash.rect.x < 0 or slash.rect.x > (800-slash.rect.width):
            player.slash_projectiles_list.remove(slash)

    player.draw()
    #Enemy.draw()

    #player actions depending on player alive status
    if player.alive:
        if player.in_air:
            player.update_action(2)

        #My creation
        elif player.attacking:
            player.update_action(3)

        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:

            save_data() #My creation

            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            player.attacking = True
        if event.type == pygame.MOUSEBUTTONUP:
            player.attacking = False
        #keyboard presses

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w or event.key == pygame.K_SPACE and player.alive: #I added in the ability to use SPACEBAR as a jump button
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                save_data()
                run = False

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            
    pygame.display.update()

pygame.quit()
