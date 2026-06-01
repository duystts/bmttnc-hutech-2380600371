import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.vigenere import Ui_MainWindow
import requests

class VigenereApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        key_text = self.ui.txt_key.text().strip()
        if not key_text:
            QMessageBox.warning(self, "Validation Error", "Key field cannot be empty.")
            return

        plain_text = self.ui.txt_plain_text.toPlainText()
        if not plain_text:
            QMessageBox.warning(self, "Validation Error", "Plain text field cannot be empty.")
            return

        url = "http://127.0.0.1:5000/api/vigenere/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key_text
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_text"])
                
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
        key_text = self.ui.txt_key.text().strip()
        if not key_text:
            QMessageBox.warning(self, "Validation Error", "Key field cannot be empty.")
            return

        cipher_text = self.ui.txt_cipher_text.toPlainText()
        if not cipher_text:
            QMessageBox.warning(self, "Validation Error", "CipherText field cannot be empty.")
            return

        url = "http://127.0.0.1:5000/api/vigenere/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key_text
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_text"])
                
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
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())
