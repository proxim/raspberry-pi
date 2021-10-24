import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIN_WIDTH = 1920
WIN_HEIGHT = 260

class Text:
    def __init__(self, text, center_coords, font_size=50, antialias=True, color=BLACK):
        self.font_size = font_size
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.surface = self.font.render(text, antialias, color)
        self.rect = self.surface.get_rect()
        self.rect.center = center_coords
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, left_top_coords=(0,0)):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = left_top_coords
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)            
            
        
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('OEDK Data Visualization') 

    background = Image('graphics/pct_female_users.png')
    #txt = Text('Number of Female OEDK Users 2020', (WIN_WIDTH // 2, 50))
    
    running = True
    while running:
        screen.fill(WHITE)

        background.draw(screen)
        #txt.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()