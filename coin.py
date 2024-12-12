import pygame

GRAVITY = 0.1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: float, screen: pygame.Surface) -> None:
        """
        My creatoin
        Initialize a Coin sprite.

        Args:
            x (int): The x-coordinate of the coin's center.
            y (int): The y-coordinate of the coin's center.
            scale (float): Scale factor for the coin's size.
            screen (pygame.Surface): The surface to draw the coin on.
        """
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.vel_y = 0
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        for i in range(6):
            img = pygame.image.load(f'img/Coins/Coin1/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self) -> None:
        """
        Update the coin's animation by cycling through frames.
        """
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list) - 1:
                self.frame_index = 0

    def move(self) -> None:
        """
        Move the coin downward under the influence of gravity.
        """
        dy = 0
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom

        self.rect.y += dy

    def draw(self) -> None:
        """
        Draw the coin on the screen.
        """
        self.screen.blit(self.image, self.rect)
