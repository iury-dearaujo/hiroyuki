# -*- coding: utf-8 -*-
import os
import shutil

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextEdit, QLabel, QHBoxLayout, QFileDialog
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox

from auth import APIClient
from files_manager import read_data
from logger import logger_dict
from execution import Execution


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.execution = None
        self.username = ""
        self.password = ""
        self.data_path = None
        self.url = "https://platform.senior.com.br/t/senior.com.br/bridge/1.0/rest/"

        self.api_client = APIClient()

        self.setMinimumSize(450, 450)
        self.setWindowTitle("DOWNLOAD")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.user_layout = QHBoxLayout()
        self.user_label = QLabel("USERNAME:")
        self.user_layout.addWidget(self.user_label)
        self.user_input = QLineEdit()
        self.user_layout.addWidget(self.user_input)
        self.layout.addLayout(self.user_layout)

        self.pass_layout = QHBoxLayout()
        self.pass_label = QLabel("PASSWORD:")
        self.pass_layout.addWidget(self.pass_label)
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_layout.addWidget(self.pass_input)
        self.layout.addLayout(self.pass_layout)

        self.layout_control = QVBoxLayout()

        self.login_button = QPushButton("LOGIN")
        self.login_button.clicked.connect(self.login)  # type: ignore
        self.layout_control.addWidget(self.login_button)

        self.login_reset_button = QPushButton("RESET LOGIN")
        self.login_reset_button.clicked.connect(self.login_reset)  # type: ignore
        self.layout_control.addWidget(self.login_reset_button)

        self.confirm_checkbox = QCheckBox("CONFIRM", self)
        self.confirm_checkbox.setDisabled(True)
        self.layout_control.addWidget(self.confirm_checkbox)

        self.exec_button = QPushButton("EXECUTE", self)
        self.exec_button.clicked.connect(self.on_exec_clicked)  # type: ignore
        self.exec_button.setDisabled(True)
        self.layout_control.addWidget(self.exec_button)

        self.layout.addLayout(self.layout_control)

        self.label_file_path = QLabel("No file selected")
        self.layout.addWidget(self.label_file_path)
        self.button_select_file = QPushButton("Select files")
        self.button_select_file.clicked.connect(self.selectFile)  # type: ignore
        self.layout.addWidget(self.button_select_file)
        self.button_select_file.setDisabled(True)

        self.log_textbox = QTextEdit(self)
        self.log_textbox.setPlaceholderText("Log:")
        self.log_textbox.setReadOnly(True)

        self.log_textbox.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.log_textbox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.layout.addWidget(self.log_textbox)

        self.setLayout(self.layout)

    def selectFile(self):
        if self.confirm_checkbox.isChecked():
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getOpenFileName(
                self, "Select File", "", "All files (*);;Text files (*.txt);;Image files (*.jpg *.png)"
            )
            if file_path:
                self.label_file_path.setText(f"Selected file: {str(file_path).split('/')[-1]}")
                self.log_textbox.append("")
                self.log_textbox.append(f'File path: {str(file_path)}')
                self.copyFileToRoot(file_path)
        else:
            self.log_textbox.append("")
            self.log_textbox.append("Confirm the operation before proceeding!")

    def copyFileToRoot(self, file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            root_file_path = os.path.join(os.getcwd(), file_name)
            if not os.path.exists(root_file_path):
                shutil.copy(file_path, root_file_path)
                self.data_path = file_name
                self.log_textbox.append(f'File copied to root: {file_name}')
            else:
                self.log_textbox.append(f'A file with the same name already exists in the root directory: {file_name}')
        else:
            self.log_textbox.append("Invalid file or file does not exist.")

    def on_exec_clicked(self):
        if self.confirm_checkbox.isChecked():
            self.confirm_checkbox.setDisabled(True)
            self.exec_button.setDisabled(True)
            self.button_select_file.setDisabled(True)

            self.execution = Execution(self.api_client, self.username, self.password)

            callbackReadFile = read_data()
            if callbackReadFile[0] == 0:
                self.execution.pre_admissions = callbackReadFile[2]
                self.log_textbox.append(str(callbackReadFile[1]))
                self.execution.start()
            else:
                self.log_textbox.append(str(callbackReadFile[1]))



        else:
            self.log_textbox.append("")
            self.log_textbox.append("Confirm the operation before proceeding!")

    def login_reset(self):
        self.username = ""
        self.password = ""
        self.user_input.setText("")
        self.pass_input.setText("")
        self.log_textbox.setText("")
        self.confirm_checkbox.setDisabled(True)
        self.confirm_checkbox.setChecked(False)
        self.exec_button.setDisabled(True)
        self.login_button.setDisabled(False)
        self.user_input.setDisabled(False)
        self.pass_input.setDisabled(False)
        self.login_button.setDisabled(False)
        self.button_select_file.setDisabled(True)
        self.api_client = APIClient()

    def login(self):
        self.log_textbox.setText("")
        password_hide = '*' * self.pass_input.text().__len__()
        self.password = self.pass_input.text()
        self.username = self.user_input.text()

        payload = {
            "username": self.username,
            "password": self.password
        }
        self.log_textbox.append(f"Account: {payload.get('username')}, {password_hide}")
        result = self.api_client.login(payload.get('username'), payload.get('password'))
        if result:
            self.user_input.setDisabled(True)
            self.pass_input.setDisabled(True)
            self.login_button.setDisabled(True)
            self.confirm_checkbox.setDisabled(False)
            self.exec_button.setDisabled(False)
            self.button_select_file.setDisabled(False)
            self.log_textbox.append(str(self.api_client.response_status_code))
            self.log_textbox.append(f'token: {"*" * str(self.api_client.token).__len__()}')
            self.log_textbox.append("Login - Success")
        else:
            self.log_textbox.append(str(self.api_client.response_status_code))
            self.log_textbox.append(logger_dict('domain', self.api_client.response_complete))
            self.log_textbox.append(logger_dict('service', self.api_client.response_complete))
            self.log_textbox.append(logger_dict('errorCode', self.api_client.response_complete))
            self.log_textbox.append(logger_dict('reason', self.api_client.response_complete))
            self.log_textbox.append(logger_dict('message', self.api_client.response_complete))
            self.log_textbox.append("Login - Filed")
            self.user_input.setText("")
            self.pass_input.setText("")
