import pygame

class SlashProjectile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: float, flip: bool, screen: pygame.Surface) -> None:
        """
        My creation
        Initialize a Coin sprite.

        Args:
            x (int): The x-coordinate of the coin's center.
            y (int): The y-coordinate of the coin's center.
            scale (float): Scale factor for the coin's size.
            flip (bool): bool for if img should be flipped or not
            screen (pygame.Surface): The surface to draw the projectile on.
        """
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.flip = flip
        self.direction = 1
        self.vel_x = 0
        self.x = x
        self.y = y + 50

        img = pygame.image.load(f'img/SwordSlashes/WhiteSlashWide/0.png')
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))

        self.image = img
        self.rect = self.image.get_rect()
        if not self.flip:
            self.x += 150
        self.rect.center = (self.x, self.y)

    def move(self) -> None:
        """
        Move the coin downward under the influence of gravity.
        """
        dx = 10

        if self.flip:
            self.direction = -1
        else:
            self.direction = 1

        self.rect.x += dx * self.direction

    def draw(self) -> None:
        """
        Draw the coin on the screen.
        """
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
