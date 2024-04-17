from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout,\
                                QVBoxLayout, QLabel, QTextEdit, QApplication, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from tracklist_combiner import load_tracklist, merge_consecutive_rows, get_track_counts, \
                                get_exceeding_artists, get_exceeding_albums, get_consecutive_artist_tracks,\
                                    get_consecutive_album_tracks, format_tracklist, format_reason_for_restriction, \
                                        format_macro_info, check_all_for_repeated_tracks

class RockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show tracklist checker")
        self.resize(1000, 800)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #171C2B;
            }
            QPushButton {
                font-family: "DM Sans", sans-serif;
                background-color: #5000ff;
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin: 1px 2px;
                border-radius: 10px;
                width: 140px;
            }
            QPushButton:hover {
                background-color: #7D52BA;
            }
            QTextEdit {
                font: Courier;
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 4px;
                color: black;
            }
            QLineEdit {
                font-family: "DM Sans", sans-serif;
                color:white;
                background-color: #1E232F;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 4px;
            }
            QLabel {
                font-family: "DM Sans", sans-serif;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 8px;
                color: white;
            }
        """)
        
        self.setupUI()
    
    def setupUI(self):
        # Line Edit and Label
        label = QLabel("Enter tracklist: ")
        
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter tracklist here")
        
        enter_button = QPushButton("↵")
        enter_button.setFixedWidth(100)
        enter_button.setFixedHeight(35)
        enter_button.setStyleSheet("font-weight: bold;")
        enter_button.setStyleSheet("font-size: 22px;")
        enter_button.clicked.connect(self.paste_and_enter)
        
        # Buttons
        button1 = self.createButton("Clean up tracklist", self.button1_clicked)
        button2 = self.createButton("Reason for restriction", self.button2_clicked)
        button3 = self.createButton("Macro info", self.button3_clicked)
        buttonn = self.createButton("Reset", self.buttonn_clicked)
        
        # Text Holder Label
        self.text_holder_label = QTextEdit()
        self.text_holder_label.setReadOnly(True)
        self.text_holder_label.setPlainText(format)
        self.text_holder_label.setFont(QFont("Courier"))
        self.text_holder_label.setStyleSheet("font-size: 14px;")
        
        # Copy Button
        copy_text_holder_label = self.createButton("Copy", self.copy_text)
        copy_text_holder_label.setFixedWidth(170)
        copy_text_holder_label.setFixedHeight(50)
        copy_text_holder_label.setStyleSheet("font-size: 18px;")

        # Layout
        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(enter_button)
        h_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(button1, alignment=Qt.AlignHCenter)
        v_layout.addWidget(button2, alignment=Qt.AlignHCenter)
        v_layout.addWidget(button3, alignment=Qt.AlignHCenter)
        v_layout.addWidget(buttonn, alignment=Qt.AlignHCenter)
        v_layout.addWidget(self.text_holder_label)
        v_layout.addWidget(copy_text_holder_label, alignment=Qt.AlignHCenter)
        
        self.setLayout(v_layout)
    
    def createButton(self, text, clicked_method):
        button = QPushButton(text)
        button.clicked.connect(clicked_method)
        return button

    def enter_text(self):
        self.text_holder_label.setText(self.line_edit.text())

    def paste_and_enter(self):
        self.line_edit.clear()
        clipboard = QApplication.clipboard()
        text = clipboard.text()  # Get text from clipboard
        self.line_edit.setText(text)  # Set text to line edit
        self.enter_text()  # Call enter_text method to update text_holder_label

    def editing_finished(self):
        self.text_holder_label.setPlainText(self.line_edit.text())

    def button1_clicked(self):
        try:
            tracklist_data = self.line_edit.text()
            rows = load_tracklist(tracklist_data)
            merged_rows = merge_consecutive_rows(rows)
            formatted_tracklist = format_tracklist(merged_rows)
            self.text_holder_label.setPlainText(formatted_tracklist)
            self.sender().clearFocus()
        except Exception as e:
            self.display_error_message(str(e))

    def button2_clicked(self):
        try:
            tracklist_data = self.line_edit.text()
            rows = load_tracklist(tracklist_data)
            merged_rows = merge_consecutive_rows(rows)
            artist_tracks, album_tracks = get_track_counts(merged_rows)
            exceeding_artists = get_exceeding_artists(artist_tracks)
            exceeding_albums = get_exceeding_albums(album_tracks)
            consecutive_artist_tracks = get_consecutive_artist_tracks(merged_rows)
            consecutive_album_tracks = get_consecutive_album_tracks(merged_rows)

            result_text = format_reason_for_restriction(exceeding_artists, exceeding_albums, consecutive_artist_tracks, consecutive_album_tracks)

            if result_text:
                self.text_holder_label.setPlainText(result_text)
            else:
                self.text_holder_label.setPlainText("No restrictions found.")

            # Check for repeated tracks

            repeated_tracks = check_all_for_repeated_tracks(exceeding_artists, exceeding_albums, consecutive_artist_tracks, consecutive_album_tracks)

            if repeated_tracks:
                error_message = "The following track(s) are causing more than one restriction:\n"
                for key, tracks in repeated_tracks.items():
                    unique_tracks = set(tracks)
                    error_message += f"\n({'Album' if key in consecutive_album_tracks else 'Artist'}) {key}:\n"
                    for track in unique_tracks:
                        error_message += f"\t  - {track}\n"
                error_message += f"\nPlease review manually."
                self.display_error_message(error_message)

            self.sender().clearFocus()
        except Exception as e:
            self.display_error_message(str(e))

    def button3_clicked(self):
        try:
            tracklist_data = self.line_edit.text()
            rows = load_tracklist(tracklist_data)
            merged_rows = merge_consecutive_rows(rows)
            artist_tracks, album_tracks = get_track_counts(merged_rows)
            exceeding_artists = get_exceeding_artists(artist_tracks)
            exceeding_albums = get_exceeding_albums(album_tracks)
            consecutive_artist_tracks = get_consecutive_artist_tracks(merged_rows)
            consecutive_album_tracks = get_consecutive_album_tracks(merged_rows)

            result_text = format_macro_info(exceeding_artists, consecutive_artist_tracks, exceeding_albums, consecutive_album_tracks)

            if result_text:
                self.text_holder_label.setPlainText(result_text)
            else:
                self.text_holder_label.setPlainText("The show is not being restricted.")
                
            # Check for repeated tracks

            repeated_tracks = check_all_for_repeated_tracks(exceeding_artists, exceeding_albums, consecutive_artist_tracks, consecutive_album_tracks)

            if repeated_tracks:
                error_message = "The following track(s) are causing more than one restriction:\n"
                for key, tracks in repeated_tracks.items():
                    unique_tracks = set(tracks)
                    error_message += f"\n({'Album' if key in consecutive_album_tracks else 'Artist'}) {key}:\n"
                    for track in unique_tracks:
                        error_message += f"\t  - {track}\n"
                error_message += f"\nPlease review manually."
                self.display_error_message(error_message)

            self.sender().clearFocus()
        except Exception as e:
            self.display_error_message(str(e))

    def buttonn_clicked(self):
        self.line_edit.clear()
        self.text_holder_label.setPlainText(format)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_holder_label.toPlainText())
        self.sender().clearFocus()

    def display_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.exec_()

format = """Use the following format that includes the header:
        

