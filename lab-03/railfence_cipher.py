import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow
import requests

from PyQt5 import QtWidgets, QtCore

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Restructure grid layout to add validation labels
        self.ui.gridLayout.removeWidget(self.ui.label_plain)
        self.ui.gridLayout.removeWidget(self.ui.txt_plain_text)
        self.ui.gridLayout.removeWidget(self.ui.label_key)
        self.ui.gridLayout.removeWidget(self.ui.txt_key)
        self.ui.gridLayout.removeWidget(self.ui.label_cipher)
        self.ui.gridLayout.removeWidget(self.ui.txt_cipher_text)

        # Create validation labels
        self.lbl_plain_error = QtWidgets.QLabel(self)
        self.lbl_plain_error.setStyleSheet("color: red; font-size: 11px;")
        self.lbl_key_error = QtWidgets.QLabel(self)
        self.lbl_key_error.setStyleSheet("color: red; font-size: 11px;")
        self.lbl_cipher_error = QtWidgets.QLabel(self)
        self.lbl_cipher_error.setStyleSheet("color: red; font-size: 11px;")

        # Re-add widgets with error rows
        self.ui.gridLayout.addWidget(self.ui.label_plain, 0, 0)
        self.ui.gridLayout.addWidget(self.ui.txt_plain_text, 0, 1)
        self.ui.gridLayout.addWidget(self.lbl_plain_error, 1, 1)

        self.ui.gridLayout.addWidget(self.ui.label_key, 2, 0)
        self.ui.gridLayout.addWidget(self.ui.txt_key, 2, 1)
        self.ui.gridLayout.addWidget(self.lbl_key_error, 3, 1)

        self.ui.gridLayout.addWidget(self.ui.label_cipher, 4, 0)
        self.ui.gridLayout.addWidget(self.ui.txt_cipher_text, 4, 1)
        self.ui.gridLayout.addWidget(self.lbl_cipher_error, 5, 1)

        # Resize to fit validation labels
        self.resize(500, 480)

        # Connect signals for real-time validation
        self.ui.txt_plain_text.textChanged.connect(self.validate_inputs)
        self.ui.txt_key.textChanged.connect(self.validate_inputs)
        self.ui.txt_cipher_text.textChanged.connect(self.validate_inputs)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

        # Run initial validation
        self.validate_inputs()

    def validate_inputs(self):
        # Validate Plain Text
        plain_text = self.ui.txt_plain_text.toPlainText()
        plain_valid = True
        if not plain_text:
            self.lbl_plain_error.setText("")
            self.ui.txt_plain_text.setStyleSheet("")
            plain_valid = False
        else:
            self.lbl_plain_error.setText("")
            self.ui.txt_plain_text.setStyleSheet("")

        # Validate Key
        key_text = self.ui.txt_key.text().strip()
        key_valid = True
        if not key_text:
            self.lbl_key_error.setText("")
            self.ui.txt_key.setStyleSheet("")
            key_valid = False
        else:
            try:
                key = int(key_text)
                if key <= 1:
                    self.lbl_key_error.setText("Key phải là số nguyên lớn hơn 1.")
                    self.ui.txt_key.setStyleSheet("border: 1px solid red;")
                    key_valid = False
                else:
                    self.lbl_key_error.setText("")
                    self.ui.txt_key.setStyleSheet("")
            except ValueError:
                self.lbl_key_error.setText("Key phải là số nguyên.")
                self.ui.txt_key.setStyleSheet("border: 1px solid red;")
                key_valid = False

        # Validate Cipher Text
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        cipher_valid = True
        if not cipher_text:
            self.lbl_cipher_error.setText("")
            self.ui.txt_cipher_text.setStyleSheet("")
            cipher_valid = False
        else:
            self.lbl_cipher_error.setText("")
            self.ui.txt_cipher_text.setStyleSheet("")

        # Enable/Disable Buttons
        self.ui.btn_encrypt.setEnabled(plain_valid and key_valid)
        self.ui.btn_decrypt.setEnabled(cipher_valid and key_valid)

    def call_api_encrypt(self):
        key = int(self.ui.txt_key.text().strip())
        plain_text = self.ui.txt_plain_text.toPlainText()

        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.blockSignals(True)
                self.ui.txt_cipher_text.setText(data["encrypted_text"])
                self.ui.txt_cipher_text.blockSignals(False)
                self.validate_inputs()
                
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "API Error", "Error while calling Encryption API.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Cannot connect to API server:\n{str(e)}")

    def call_api_decrypt(self):
        key = int(self.ui.txt_key.text().strip())
        cipher_text = self.ui.txt_cipher_text.toPlainText()

        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.blockSignals(True)
                self.ui.txt_plain_text.setText(data["decrypted_text"])
                self.ui.txt_plain_text.blockSignals(False)
                self.validate_inputs()
                
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "API Error", "Error while calling Decryption API.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Cannot connect to API server:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())
