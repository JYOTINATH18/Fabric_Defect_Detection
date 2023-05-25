import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from PyQt5.QtCore import Qt
from detect_image import detect_defect
from detect_folder import detect_defects_in_folder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Fabric Defect Detection")
        # logo = QIcon("D:\\FabricDataset\\Capture.PNG")
        # self.setWindowIcon(logo)
        screen_size = QApplication.primaryScreen().availableGeometry().size()
        self.setFixedSize(screen_size.width() * 4 // 4, screen_size.height() * 4 // 4)
        self.showMaximized()

        self.title_label = QLabel("<i>FABRIC DEFECT DETECTION AND CLASSIFICATION</i>")
        self.title_label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 36, QFont.Bold)  # Use Arial font with size 48 and bold style
        self.title_label.setFont(font)

        # Set the color for the title label
        color = QColor("#1D267D")  # Use a custom color, you can change it to any desired color
        self.title_label.setStyleSheet(f"color: {color.name()};")

        # Create the buttons
        self.upload_image_button = QPushButton("Upload Image")
        self.upload_folder_button = QPushButton("Upload Folder")
        self.detect_defect_button = QPushButton("Detect Defect")
        self.exit_button = QPushButton("Exit")

        # Create the image label and set its properties
        self.image_label = QLabel("Upload Fabric image or folder")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("font-size: 30px; color: #34b7eb ;")

        # Set the fonts and styles for the buttons and labels
        font = QFont()
        font.setPointSize(20)
        self.upload_image_button.setFont(font)
        self.upload_folder_button.setFont(font)
        self.detect_defect_button.setFont(font)

        button_style = """
            QPushButton {
                background-color: #343deb;
                color: #ffffff;
                border: 2px solid #3366cc;
                border-radius: 10px;
                padding: 20px;
                min-width: 150px;
            }

            QPushButton:hover {
                background-color: #b5b7eb;
                color: #080808;
                border: 2px solid #3366cc;
            }

            QPushButton:pressed {
                background-color: #204080;
                color: #ffffff;
                border: 2px solid #204080;
            }
        """
        self.upload_image_button.setStyleSheet(button_style)
        self.upload_folder_button.setStyleSheet(button_style)
        self.exit_button = QPushButton("Exit")
        self.exit_button.setFont(font)
        self.exit_button.clicked.connect(QApplication.quit)

        detect_button_style = """
            QPushButton {
                background-color: #cc2f1b;
                color: #ffffff;
                border: 2px solid #cc0000;
                border-radius: 10px;
                padding: 20px;
            }

            QPushButton:hover {
                background-color: #f08475;
                color: #080808;
                border: 2px solid #cc0000;
            }

            QPushButton:pressed {
                background-color: #800000;
                color: #ffffff;
                border: 2px solid #800000;
            }
        """
        self.detect_defect_button.setStyleSheet(detect_button_style)
        self.exit_button.setStyleSheet(detect_button_style)
        self.image_label = QLabel("Upload Fabric image or folder")
        self.image_label.setFixedSize(900, 800)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("font-size: 30px; color: #34b7eb ;")

        self.image_label.setStyleSheet("background-color: #d3f0ed; border: 7px solid #34b7eb; border-radius: 10px;")

        # Set the layout
        vbox_buttons = QVBoxLayout()
        vbox_buttons.addWidget(self.upload_image_button)
        vbox_buttons.addWidget(self.upload_folder_button)
        vbox_buttons.addWidget(self.detect_defect_button)
        vbox_buttons.addWidget(self.exit_button)
        vbox_buttons.setSpacing(20)

        hbox_main = QHBoxLayout()
        hbox_main.addWidget(self.image_label)
        hbox_main.addSpacing(100)  # Adjust spacing between image label and buttons
        hbox_main.addLayout(vbox_buttons)

        vbox_main = QVBoxLayout()
        vbox_main.addWidget(self.title_label)
        vbox_main.addStretch(1)
        vbox_main.addLayout(hbox_main)
        vbox_main.addStretch(1)  # Stretch to fill available space

        self.setLayout(vbox_main)

        self.upload_image_button.setFixedWidth(350)
        self.upload_folder_button.setFixedWidth(350)
        self.detect_defect_button.setFixedWidth(350)
        self.exit_button.setFixedWidth(350)

        # Connect the buttons to their respective functions
        self.upload_image_button.clicked.connect(self.upload_image)
        self.upload_folder_button.clicked.connect(self.upload_folder)
        self.detect_defect_button.clicked.connect(self.detect_defect)

        # Initialize the path to the selected image
        self.image_path = ""

    def upload_image(self):
        # Open a file dialog and get the path to the selected image
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.jfif *jpeg)")
        if file_path:
            # Display the selected image in the label
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)
            self.image_path = file_path

            # Resize the pixmap to fit the label
            pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)

            # Set the pixmap for the label
            self.image_label.setPixmap(pixmap)

    def upload_folder(self):
        # Open a file dialog and get the path to the selected folder
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            # TODO: Implement defect detection on all images in folder
            detect_defects_in_folder(folder_path)
        else:
            pass

    def detect_defect(self):
        # Call the detect_defect function from detect.py
        if self.image_path:
            detect_defect(self.image_path)
        else:
            print("No image selected")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet("background-color: #f0f0f0;")
    window.show()
    sys.exit(app.exec_())
