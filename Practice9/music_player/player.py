import pygame
import os

playlist = [
    "music/INNA_Sean_Paul_-_UP_(SkySound.cc).wav",
    "music/UNIK_-_Gonk-Kong_(SkySound.cc).wav"
]

current_track = 0
is_playing = False


def load_track():
    global current_track
    pygame.mixer.music.load(playlist[current_track])


def play_track():
    global is_playing
    load_track()
    pygame.mixer.music.play()
    is_playing = True


def stop_track():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False


def next_track():
    global current_track, is_playing
    current_track = (current_track + 1) % len(playlist)
    load_track()
    pygame.mixer.music.play()
    is_playing = True


def previous_track():
    global current_track, is_playing
    current_track = (current_track - 1) % len(playlist)
    load_track()
    pygame.mixer.music.play()
    is_playing = True


def get_track_name():
    return os.path.basename(playlist[current_track])


def get_track_position():
    pos = pygame.mixer.music.get_pos()
    if pos == -1:
        return "00:00"
    seconds = pos // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"