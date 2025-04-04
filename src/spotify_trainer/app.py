import sys

# pylint: disable=E0611
from PyQt5.QtWidgets import QApplication
# pylint:disable=E0611
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class App:
    def __init__(self):

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id="9b5d8c07f8724ad9b6ad92a7bff7acc1",
                client_secret="8b9484a55f0046e4b0e4768bd52b96a5",
                redirect_uri="http://localhost:8080/callback",
                scope="user-modify-playback-state user-read-playback-state",
            )
        )

        app = QApplication(sys.argv)
        self.window = MainWindow(
            "https://open.spotify.com/playlist/15hZ0ez6sHYhTeCCshxJTN?si=88b86ab0d1c94571"
        )
        self.window.set_playlist_apply_callback(self.set_playlist_apply)
        self.window.set_playback_pause_callback(self.pause)
        self.window.set_playback_next_callback(self.skip)
        self.window.set_playback_start_callback(self.pause)
        self.window.set_guess_callback(self.guess)
        self.window.show()
        app.exec()

    def set_playlist_apply(self, playlist_str):
        playlist_id = playlist_str.split("/")[-1].split("?")[
            0
        ]  # Playlist-ID extrahieren
        self.sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
        self.pause()

    def pause(self):
        if self.is_playing():
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

    def skip(self):
        self.sp.next_track()
        self.window.set_results(["", "", ""])

    def is_playing(self):
        playback_info = self.sp.current_playback()
        if playback_info and playback_info["is_playing"]:
            return True
        return False
    
    def guess(self):
        self.window.set_results(self.get_current_track())

    def get_current_track(self):
        track_info = self.sp.current_playback()

        if track_info and track_info["item"]:
            track = track_info["item"]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            release_year = track["album"]["release_date"][:4]  # Nur das Jahr extrahieren

            return release_year, artist_name, track_name
        return None

start_app = App()

class MainWindow(QMainWindow):
    def __init__(self, playlist_str):
        super().__init__()

        self.setWindowTitle("Spotify Trainer")

        self.apply_playlist_callback = None
        self.start_playback_callback = None
        self.pause_playback_callback = None
        self.next_track_callback = None
        self.guess_callback = None

        # Haupt-Widget und Layout
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        playlist_layout = QHBoxLayout()
        playback_layout = QHBoxLayout()
        guessing_layout = QHBoxLayout()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(central_layout)

        self.playlist_line_edit = QLineEdit()
        self.playlist_line_edit.setText(playlist_str)
        playlist_layout.addWidget(self.playlist_line_edit)

        self.playlist_apply_button = QPushButton()
        self.playlist_apply_button = QPushButton("Apply")
        self.playlist_apply_button.clicked.connect(self.apply_playlist)
        playlist_layout.addWidget(self.playlist_apply_button)
        central_layout.addLayout(playlist_layout)

        self.playback_start_button = QPushButton("Start")
        self.playback_start_button.clicked.connect(self.start_playback)
        playback_layout.addWidget(self.playback_start_button)

        self.playback_pause_button = QPushButton("Pause")
        self.playback_pause_button.clicked.connect(self.pause_playback)
        playback_layout.addWidget(self.playback_pause_button)

        self.playback_next_button = QPushButton("Next")
        self.playback_next_button.clicked.connect(self.next_track)
        playback_layout.addWidget(self.playback_next_button)
        central_layout.addLayout(playback_layout)

        self.year_guess_line_edit = QLineEdit()
        self.year_guess_line_edit.setPlaceholderText("Year")
        guessing_layout.addWidget(self.year_guess_line_edit)

        self.interpret_guess_line_edit = QLineEdit()
        self.interpret_guess_line_edit.setPlaceholderText("Interpret")
        guessing_layout.addWidget(self.interpret_guess_line_edit)

        self.title_guess_line_edit = QLineEdit()
        self.title_guess_line_edit.setPlaceholderText("Title")
        guessing_layout.addWidget(self.title_guess_line_edit)

        self.guess_button = QPushButton("Guess")
        self.guess_button.clicked.connect(self.guess)
        guessing_layout.addWidget(self.guess_button)

        central_layout.addLayout(guessing_layout)

    def set_playlist_apply_callback(self, callback):
        self.apply_playlist_callback = callback

    def set_playback_start_callback(self, callback):
        self.start_playback_callback = callback

    def set_playback_pause_callback(self, callback):
        self.pause_playback_callback = callback

    def set_playback_next_callback(self, callback):
        self.next_track_callback = callback

    def set_guess_callback(self, callback):
        self.guess_callback = callback

    def guess(self):
        if hasattr(self, "guess_callback"):
            self.guess_callback()

    def apply_playlist(self):
        if hasattr(self, "apply_playlist_callback"):
            self.apply_playlist_callback(self.playlist_line_edit.text())

    def start_playback(self):
        if hasattr(self, "start_playback_callback"):
            self.start_playback_callback()

    def pause_playback(self):
        if hasattr(self, "pause_playback_callback"):
            self.pause_playback_callback()

    def next_track(self):
        if hasattr(self, "next_track_callback"):
            self.next_track_callback()

    def set_results(self, results):
        self.year_guess_line_edit.setText(str(results[0]))
        self.interpret_guess_line_edit.setText(results[1])
        self.title_guess_line_edit.setText(results[2])
