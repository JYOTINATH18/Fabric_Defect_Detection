import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from detect_image import detect_defect
from detect_folder import detect_defects_in_folder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Fabric Defect Detection")
        screen_size = QApplication.primaryScreen().availableGeometry().size()
        self.setFixedSize(screen_size.width() * 3 // 4, screen_size.height() * 3 // 4)

        self.title_label = QLabel("Fabric Defect Detection")
        self.title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(40)
        self.title_label.setFont(font)

        # Create the buttons and labels
        self.upload_image_button = QPushButton("Upload Image")
        self.upload_folder_button = QPushButton("Upload Folder")
        self.detect_defect_button = QPushButton("Detect Defect")
        self.image_label = QLabel("Upload Fabric image or folder")
        self.image_label.setFixedSize(600, 500)
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

        self.image_label.setStyleSheet("background-color: #d3f0ed; border: 7px solid #34b7eb; border-radius: 10px;")

        # Set the layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.upload_image_button)
        vbox.addWidget(self.upload_folder_button)
        vbox.addWidget(self.detect_defect_button)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.image_label)
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)

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
