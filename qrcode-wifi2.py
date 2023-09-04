#!/usr/bin/python3

import os
import sys
from PyQt5.QtCore import Qt, QDir
import qrcode
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QComboBox, QLabel, QCheckBox, QFileDialog
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI elements
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 280, 280)

        self.ssid_label = QLabel("SSID:", self)
        self.ssid_label.setGeometry(300, 10, 40, 30)
        self.ssid_input = QLineEdit(self)
        self.ssid_input.setGeometry(340, 10, 240, 30)

        self.password_label = QLabel("Pass:", self)
        self.password_label.setGeometry(300, 50, 60, 30)

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(340, 50, 240, 30)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide the password by default

        self.encryption_input = QComboBox(self)
        self.encryption_input.addItems(["WEP", "WPA", "PSK", "SAE"])
        self.encryption_input.setGeometry(340, 90, 240, 30)

        self.hide_wifi = QCheckBox("Hide", self)
        self.hide_wifi.setGeometry(340, 120, 240, 30)

        self.show_password = QCheckBox("Voir clé", self)
        self.show_password.setGeometry(400, 105, 240, 60)
        self.show_password.stateChanged.connect(self.toggle_password)  # Connect to the toggle_password function

        self.button = QPushButton("Generate QR Code", self)
        self.button.setGeometry(300, 170, 280, 30)
        self.button.clicked.connect(self.generate_qr_code)

        # Initialize window
        self.setGeometry(500, 500, 600, 400)
        self.setWindowTitle("Generateur QRcode")
        self.show()

    def toggle_password(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)  # Show the password
        else:
            self.password_input.setEchoMode(QLineEdit.Password)  # Hide the password

    def generate_qr_code(self):
        ssid = self.ssid_input.text()
        password = self.password_input.text()
        encryption = self.encryption_input.currentText()
        hide = "H:true" if self.hide_wifi.isChecked() else "H:false"
        wifi_data = f"WIFI:S:{ssid};T:{encryption};P:{password};{hide};;"

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(wifi_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Get the user's home directory
        home_dir = QDir.homePath()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", home_dir, "PNG Files (*.png)")

        if file_path:
            img.save(file_path)
            self.label.setPixmap(QPixmap(file_path))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
