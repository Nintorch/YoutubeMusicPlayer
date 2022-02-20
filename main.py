import downloader
import pygame
import pygame_gui
from pygame._sdl2.video import Window
import pynput

# Initialize PyGame
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("YouTube Player")
window_size = (450, 180)
screen = pygame.display.set_mode(window_size, flags=pygame.NOFRAME)
window = Window.from_display_module()  # Get the window so we can change its position

clock = pygame.time.Clock()  # Clock to make the app update 60 times per second

# PyGame GUI elements

manager = pygame_gui.UIManager(pygame.display.get_window_size())  # Manager

search_box = pygame_gui.elements.UITextEntryLine(pygame.rect.Rect((10, 30), (260, 60)), manager)

# Buttons
btn_pause = pygame_gui.elements.UIButton(pygame.Rect((10 + 260 / 2 - 35 - 50, 60), (50, 30)), "Pause", manager)
btn_play = pygame_gui.elements.UIButton(pygame.Rect((10 + 260 / 2 - 25, 60), (50, 30)), "Play", manager)
btn_stop = pygame_gui.elements.UIButton(pygame.Rect((10 + 260 / 2 + 35, 60), (50, 30)), "Stop", manager)

position_slider = pygame_gui.elements.UIHorizontalSlider(pygame.rect.Rect((10, 90), (260, 25)), 0, (0.0, 1.0), manager)

log_text = pygame_gui.elements.UITextBox("(Logging here)", pygame.Rect((10, 130), (260, 50)), manager, True)

# Video thumbnail
thumbnail = pygame.surface.Surface((160, 120))

# Flags and other needed variables
paused = False
music_length = 0.0
music_pos = 0.0
music_loaded = False
mouse_move = False

# some pynput junk so we can get the screen mouse position
mouse = pynput.mouse.Controller()
mouse_pos = (0, 0)


def on_click(x, y, button, pressed):
    quit()
    global mouse_move
    if button == 0 and not pressed:
        mouse_move = False


listener = pynput.mouse.Listener(on_click=on_click)
listener.start()


def events():
    global running, music_pos, music_length, position_slider, music_loaded, mouse_move, mouse_pos, mouse

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.mixer.music.get_busy():
                # Skip 5 seconds forward if arrow right was pressed
                if event.key == pygame.K_RIGHT:

                    music_pos += 5
                    if music_pos > music_length:
                        music_pos = music_length - 1

                    position_slider.set_current_value(music_pos / music_length)
                    pygame.mixer.music.set_pos(music_pos)

                # Go 5 seconds back if arrow left was pressed
                elif event.key == pygame.K_LEFT:

                    music_pos -= 5
                    if music_pos < 0:
                        music_pos = 0

                    position_slider.set_current_value(music_pos / music_length)
                    pygame.mixer.music.set_pos(music_pos)

        # Check if mouse button was clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[1] < 20:
                mouse_pos = pygame.mouse.get_pos()
                mouse_move = True

        # PyGame GUI events
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # GUI button was pressed
                if event.ui_element == btn_play:
                    play()
                elif event.ui_element == btn_stop:
                    stop()
                elif event.ui_element == btn_pause:
                    pause()
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and music_loaded:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()

                if event.value > ((music_length - 1) / music_length):
                    event.value = ((music_length - 1) / music_length)

                pygame.mixer.music.set_pos(event.value * music_length)
                music_pos = event.value * music_length

        manager.process_events(event)

    if mouse_move:
        window.position = (mouse.position[0] - mouse_pos[0],
                           mouse.position[1] - mouse_pos[1])

    if not pygame.mouse.get_pressed(3)[0]:
        mouse_move = False


# Logging function
def log(s):
    events()
    global log_text
    log_text.kill()
    log_text = pygame_gui.elements.UITextBox(s, pygame.Rect((10, 110), (260, 40)), manager, True)
    log_text.full_redraw()

    manager.update(0)
    manager.draw_ui(screen)
    pygame.display.flip()


downloader.log = log


# Play the requested music
def play():
    pygame.mixer.music.stop()
    track = downloader.download(search_box.get_text())

    global music_length
    music_length = pygame.mixer.Sound(track.filename).get_length()

    pygame.mixer.music.load(track.filename)
    pygame.mixer.music.play()
    log("Playing " + track.title)

    global thumbnail
    thumbnail = pygame.image.load(track.thumbnail)

    global music_loaded, music_pos
    music_loaded = True
    music_pos = 0


# Stop the currently playing music
def stop():
    pygame.mixer.music.stop()
    log("Stopped")

    global thumbnail
    thumbnail = pygame.surface.Surface((160, 120))

    global music_loaded
    music_loaded = False


# Pause the currently playing music
def pause():
    global paused
    if not paused:
        pygame.mixer.music.pause()
        log("Paused")
        paused = True
    else:
        pygame.mixer.music.unpause()
        log("Unpaused")
        paused = False


# GUI font
font = pygame.font.SysFont("Arial", 16)
# The header (with the text "YouTube Music Player")
header = pygame.surface.Surface((pygame.display.get_window_size()[0], 20))


# Draw the header
# (This function will have a more useful purpose when I add the themes)
def update_header():
    header.fill(manager.get_theme().get_colour("normal_border"))
    header_text = font.render("YouTube Music Player", True, manager.get_theme().get_colour("normal_text"))
    header.blit(header_text,
                (pygame.display.get_window_size()[0] / 2 - header_text.get_width() / 2, 0))


update_header()

bgcolor = manager.get_theme().get_colour("disabled_bg")

# Main loop

running = True
while running:
    delta_time = clock.tick(60) / 1000.0
    events()

    screen.fill(bgcolor)

    if not position_slider.is_focused and pygame.mixer.music.get_busy():
        music_pos += 1.0 / 60.0
        position_slider.set_current_value(music_pos / music_length)

    manager.update(delta_time)

    screen.blit(header, (0, 0))
    screen.blit(pygame.transform.scale(thumbnail, (160, 120)), (280, 40))

    manager.draw_ui(screen)
    pygame.display.flip()
