# YoutubeMusicPlayer
A music player that plays the music from youtube using the search. I made it because I wanted to, lol

![design](https://user-images.githubusercontent.com/92302738/154856580-83a29835-5480-40c1-97d6-2f11fd66afc9.png)

Features:
- Download the track using the search request, the first result will be downloaded
- Slider as the current posision in the track, pause and stop buttons
- Press right arrow to skip 5 seconds and left arrow to go 5 seconds back
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
- Themes maybe
- Change the downloaded tracks naming system (so the files' names were a video names instead of video ids) 