Start	End	Artists	Track Title	Id	Albums
0	30	Mack Fields	Bowling Ball Blues	3530145	Cults Hits Novelty Classics, Vol. 1
30	60	Mack Fields	Bowling Ball Blues	3530145	Cults Hits Novelty Classics, Vol. 1
60	90	Mack Fields	Bowling Ball Blues	3530145	Cults Hits Novelty Classics, Vol. 1
90	120	Mack Fields	Bowling Ball Blues	3530145	Cults Hits Novelty Classics, Vol. 1
120	150	Hank Locklin	I m Tired Of Bummin Around	4838751	Queen Of Hearts
150	180	Hank Locklin	I m Tired Of Bummin Around	4838751	Queen Of Hearts
180	210	Hank Locklin	I m Tired Of Bummin Around	4838751	Queen Of Hearts
210	240	Hank Locklin	I m Tired Of Bummin Around	4838751	Queen Of Hearts
240	270	Hank Locklin	I m Tired Of Bummin Around	4838751	Queen Of Hearts
390	420	Hank Thompson	Hangover Tavern	2964975	A Six Pack To Go
420	450	Hank Thompson	Hangover Tavern	2964975	A Six Pack To Go
450	480	Hank Thompson	Hangover Tavern	2964975	A Six Pack To Go
480	510	Hank Thompson	Hangover Tavern	2964975	A Six Pack To Go
510	540	Hank Thompson	Hangover Tavern	2964975	A Six Pack To Go
540	570	Hank Thompson	Hangover Tavern	2964975	A Six Pack To Go"""