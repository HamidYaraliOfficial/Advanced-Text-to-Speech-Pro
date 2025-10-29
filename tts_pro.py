import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QComboBox, QLabel, QProgressBar,
    QFileDialog, QGroupBox, QRadioButton, QButtonGroup, QScrollArea,
    QFrame, QSpacerItem, QSizePolicy, QGridLayout, QTabWidget,
    QFormLayout, QLineEdit, QSpinBox, QCheckBox, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QLinearGradient, QBrush, QPixmap
from gtts import gTTS
from gtts.lang import tts_langs
import pygame
import tempfile
import uuid

# Thread for TTS conversion
class TTSThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text, lang, output_file, tld='com'):
        super().__init__()
        self.text = text
        self.lang = lang
        self.output_file = output_file
        self.tld = tld

    def run(self):
        try:
            total = len(self.text)
            if total == 0:
                self.error.emit("Text is empty!")
                return

            chunk_size = 4000
            temp_files = []
            for i in range(0, total, chunk_size):
                chunk = self.text[i:i + chunk_size]
                tts = gTTS(text=chunk, lang=self.lang, tld=self.tld, slow=False)
                temp_fd, temp_path = tempfile.mkstemp(suffix='.mp3')
                os.close(temp_fd)
                tts.save(temp_path)
                temp_files.append(temp_path)
                progress_percent = int((i + chunk_size) / total * 100)
                self.progress.emit(min(progress_percent, 100))

            # Merge audio files
            pygame.mixer.init()
            merged = None
            for temp_path in temp_files:
                sound = pygame.mixer.Sound(temp_path)
                if merged is None:
                    merged = sound
                else:
                    channel = merged.play()
                    while channel.get_busy():
                        pygame.time.wait(100)
                    merged = sound
                os.remove(temp_path)

            if merged:
                merged_sound = pygame.mixer.Sound(buffer=merged.get_raw())
                pygame.mixer.music.load(merged_sound.get_raw())
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)

            self.finished.emit(self.output_file)
        except Exception as e:
            self.error.emit(str(e))


