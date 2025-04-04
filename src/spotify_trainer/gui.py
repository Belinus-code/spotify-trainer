"""Gui module for Spotify trainer"""

# pylint:disable=E0611
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QWidget,
)


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
