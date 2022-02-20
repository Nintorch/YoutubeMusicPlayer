# YoutubeMusicPlayer
A music player that plays the music from youtube using the search. I made it because I wanted to, lol

Features:
- Download the track using the search request, the first result will be downloaded
- Slider as the current posision in the track, pause and stop buttons
- Video thumbnail is downloaded and shown in the player

Requirements:
- Python 3
- PyGame 2
- Pygame_gui
- Pytube (with https://github.com/pytube/pytube/pull/1244 applied)
- Pynput (so we can get the screen mouse position, Pygame only allows to get the local mouse position)
- PyFFmpeg and FFmpeg (to convert the downloaded mp4 to ogg)

Todo:
- A playlist of downloaded tracks
- Volume control