# Main Window
class TTSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Text-to-Speech Converter")
        self.setWindowIcon(QIcon(self.resource_path("icon.ico")))
        self.setMinimumSize(1000, 720)
        self.current_theme = "Windows11"
        self.current_lang = "en"
        self.is_dark = False
        self.output_format = "mp3"
        self.speed = 1.0
        self.volume = 1.0
        self.voice_tld = "com"
        self.init_ui()
        self.apply_theme()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Tabs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setStyleSheet("QTabBar::tab { height: 40px; width: 150px; }")
        main_layout.addWidget(tabs)

        # Main Tab
        main_tab = self.create_main_tab()
        tabs.addTab(main_tab, self.tr("Main"))

        # Settings Tab
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, self.tr("Settings"))

        # Themes Tab
        themes_tab = self.create_themes_tab()
        tabs.addTab(themes_tab, self.tr("Themes"))

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

    def create_header(self):
        header = QGroupBox()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Text-to-Speech Pro")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lang_group = QGroupBox(self.tr("Language"))
        lang_layout = QHBoxLayout(lang_group)
        self.lang_combo = QComboBox()
        self.populate_languages()
        lang_layout.addWidget(self.lang_combo)

        header_layout.addWidget(title, 2)
        header_layout.addWidget(lang_group, 1)

        return header

    def populate_languages(self):
        languages = {
            "en": ("English", Qt.AlignmentFlag.AlignLeft),
            "fa": ("فارسی", Qt.AlignmentFlag.AlignRight),
            "zh-CN": ("中文", Qt.AlignmentFlag.AlignLeft),
            "ru": ("Русский", Qt.AlignmentFlag.AlignRight),
        }
        for code, (name, align) in languages.items():
            self.lang_combo.addItem(name, code)
        self.lang_combo.currentIndexChanged.connect(self.change_language)

    def create_main_tab(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(15)

        # Text Input
        text_group = QGroupBox(self.tr("Input Text"))
        text_layout = QVBoxLayout(text_group)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(self.tr("Enter your text here..."))
        self.text_edit.setFont(QFont("Segoe UI", 11))
        text_layout.addWidget(self.text_edit)

        # Controls
        control_group = QGroupBox(self.tr("Controls"))
        control_layout = QHBoxLayout(control_group)
        control_layout.setSpacing(10)

        self.convert_btn = QPushButton(self.tr("Convert to Speech"))
        self.convert_btn.setIcon(QIcon(self.resource_path("convert.png")))
        self.convert_btn.setMinimumHeight(45)
        self.convert_btn.clicked.connect(self.start_conversion)

        self.save_btn = QPushButton(self.tr("Save As..."))
        self.save_btn.setIcon(QIcon(self.resource_path("save.png")))
        self.save_btn.setMinimumHeight(45)
        self.save_btn.clicked.connect(self.save_file)

        self.play_btn = QPushButton(self.tr("Play"))
        self.play_btn.setIcon(QIcon(self.resource_path("play.png")))
        self.play_btn.setMinimumHeight(45)
        self.play_btn.clicked.connect(self.play_audio)

        self.stop_btn = QPushButton(self.tr("Stop"))
        self.stop_btn.setIcon(QIcon(self.resource_path("stop.png")))
        self.stop_btn.setMinimumHeight(45)
        self.stop_btn.clicked.connect(self.stop_audio)

        control_layout.addWidget(self.convert_btn)
        control_layout.addWidget(self.save_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.stop_btn)

        # Output Format
        format_group = QGroupBox(self.tr("Output Format"))
        format_layout = QHBoxLayout(format_group)
        self.format_mp3 = QRadioButton("MP3")
        self.format_wav = QRadioButton("WAV")
        self.format_mp3.setChecked(True)
        format_layout.addWidget(self.format_mp3)
        format_layout.addWidget(self.format_wav)
        self.format_group = QButtonGroup()
        self.format_group.addButton(self.format_mp3, 0)
        self.format_group.addButton(self.format_wav, 1)

        layout.addWidget(text_group, 0, 0, 1, 2)
        layout.addWidget(control_group, 1, 0, 1, 2)
        layout.addWidget(format_group, 2, 0, 1, 2)

        return widget

    def create_settings_tab(self):
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        container = QWidget()
        layout = QFormLayout(container)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        # Speed
        speed_label = QLabel(self.tr("Speed:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        self.speed_slider.valueChanged.connect(self.update_speed)
        self.speed_value = QLabel("1.0x")
        speed_row = QHBoxLayout()
        speed_row.addWidget(self.speed_slider)
        speed_row.addWidget(self.speed_value)
        layout.addRow(speed_label, speed_row)

        # Volume
        volume_label = QLabel(self.tr("Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.update_volume)
        self.volume_value = QLabel("100%")
        volume_row = QHBoxLayout()
        volume_row.addWidget(self.volume_slider)
        volume_row.addWidget(self.volume_value)
        layout.addRow(volume_label, volume_row)

        # TLD (Accent)
        tld_label = QLabel(self.tr("Accent (TLD):"))
        self.tld_combo = QComboBox()
        tlds = {
            "com": "Default (US)",
            "co.uk": "United Kingdom",
            "ca": "Canada",
            "com.au": "Australia",
            "co.in": "India",
            "ie": "Ireland",
        }
        for code, name in tlds.items():
            self.tld_combo.addItem(name, code)
        layout.addRow(tld_label, self.tld_combo)

        # Slow Mode
        self.slow_check = QCheckBox(self.tr("Slow Speech"))
        layout.addRow("", self.slow_check)

        # Auto Save
        self.auto_save_check = QCheckBox(self.tr("Auto Save After Conversion"))
        layout.addRow("", self.auto_save_check)

        # File Naming
        name_label = QLabel(self.tr("Default File Name:"))
        self.name_edit = QLineEdit("output_audio")
        layout.addRow(name_label, self.name_edit)

        # Output Directory
        dir_label = QLabel(self.tr("Output Directory:"))
        dir_layout = QHBoxLayout()
        self.dir_edit = QLineEdit(os.path.expanduser("~/Desktop"))
        self.dir_browse = QPushButton("...")
        self.dir_browse.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.dir_edit)
        dir_layout.addWidget(self.dir_browse)
        layout.addRow(dir_label, dir_layout)

        widget.setWidget(container)
        return widget

    def create_themes_tab(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(15)

        themes = [
            ("Windows11", "Windows 11 Default"),
            ("Light", "Light Theme"),
            ("Dark", "Dark Theme"),
            ("Blue", "Ocean Blue"),
            ("Red", "Crimson Red"),
        ]

        row, col = 0, 0
        self.theme_buttons = QButtonGroup()
        self.theme_buttons.setExclusive(True)
        for idx, (key, name) in enumerate(themes):
            btn = QRadioButton(name)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("QRadioButton { font-size: 14px; }")
            if key == "Windows11":
                btn.setChecked(True)
            self.theme_buttons.addButton(btn, idx)
            layout.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.theme_buttons.buttonClicked.connect(self.apply_theme_by_button)

        return widget

    def change_language(self, index):
        lang_code = self.lang_combo.itemData(index)
        self.current_lang = lang_code
        self.retranslate_ui()
        self.update_text_alignment()

    def update_text_alignment(self):
        align = Qt.AlignmentFlag.AlignRight if self.current_lang in ["fa", "ru"] else Qt.AlignmentFlag.AlignLeft
        self.text_edit.setAlignment(align)
        self.apply_rtl_if_needed()

    def apply_rtl_if_needed(self):
        if self.current_lang in ["fa", "ru"]:
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("Advanced Text-to-Speech Converter"))
        # Re-translate all widgets
        self.convert_btn.setText(self.tr("Convert to Speech"))
        self.save_btn.setText(self.tr("Save As..."))
        self.play_btn.setText(self.tr("Play"))
        self.stop_btn.setText(self.tr("Stop"))

    def update_speed(self, value):
        self.speed = value / 100.0
        self.speed_value.setText(f"{self.speed:.1f}x")

    def update_volume(self, value):
        self.volume = value / 100.0
        self.volume_value.setText(f"{value}%")

    def start_conversion(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            self.status_label.setText(self.tr("Error: Text is empty!"))
            return

        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setText(self.tr("Converting..."))

        output_file = os.path.join(
            self.dir_edit.text(),
            f"{self.name_edit.text() or 'output'}.{self.output_format}"
        )

        self.tts_thread = TTSThread(
            text=text,
            lang=self.current_lang,
            output_file=output_file,
            tld=self.tld_combo.currentData()
        )
        self.tts_thread.progress.connect(self.progress.setValue)
        self.tts_thread.finished.connect(self.conversion_finished)
        self.tts_thread.error.connect(self.conversion_error)
        self.tts_thread.start()

    def conversion_finished(self, file_path):
        self.progress.setVisible(False)
        self.status_label.setText(self.tr(f"Saved: {os.path.basename(file_path)}"))
        if self.auto_save_check.isChecked():
            self.save_file(file_path)

    def conversion_error(self, msg):
        self.progress.setVisible(False)
        self.status_label.setText(self.tr(f"Error: {msg}"))

    def save_file(self, default_path=None):
        formats = {
            0: ("MP3 Files (*.mp3)", ".mp3"),
            1: ("WAV Files (*.wav)", ".wav"),
        }
        fmt_idx = self.format_group.checkedId()
        filter_str, ext = formats[fmt_idx]
        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Save Audio File"), default_path or "", filter_str
        )
        if file_path:
            if not file_path.endswith(ext):
                file_path += ext
            # In real app, convert format here
            self.status_label.setText(self.tr(f"Saved: {os.path.basename(file_path)}"))

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.last_output or self.resource_path("sample.mp3"))
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, self.tr("Select Output Directory"))
        if dir_path:
            self.dir_edit.setText(dir_path)

    def apply_theme_by_button(self, button):
        themes = ["Windows11", "Light", "Dark", "Blue", "Red"]
        idx = self.theme_buttons.id(button)
        self.current_theme = themes[idx]
        self.apply_theme()

    def apply_theme(self):
        app = QApplication.instance()
        palette = QPalette()

        if self.current_theme == "Windows11":
            app.setStyle("windowsvista")
            palette = app.palette()
        elif self.current_theme == "Light":
            palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 247))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Button, QColor(230, 230, 230))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        elif self.current_theme == "Dark":
            palette.setColor(QPalette.ColorRole.Window, QColor(32, 32, 32))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 40))
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        elif self.current_theme == "Blue":
            palette.setColor(QPalette.ColorRole.Window, QColor(10, 25, 50))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 230, 255))
            palette.setColor(QPalette.ColorRole.Base, QColor(15, 35, 70))
            palette.setColor(QPalette.ColorRole.Text, QColor(200, 230, 255))
            palette.setColor(QPalette.ColorRole.Button, QColor(20, 50, 100))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(200, 230, 255))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(100, 180, 255))
        elif self.current_theme == "Red":
            palette.setColor(QPalette.ColorRole.Window, QColor(50, 10, 10))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 200, 200))
            palette.setColor(QPalette.ColorRole.Base, QColor(70, 15, 15))
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 200, 200))
            palette.setColor(QPalette.ColorRole.Button, QColor(100, 20, 20))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 200, 200))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 100, 100))

        app.setPalette(palette)
        self.update_styles()

    def update_styles(self):
        gradient = ""
        if self.current_theme == "Blue":
            gradient = "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0a1940, stop:1 #1e3a8a); color: #c8e6ff;"
        elif self.current_theme == "Red":
            gradient = "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #320a0a, stop:1 #8a1e1e); color: #ffc8c8;"

        stylesheet = f"""
        QMainWindow {{ {gradient} }}
        QGroupBox {{ font-weight: bold; border: 2px solid #444; border-radius: 8px; margin-top: 10px; padding: 10px; }}
        QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px; }}
        QPushButton {{ border: none; border-radius: 8px; padding: 12px; font-weight: bold; }}
        QPushButton:hover {{ background-color: rgba(255,255,255,0.1); }}
        QTextEdit, QLineEdit {{ border: 1px solid #555; border-radius: 6px; padding: 8px; }}
        QComboBox, QSlider {{ border: 1px solid #555; border-radius: 6px; padding: 5px; }}
        QProgressBar {{ border: 1px solid #555; border-radius: 6px; text-align: center; }}
        QTabWidget::pane {{ border: 1px solid #444; border-radius: 8px; }}
        QTabBar::tab {{ background: #333; color: white; padding: 10px; margin: 2px; border-top-left-radius: 6px; border-top-right-radius: 6px; }}
        QTabBar::tab:selected {{ background: #0078d4; }}
        """
        self.setStyleSheet(stylesheet)

    def tr(self, text):
        translations = {
            "en": {
                "Main": "Main",
                "Settings": "Settings",
                "Themes": "Themes",
                "Language": "Language",
                "Input Text": "Input Text",
                "Controls": "Controls",
                "Convert to Speech": "Convert to Speech",
                "Save As...": "Save As...",
                "Play": "Play",
                "Stop": "Stop",
                "Output Format": "Output Format",
                "Speed:": "Speed:",
                "Volume:": "Volume:",
                "Accent (TLD):": "Accent (TLD):",
                "Slow Speech": "Slow Speech",
                "Auto Save After Conversion": "Auto Save After Conversion",
                "Default File Name:": "Default File Name:",
                "Output Directory:": "Output Directory:",
                "Select Output Directory": "Select Output Directory",
                "Error: Text is empty!": "Error: Text is empty!",
                "Converting...": "Converting...",
                "Saved:": "Saved:",
                "Ready": "Ready",
            },
            "fa": {
                "Main": "اصلی",
                "Settings": "تنظیمات",
                "Themes": "تم‌ها",
                "Language": "زبان",
                "Input Text": "متن ورودی",
                "Controls": "کنترل‌ها",
                "Convert to Speech": "تبدیل به گفتار",
                "Save As...": "ذخیره با نام...",
                "Play": "پخش",
                "Stop": "توقف",
                "Output Format": "فرمت خروجی",
                "Speed:": "سرعت:",
                "Volume:": "حجم صدا:",
                "Accent (TLD):": "لهجه (TLD):",
                "Slow Speech": "گفتار آهسته",
                "Auto Save After Conversion": "ذخیره خودکار پس از تبدیل",
                "Default File Name:": "نام فایل پیش‌فرض:",
                "Output Directory:": "مسیر خروجی:",
                "Select Output Directory": "انتخاب مسیر خروجی",
                "Error: Text is empty!": "خطا: متن خالی است!",
                "Converting...": "در حال تبدیل...",
                "Saved:": "ذخیره شد:",
                "Ready": "آماده",
            },
            "zh-CN": {
                "Main": "主要",
                "Settings": "设置",
                "Themes": "主题",
                "Language": "语言",
                "Input Text": "输入文本",
                "Controls": "控制",
                "Convert to Speech": "转换为语音",
                "Save As...": "另存为...",
                "Play": "播放",
                "Stop": "停止",
                "Output Format": "输出格式",
                "Speed:": "速度:",
                "Volume:": "音量:",
                "Accent (TLD):": "口音 (TLD):",
                "Slow Speech": "慢速语音",
                "Auto Save After Conversion": "转换后自动保存",
                "Default File Name:": "默认文件名:",
                "Output Directory:": "输出目录:",
                "Select Output Directory": "选择输出目录",
                "Error: Text is empty!": "错误：文本为空！",
                "Converting...": "正在转换...",
                "Saved:": "已保存:",
                "Ready": "就绪",
            },
            "ru": {
                "Main": "Основное",
                "Settings": "Настройки",
                "Themes": "Темы",
                "Language": "Язык",
                "Input Text": "Входной текст",
                "Controls": "Управление",
                "Convert to Speech": "Преобразовать в речь",
                "Save As...": "Сохранить как...",
                "Play": "Воспроизвести",
                "Stop": "Остановить",
                "Output Format": "Формат вывода",
                "Speed:": "Скорость:",
                "Volume:": "Громкость:",
                "Accent (TLD):": "Акцент (TLD):",
                "Slow Speech": "Медленная речь",
                "Auto Save After Conversion": "Автосохранение после конвертации",
                "Default File Name:": "Имя файла по умолчанию:",
                "Output Directory:": "Каталог вывода:",
                "Select Output Directory": "Выбрать каталог",
                "Error: Text is empty!": "Ошибка: Текст пуст!",
                "Converting...": "Преобразование...",
                "Saved:": "Сохранено:",
                "Ready": "Готово",
            },
        }
        return translations.get(self.current_lang, translations["en"]).get(text, text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("TTS Pro")
    app.setOrganizationName("xAI Labs")
    window = TTSApp()
    window.show()
    sys.exit(app.exec())