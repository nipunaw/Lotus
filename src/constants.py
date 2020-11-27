import os

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/config.ini')
SCHEDULE_FILE_PATH  = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/schedule.json')
SCHEDULED_NOTES_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/')
DIRECTORY_FILE = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/directories.txt')

########### Assets ###########
assets = {
    "logo": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/lotus.png'),
    "newNote": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/newNote.png'),
    "newNoteDarker": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/newNoteDarker.png'),
    "previousNotes": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/previousNotes.png'),
    "previousNotesDarker": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/previousNotesDarker.png'),
    "schedule": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/schedule.png'),
    "scheduleDarker": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/scheduleDarker.png'),
    "time_date" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/time_date.png'),
    "lato" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/Lato-Regular.ttf'),
    "logo_black" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/logo_black.png'),
    "settings" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/settings.png'),
    "pen" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/pen.png'),
    "eraser" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/eraser.png'),
    "highlighter" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/highlighter.png'),
    "undo" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/undo.png'),
    "redo" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/redo.png'),
    "clear" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/clear.png'),
    "home" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/home.png'),
    "color_wheel" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/color_wheel.png'),
    "color_indicator" : os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/color_indicator.png'),
    "pen_eraser_cursor": os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/PenEraserCursor.png')
}