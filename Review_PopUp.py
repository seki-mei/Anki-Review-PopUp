#// auth_ Mamad
#// Copyright (c) 2020 - 2023 Mamad


from anki.hooks import wrap
from anki.sound import play, clearAudioQueue, AVPlayer
from aqt.reviewer import Reviewer
from aqt.utils import showInfo
from aqt import mw, gui_hooks
from aqt.qt import *
import os
from os.path import join, dirname
import random
addon_path = dirname(__file__)
config = mw.addonManager.getConfig(__name__)


def _play_tags(self, tags):
    self._enqueued = tags[:]
    self._play_next_if_idle()


def myPopUp(self, ease):
    cnt = self.mw.col.sched.answerButtons(self.card)
    popUp_Chance = config["Pop-Up Chance"]
    show_random = random.randint(0, 100)
    if show_random < popUp_Chance:
        play_audio = config["Play Audio"]
        play_videoGif = config["Play Video/GIF"]
        if self.state == "answer":
            if cnt == 3:
                if ease == 1:
                    folder = 'again'
                elif ease == 2:
                    folder = 'good'
                else:
                    folder = 'easy'
            else:
                if ease == 1:
                    folder = 'again'
                elif ease == 2:
                    folder = 'hard'
                elif ease == 3:
                    folder = 'good'
                else:
                    folder = 'easy'
            if play_audio:
                audio_folder = join(addon_path, 'user_files/audio', folder)
                audioName_list = os.listdir(audio_folder)
                audio_name = '/{}'.format(random.choice(audioName_list))
                audio_path = audio_folder + audio_name
                AVPlayer.play_tags=_play_tags
                clearAudioQueue()
                play(audio_path)
            if play_videoGif:
                video_folder = join(addon_path, 'user_files/video_gif', folder)
                videoName_list = os.listdir(video_folder)
                video_name = '/{}'.format(random.choice(videoName_list))
                video_path = video_folder + video_name
                AVPlayer.play_tags=_play_tags
                clearAudioQueue()
                play(video_path)
            show_popUp(cnt, ease)

def show_popUp(cnt, ease):
    headerText_fontSize = config["Header Text Font Size"]
    headerText_fontStyle = config["Header Text Font Style"]
    show_header = config["Show Header"]
    show_image = config["Show Image"]
    header_list_again = config["Header Texts_ Again"]
    header_list_hard = config["Header Texts_ Hard"]
    header_list_good = config["Header Texts_ Good"]
    header_list_easy = config["Header Texts_ Easy"]
    if cnt == 3:
        if ease == 1:
            folder = 'again'
            header_text = random.choice(header_list_again)
        elif ease == 2:
            folder = 'good'
            header_text = random.choice(header_list_good)
        elif ease == 3:
            folder = 'easy'
            header_text = random.choice(header_list_easy)
        else:
            folder = 'again'
            header_text = "cnt: {} | ease: {}".format(cnt, ease)
    else:
        if ease == 1:
            folder = 'again'
            header_text = random.choice(header_list_again)
        elif ease == 2:
            folder = 'hard'
            header_text = random.choice(header_list_hard)
        elif ease == 3:
            folder = 'good'
            header_text = random.choice(header_list_good)
        elif ease == 4:
            folder = 'easy'
            header_text = random.choice(header_list_easy)
        else:
            folder = 'again'
            header_text = "cnt: {} | ease: {}".format(cnt, ease)
    image_folder = join(addon_path, 'user_files/images', folder)
    imageName_list = os.listdir(image_folder)
    image_name = '/{}'.format(random.choice(imageName_list))

    window = QDialog(mw)

    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    window.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.Popup |
        Qt.WindowType.NoDropShadowWindowHint |
        Qt.WindowType.WindowStaysOnTopHint
    )
    window.setStyleSheet("background: transparent;")

    window.setWindowIcon(QIcon(join(addon_path, 'user_files/images') + "/icon.png"))
    
    # Get the screen where the main window is displayed
    screen = mw.window().screen()
    # Get the available screen geometry (accounts for taskbars/docks)
    screen_rect = screen.availableGeometry()
    screen_width = screen_rect.width()
    screen_height = screen_rect.height()
    
    # Set window to be frameless
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup | Qt.WindowType.NoDropShadowWindowHint)
    
    # Set the size to match the screen dimensions
    window.setFixedSize(screen_width, screen_height)
    
    # Position it at the top-left of the available screen area
    window.move(screen_rect.x(), screen_rect.y())
    
    header = QLabel()
    header.setAlignment(Qt.AlignmentFlag.AlignCenter)
    header.setText("<div style='font-size: {}px; font-family: {};'> {} </div>".format(headerText_fontSize, headerText_fontStyle, header_text))
    image = QLabel()
    pixmap = QPixmap(image_folder + image_name)
    
    # Use screen dimensions for scaling instead of fixed 1024px limits
    picture = pixmap.scaled(screen_width, screen_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    image.setAlignment(Qt.AlignmentFlag.AlignCenter)
    image.setPixmap(picture)
    
    layout = QVBoxLayout()
    if show_header:
        layout.addWidget(header)
    if show_image:
        layout.addWidget(image)
    show_onAgain = config["Show on Again"]
    show_onHard = config["Show on Hard"]
    show_onGood = config["Show on Good"]
    show_onEasy = config["Show on Easy"]
    window.setLayout(layout)
    
    # Add key press event to close on any key
    window.keyPressEvent = lambda event: window.hide() if event.key() != Qt.Key.Key_unknown else None
    
    if not show_image and not show_header:
        return
    elif ease == 1 and show_onAgain:
        window.exec()
    elif ease == 2 and show_onHard:
        window.exec()
    elif ease == 3 and show_onGood:
        window.exec()
    elif ease == 4 and show_onEasy:
        window.exec()
    else:
        return


Reviewer._answerCard = wrap(Reviewer._answerCard, myPopUp, 'before')
