from os import system
from sys import argv, exit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox


class SimpleTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.input_font = QFont('Droid Sans Mono', 50)
        self.button_font = QFont('Droid Sans Mono', 25, weight=1)
        self.label_font = QFont('Droid Sans Mono', 15)
        self.timer_font = QFont('Droid Sans Mono', 100, weight=1)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout_action)

        self.is_work_time = True

        self.setup_ui()

    def timeout_action(self):
        m, s = self.text_to_min_sec(self.timer_label)
        curr_time = m*60 + s - 1
        self.timer_label.setText("%02d:%02d" % (curr_time//60, curr_time%60))

        if not curr_time:
            self.timer_label.setStyleSheet('color: black')
            self.is_work_time = not self.is_work_time
            system("play -nq -t alsa synth 1 sin 1200")
            if not self.is_work_time:
                sets_left = int(self.sets_left.text()) - 1
                self.sets_left.setText("%02d" % sets_left)
                if not sets_left:
                    self.stop_timer_action()
                    system("play -nq -t alsa synth 1 sin 1200")
                    return
            self.timer_label.setText([self.rest_time_input.text(), self.work_time_input.text()][self.is_work_time])
        elif curr_time <= 5:
            self.timer_label.setStyleSheet('color: ' + ['black', 'red'][curr_time%2])
            if curr_time <= 3:
                system("play -nq -t alsa synth 0.25 sin 1200")

    def text_to_min_sec(self, label):
        text = label.text()
        return (int(text[:2]), int(text[-2:]))

    def sets_minus_action(self):
        sets = int(self.sets_input.text()) - 1
        if sets < 1:
            sets = 1
        self.sets_input.setText("%02d" % sets)

    def sets_plus_action(self):
        sets = int(self.sets_input.text()) + 1
        self.sets_input.setText("%02d" % sets)

    def generate_sets_input_layout(self):
        layout = QHBoxLayout()

        minus_button = QPushButton('-', font=self.button_font)
        minus_button.clicked.connect(self.sets_minus_action)
        layout.addWidget(minus_button)
        layout.addSpacing(20)

        self.sets_input = QLabel("06", alignment=Qt.AlignCenter, font=self.input_font)
        layout.addWidget(self.sets_input)
        layout.addSpacing(20)

        plus_button = QPushButton('+', font=self.button_font)
        plus_button.clicked.connect(self.sets_plus_action)
        layout.addWidget(plus_button)

        return layout

    def work_time_minus_action(self):
        m, s = self.text_to_min_sec(self.work_time_input)
        work_time = m*60 + s - 15
        if work_time < 15:
            work_time = 15
        self.work_time_input.setText("%02d:%02d" % ( work_time//60, work_time%60 ))

    def work_time_plus_action(self):
        m, s = self.text_to_min_sec(self.work_time_input)
        work_time = m*60 + s + 15
        self.work_time_input.setText("%02d:%02d" % ( work_time//60, work_time%60 ))

    def generate_work_time_input_layout(self):
        layout = QHBoxLayout()

        minus_button = QPushButton('-', font=self.button_font)
        minus_button.clicked.connect(self.work_time_minus_action)
        layout.addWidget(minus_button)
        layout.addSpacing(20)

        self.work_time_input = QLabel("%02d:%02d" % ( 6, 0 ), alignment=Qt.AlignCenter, font=self.input_font)
        layout.addWidget(self.work_time_input)
        layout.addSpacing(20)

        plus_button = QPushButton('+', font=self.button_font)
        plus_button.clicked.connect(self.work_time_plus_action)
        layout.addWidget(plus_button)

        return layout

    def rest_time_minus_action(self):
        m, s = self.text_to_min_sec(self.rest_time_input)
        rest_time = m*60 + s - 15
        if rest_time < 15:
            rest_time = 15
        self.rest_time_input.setText("%02d:%02d" % ( rest_time//60, rest_time%60 ))

    def rest_time_plus_action(self):
        m, s = self.text_to_min_sec(self.rest_time_input)
        rest_time = m*60 + s + 15
        self.rest_time_input.setText("%02d:%02d" % ( rest_time//60, rest_time%60 ))

    def generate_rest_time_input_layout(self):
        layout = QHBoxLayout()

        minus_button = QPushButton('-', font=self.button_font)
        minus_button.clicked.connect(self.rest_time_minus_action)
        layout.addWidget(minus_button)
        layout.addSpacing(20)

        self.rest_time_input = QLabel("%02d:%02d" % ( 2, 0 ), alignment=Qt.AlignCenter, font=self.input_font)
        layout.addWidget(self.rest_time_input)
        layout.addSpacing(20)

        plus_button = QPushButton('+', font=self.button_font)
        plus_button.clicked.connect(self.rest_time_plus_action)
        layout.addWidget(plus_button)

        return layout

    def start_timer_action(self):
        self.start_button.setVisible(False)
        self.resume_button.setVisible(False)
        self.pause_button.setVisible(True)
        self.stop_button.setVisible(True)

        self.sets_left.setText(self.sets_input.text())
        self.timer_label.setText(self.work_time_input.text())

        self.timer.start()

    def resume_timer_action(self):
        self.start_button.setVisible(False)
        self.resume_button.setVisible(False)
        self.pause_button.setVisible(True)
        self.stop_button.setVisible(True)

        self.timer.start()

    def pause_timer_action(self):
        self.start_button.setVisible(False)
        self.resume_button.setVisible(True)
        self.pause_button.setVisible(False)
        self.stop_button.setVisible(True)

        self.timer.stop()

    def stop_timer_action(self):
        self.start_button.setVisible(True)
        self.resume_button.setVisible(False)
        self.pause_button.setVisible(False)
        self.stop_button.setVisible(False)

        self.timer_label.setStyleSheet('color: black')

        self.timer.stop()

    def generate_control_buttons_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 50, 0, 50)

        self.start_button = QPushButton('START', font=self.button_font)
        self.start_button.clicked.connect(self.start_timer_action)
        self.start_button.setVisible(True)
        self.start_button.setStyleSheet('background-color: green; color: white')
        layout.addWidget(self.start_button)

        self.resume_button = QPushButton('RESUME', font=self.button_font)
        self.resume_button.clicked.connect(self.resume_timer_action)
        self.resume_button.setStyleSheet('background-color: blue; color: white')
        self.resume_button.setVisible(False)
        layout.addWidget(self.resume_button)

        self.pause_button = QPushButton('PAUSE', font=self.button_font)
        self.pause_button.clicked.connect(self.pause_timer_action)
        self.pause_button.setStyleSheet('background-color: blue; color: white')
        self.pause_button.setVisible(False)
        layout.addWidget(self.pause_button)

        self.stop_button = QPushButton('STOP', font=self.button_font)
        self.stop_button.clicked.connect(self.stop_timer_action)
        self.stop_button.setStyleSheet('background-color: red; color: white')
        self.stop_button.setVisible(False)
        layout.addWidget(self.stop_button)

        return layout

    def generate_input_layout(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel('SETS', alignment=Qt.AlignCenter, font=self.label_font))
        layout.addLayout(self.generate_sets_input_layout())

        layout.addWidget(QLabel('WORK TIME', alignment=Qt.AlignCenter, font=self.label_font))
        layout.addLayout(self.generate_work_time_input_layout())

        layout.addWidget(QLabel('REST TIME', alignment=Qt.AlignCenter, font=self.label_font))
        layout.addLayout(self.generate_rest_time_input_layout())

        layout.addLayout(self.generate_control_buttons_layout())

        return layout

    def show_help(self):
        help_message_box = QMessageBox()
        help_message_box.setWindowTitle('Help')
        help_message_box.setIcon(QMessageBox.Question)
        help_message_box.setText("If there's no sound, install sox!\nsudo apt install sox")
        help_message_box.exec_()

    def generate_timer_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 40, 0, 0)

        layout.addWidget(QLabel('SETS LEFT', alignment=Qt.AlignCenter, font=self.label_font))
        self.sets_left = QLabel('00', alignment=Qt.AlignCenter, font=self.input_font)
        layout.addWidget(self.sets_left)

        self.timer_label = QLabel('00:00', alignment=Qt.AlignCenter, font=self.timer_font)
        layout.addWidget(self.timer_label, stretch=1)

        help_button_font = QFont(self.button_font)
        help_button = QPushButton('?', font=self.button_font)
        help_button.setMaximumWidth(60)
        help_button.clicked.connect(self.show_help)
        layout.addWidget(help_button, alignment=Qt.AlignBottom | Qt.AlignRight)

        return layout

    def setup_ui(self):
        self.setWindowTitle('Simple Timer')

        central_widget = QHBoxLayout(self)
        central_widget.setAlignment(Qt.AlignCenter)
        central_widget.setContentsMargins(100, 30, 100, 30)
        central_widget.addLayout(self.generate_input_layout())
        central_widget.addSpacing(100)
        central_widget.addLayout(self.generate_timer_layout(), 1)


if __name__ == '__main__':
    app = QApplication(argv)
    window = SimpleTimer()
    window.show()
    exit(app.exec_())
