import pygame
import sys
import os

pygame.init()

frame_size_x = 2560
frame_size_y = 1440
corner_size = 6
usable_frame_size_x = frame_size_x - 2 * corner_size
usable_frame_size_y = frame_size_y - 2 * corner_size
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
selected_color = red
unselected_color = white
header_color = pygame.Color(255, 140, 0)
credits_text_color = pygame.Color(0, 255, 0)
fps_controller = pygame.time.Clock()

pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

menu_items = ['Start Game', 'Select Background', 'Credits', 'Exit']
selected_item = 0

font = pygame.font.SysFont('consolas', 60, bold=True)

logo_img = pygame.image.load("strangersnake_logo.png")
logo_width = int(usable_frame_size_x * 0.4)
logo_height = int(logo_width * logo_img.get_height() / logo_img.get_width())
logo_img = pygame.transform.scale(logo_img, (logo_width, logo_height))

background_images = [
    pygame.image.load("bg1.jpeg"),
    pygame.image.load("bg2.jpg")
]

def draw_menu():
    game_window.fill(black)
    logo_rect = logo_img.get_rect(center=(frame_size_x * 0.25, corner_size + usable_frame_size_y // 4))
    game_window.blit(logo_img, logo_rect)
    menu_height = len(menu_items) * 100
    top_margin = (usable_frame_size_y - menu_height) // 2
    for index, item in enumerate(menu_items):
        color = selected_color if index == selected_item else unselected_color
        menu_surface = font.render(item, True, color)
        menu_rect = menu_surface.get_rect(center=(frame_size_x * 0.25, corner_size + top_margin + index * 100))
        game_window.blit(menu_surface, menu_rect)

def show_background_options():
    selected_bg_index = 0
    while True:
        game_window.fill(black)
        logo_rect = logo_img.get_rect(center=(frame_size_x * 0.25, corner_size + usable_frame_size_y // 4))
        game_window.blit(logo_img, logo_rect)
        thumbnail_size = (500, 500)  # Larger thumbnail size
        x_offset = 100
        for i, bg_image in enumerate(background_images):
            thumbnail = pygame.transform.scale(bg_image, thumbnail_size)
            if i == selected_bg_index:
                pygame.draw.rect(game_window, red, (x_offset - 10, 690, thumbnail_size[0] + 20, thumbnail_size[1] + 20), 3)
            game_window.blit(thumbnail, (x_offset, 700))
            x_offset += 600  # Adjust the x-offset for the next thumbnail
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Move left
                    selected_bg_index = (selected_bg_index - 1) % len(background_images)
                elif event.key == pygame.K_l:  # Move right
                    selected_bg_index = (selected_bg_index + 1) % len(background_images)
                elif event.key == pygame.K_y:
                    return selected_bg_index

def select_background():
    selected_bg_index = show_background_options()
    return selected_bg_index

def main_menu():
    global selected_item
    while True:
        game_window.fill(black)
        draw_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('t'):
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN or event.key == ord('v'):
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_y:
                    if menu_items[selected_item] == 'Start Game':
                        game_window.fill(black)
                        pygame.display.update()
                        import nolansnake
                        nolansnake.main()
                    elif menu_items[selected_item] == 'Select Background':
                        selected_bg = select_background()
                        background_image_index = selected_bg
                        background_image = background_images[background_image_index]
                        background_image = pygame.transform.scale(background_image, (frame_size_x, frame_size_y))
                        # Start game with selected background
                        import nolansnake
                        nolansnake.main(background_image)
                    elif menu_items[selected_item] == 'Credits':
                        show_credits()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_y or event.key == pygame.K_n:
                                        return
                    elif menu_items[selected_item] == 'Exit':
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main_menu()