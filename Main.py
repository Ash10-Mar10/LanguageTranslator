import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QPalette
from PyQt5.QtCore import Qt
from googletrans import Translator

# Keeps track of open windows
open_windows = set()


# Displays the instructions window and adds to open_windows
def show_instructions():
    instructions_window.show()
    open_windows.add(instructions_window)


# Displays the application window and adds to open_windows
def start_application():
    window.show()
    open_windows.add(window)


# Closes all the windows that are opened before quiting the application
def exit_application(event=None):
    global open_windows
    for win in open_windows:
        win.close()
    QApplication.instance().quit()


# Translation function that uses GoogleTrans library
def translate_to_chosen_language():
    try:
        english_only_text = input_field.text().strip()
        target_language = dropdown.currentText().lower()
        translator = Translator()
        translation = translator.translate(english_only_text, dest=target_language)
        result_text = f"{translation.text}"

        # Creates a dialog window which displays the translated text
        dialog = QDialog()
        dialog.setWindowTitle("Translated Text")

        # Creates a layout for the dialog window so the user is able to highlight the text
        layout = QVBoxLayout()
        translation_label = QLabel(result_text)
        translation_label.setFont(QFont('Times New Roman', 14))
        translation_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(translation_label)

        # Creates a copy button for the user to be able to copy to the clipboard
        copy_button = QPushButton("Copy to Clipboard")
        layout.addWidget(copy_button)

        # Connect the copy button to copy the result_text to clipboard
        def copy_to_clipboard():
            clipboard = QApplication.clipboard()
            clipboard.setText(result_text)

        copy_button.clicked.connect(copy_to_clipboard)

        # Creates a close button so that the user has the option to click to close the window
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        # Sets the layout and executes it
        dialog.setLayout(layout)
        dialog.exec_()
    except Exception as e:
        # Creates a dialog error window to show if there is an error while trying to translate the text
        error_dialog = QDialog()
        error_dialog.setWindowTitle("Error")
        error_dialog.setFixedSize(400, 200)

        # Creates a layout for the dialog error
        layout = QVBoxLayout()
        error_label = QLabel(f"Error during translation: {e}")
        layout.addWidget(error_label)

        # Creates a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(error_dialog.close)
        layout.addWidget(close_button)

        # Sets the layout and executes it
        error_dialog.setLayout(layout)
        error_dialog.exec_()


# Creates a variable for the application
app = QApplication(sys.argv)

# Creates a cover window for the application
cover_window = QWidget()
cover_window.resize(1900, 950)
cover_window.setWindowTitle("Translator app")

# Transports the path of the image to the variable
background_image_path = r'C:\Users\ashto\PythonProjects\LanguageTranslator\Pictures\Cover_Window.jpg'

# Creates a label to display the background image
background_label = QLabel(cover_window)
background_pixmap = QPixmap(background_image_path)
background_label.setPixmap(background_pixmap)
background_label.setGeometry(0, 0, cover_window.width(), cover_window.height())

# Changes the font style and size in the cover window
cover_window.setStyleSheet("""font-family: Times New Roman; font-size: 22px;""")

# Creates an instructions button for the cover window
instruction_button = QPushButton("Instructions")
instruction_button.setFixedWidth(500)  # Set your desired width
instruction_button.setFixedHeight(40)  # Set desired height
instruction_button.clicked.connect(show_instructions)

# Creates a start button for the cover window
start_button = QPushButton("Start")
start_button.setFixedWidth(500)  # Set your desired width
start_button.setFixedHeight(40)  # Set desired height
start_button.clicked.connect(show_instructions)

# Cover window layout and displays the cover window first
cover_layout = QHBoxLayout(cover_window)
cover_layout.addWidget(instruction_button)
cover_layout.addWidget(start_button)
cover_window.show()
open_windows.add(cover_window)

# Creates an instructions window
instructions_window = QWidget()
instructions_window.resize(800, 600)  # Edits the size of the window
instructions_window.setMinimumSize(800, 600)  # Minimum size possible
instructions_window.setMaximumSize(800, 600)  # Maximum size possible
instructions_window.setWindowTitle("Instructions")

# Transports the path of the image to the variable
instructions_image_path = r'C:\Users\ashto\PythonProjects\LanguageTranslator\Pictures\Instructions_Window.jpg'

# Creates a label to display the image to the instructions window
instructions_label = QLabel(instructions_window)
instructions_pixmap = QPixmap(instructions_image_path)
instructions_label.setPixmap(instructions_pixmap)
instructions_label.setGeometry(0, 0, instructions_window.width(), instructions_window.height())

# Creates a text variable to hold the text for the instructions window
instructions_text = QTextEdit()
instructions_text.setPlainText(
    "Instructions on how to use the application:\n\n"
    "1. Enter the text you want to be translated.\n"
    "2. Ensure you correctly spell the word or phrase.\n"
    "3. Ensure you use correct punctuation.\n"
    "4. Select the dropbox on the right and choose one of the options.\n"
    "5. After you selected a language, click the submit button.\n"
    "6. The translated text will appear in a messagebox and you will have the option to copy it.\n"
    "7. There may be some languages that are not supported by the translator.\n\n"
    "                     PLEASE READ THE INSTRUCTIONS CAREFULLY!                     "
)
instructions_text.setStyleSheet(""" font-size: 22px;""")
instructions_text.setReadOnly(True)  # Prevents the user from editing the text

