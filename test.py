import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Wymiary okna
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rakieta")

# Kolory
color = pygame.Color('red')

# Funkcja rysująca rakietę
def draw_rocket(x, y, height, color):
    # Wysokość rakiety
    rocket_height = height

    # Wymiary części rakiety
    rocket_body_width = 40  # Szerokość głównej części rakiety
    rocket_tip_width = 60   # Szerokość czubka rakiety
    rocket_tip_height = 30  # Wysokość czubka rakiety
    rocket_engine_height = 30  # Wysokość silnika rakiety
    
    # Rysowanie trójkąta (czubek rakiety)
    tip_points = [(x - rocket_tip_width // 2, y), 
                  (x + rocket_tip_width // 2, y), 
                  (x, y - rocket_tip_height)]
    pygame.draw.polygon(screen, color, tip_points)

    # Rysowanie prostokąta (główna część rakiety)
    pygame.draw.rect(screen, color, (x - rocket_body_width // 2, y - rocket_tip_height, rocket_body_width, rocket_height - rocket_tip_height - rocket_engine_height))

    # Rysowanie prostokąta (silnik rakiety)
    pygame.draw.rect(screen, color, (x - rocket_body_width // 2, y - rocket_tip_height + rocket_height - rocket_engine_height, rocket_body_width, rocket_engine_height))

# Główna pętla gry
def main():
    clock = pygame.time.Clock()
    rocket_height = 100  # Wysokość rakiety
    rocket_x = screen_width // 2  # Środek ekranu (poziomo)
    rocket_y = screen_height // 2 + rocket_height // 2  # Pozycja pionowa na ekranie

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Wypełnianie tła
        screen.fill((255, 255, 255))

        # Rysowanie rakiety
        draw_rocket(rocket_x, rocket_y, rocket_height, color)

        # Aktualizacja ekranu
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
