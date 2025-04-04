import sys

# pylint: disable=E0611
from PyQt5.QtWidgets import QApplication


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_trainer.gui import MainWindow


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
    
def cli():
    """Command line interface for the app."""
    app = App()