# Sets text color to white
palette = instructions_text.palette()
palette.setColor(QPalette.Text, Qt.white)
instructions_text.setPalette(palette)

# Creates a scroll area for the text just in case it takes up a lot of space
scroll_area = QScrollArea()
scroll_area.setWidget(instructions_text)
scroll_area.setWidgetResizable(True)

# Sets the background color of the scroll area to transparent
scroll_area.setStyleSheet("background: transparent;")

# Creates a checkbox to confirm reading instructions and updates the font size and color
read_checkbox = QCheckBox("I have read and understood the instructions")
read_checkbox.setStyleSheet("QCheckBox { font-size: 22px; color: white; }")

# Creates a begin button that is only enabled when the user clicks on the checkbox
begin_button = QPushButton("Begin")
begin_button.setEnabled(False)  # Disables the button


# Function that will enable the begin button if the checkbox is clicked
def enable_begin_button(state):
    begin_button.setEnabled(state)


# Initiates the enable_begin_button function
read_checkbox.stateChanged.connect(enable_begin_button)

# Starts the application function if the begin button is clicked
begin_button.clicked.connect(start_application)

# Layout of the instructions window
instructions_layout = QVBoxLayout(instructions_window)
instructions_layout.addWidget(scroll_area)
instructions_layout.addWidget(read_checkbox)
instructions_layout.addWidget(begin_button, alignment=Qt.AlignHCenter)  # Centers the begin button on the bottom

# Creates the main window for the application
window = QWidget()
window.resize(1900, 950)  # Sets the size for the window
window.setWindowTitle("Translator App")

# Transports the path of the image to the variable
window_image_path = r'C:\Users\ashto\PythonProjects\LanguageTranslator\Pictures\Application_Window.jpg'

# Create a label to display the background image
window_label = QLabel(window)
window_pixmap = QPixmap(window_image_path)
window_label.setPixmap(window_pixmap)
window_label.setGeometry(0, 0, window.width(), window.height())

# Creates a text input in the window
input_field = QLineEdit()
input_field.setStyleSheet("""background-color: white;color: black;font-family: Times New Roman;font-size: 22px;""")
input_field.setPlaceholderText("Enter text here")
input_field.setFixedWidth(500)  # Set your desired width
input_field.setFixedHeight(40)  # Set desired height

# Creates a dropdown menu for the window
dropdown_Title = QLabel("Select a Language:")
# A list of all supported languages from googletrans library
options = ["Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani",
           "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Catalan",
           "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)",
           "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto",
           "Estonian", "Filipino", "Finnish", "French", "Frisian", "Galician",
           "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa",
           "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo",
           "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Kannada",
           "Kazakh", "Khmer", "Korean", "Kurdish (Kurmanji)", "Kyrgyz", "Lao",
           "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian",
           "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi",
           "Mongolian", "Myanmar (Burmese)", "Nepali", "Norwegian", "Odia",
           "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian",
           "Russian", "Samoan", "Scots Gaelic", "Serbian", "Sesotho", "Shona",
           "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish",
           "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Telugu", "Thai",
           "Turkish", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh",
           "Xhosa", "Yiddish", "Yoruba", "Zulu"]
dropdown = QComboBox()
dropdown.setStyleSheet("""background-color: white;color: black;font-family: Times New Roman;font-size: 22px;""")
dropdown.addItem(dropdown_Title.text())
dropdown.addItems(options)
dropdown.setFixedWidth(500)  # Sets the width of the widget
dropdown.setFixedHeight(40)  # Sets the height of the widget

# Creates a submit button for the window
submit_button = QPushButton("Submit")
submit_button.setStyleSheet("""background-color: white;color: black;font-family: Times New Roman;font-size: 22px;""")
submit_button.setFixedWidth(200)  # Sets the width of the widget
submit_button.setFixedHeight(100)  # Sets the height of the widget

# Horizontal layout for the window
horizontal_layout = QHBoxLayout()
horizontal_layout.addWidget(input_field)
horizontal_layout.addWidget(dropdown)

# Vertical layout for the window
vertical_layout = QVBoxLayout()
vertical_layout.addLayout(horizontal_layout)  # Adds the horizontal layout to the vertical so that they stay horizontal
vertical_layout.addWidget(submit_button, alignment=Qt.AlignHCenter)  # Centers the submit button vertically below

# Starts the translating function
submit_button.clicked.connect(lambda: translate_to_chosen_language())

# Sets the window layout
window.setLayout(vertical_layout)

# Connects the close events of the windows (except instructions window) to the exit_application function
cover_window.closeEvent = exit_application
window.closeEvent = exit_application

# Runs the application's main loop
if __name__ == "__main__":
    app.exec_()
