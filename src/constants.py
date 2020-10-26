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
}