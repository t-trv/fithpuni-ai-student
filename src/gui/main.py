"""
AI Summary Application - Ollama-Inspired Design
Ứng dụng tóm tắt văn bản sử dụng AI
Sử dụng Ollama local models để tóm tắt file .txt, .pdf, .docx
Design inspired by Ollama - Radical minimalism, pure grayscale
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from datetime import datetime
from ..logic.file_reader import FileReader
from ..logic.ai_summarizer import AISummarizer


# Ollama Design System Colors
class OllamaColors:
    PURE_BLACK = "#000000"
    NEAR_BLACK = "#262626"
    PURE_WHITE = "#ffffff"
    SNOW = "#fafafa"
    LIGHT_GRAY = "#e5e5e5"
    STONE = "#737373"
    MID_GRAY = "#525252"
    SILVER = "#a3a3a3"
    BUTTON_TEXT_DARK = "#404040"


class OllamaStyle:
    """Custom ttk styles following Ollama design system"""

    @staticmethod
    def configure_styles(root):
        style = ttk.Style(root)

        available_themes = style.theme_names()
        if "clam" in available_themes:
            style.theme_use("clam")
        elif "alt" in available_themes:
            style.theme_use("alt")

        # Frame
        style.configure("Ollama.TFrame", background=OllamaColors.PURE_WHITE)

        # Label
        style.configure(
            "Ollama.TLabel",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 14),
        )

        # Button styles
        style.configure(
            "GrayPill.TButton",
            background=OllamaColors.LIGHT_GRAY,
            foreground=OllamaColors.NEAR_BLACK,
            font=("Segoe UI", 13),
            padding=(20, 8),
            borderwidth=1,
            relief="solid",
        )
        style.map("GrayPill.TButton", background=[("active", OllamaColors.MID_GRAY)])

        style.configure(
            "BlackPill.TButton",
            background=OllamaColors.PURE_BLACK,
            foreground=OllamaColors.PURE_WHITE,
            font=("Segoe UI", 13),
            padding=(20, 8),
            borderwidth=0,
            relief="flat",
        )
        style.map("BlackPill.TButton", background=[("active", OllamaColors.NEAR_BLACK)])

        style.configure(
            "WhitePill.TButton",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.BUTTON_TEXT_DARK,
            font=("Segoe UI", 13),
            padding=(20, 8),
            borderwidth=1,
            relief="solid",
        )
        style.map("WhitePill.TButton", background=[("active", OllamaColors.LIGHT_GRAY)])

        # Entry
        style.configure(
            "Ollama.TEntry",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            fieldbackground=OllamaColors.PURE_WHITE,
            borderwidth=1,
            relief="solid",
            padding=(12, 8),
            font=("Segoe UI", 13),
        )

        # Combobox
        style.configure(
            "Ollama.TCombobox",
            background=OllamaColors.PURE_WHITE,
            fieldbackground=OllamaColors.PURE_WHITE,
            borderwidth=1,
            relief="solid",
            padding=(8, 6),
        )

        # Radiobutton
        style.configure(
            "Ollama.TRadiobutton",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 12),
        )

        # Scale
        style.configure(
            "Ollama.Horizontal.TScale",
            background=OllamaColors.PURE_WHITE,
            troughcolor=OllamaColors.LIGHT_GRAY,
            slidercolor=OllamaColors.PURE_BLACK,
            borderwidth=0,
            thickness=4,
        )

        # Progressbar
        style.configure(
            "Ollama.Horizontal.TProgressbar",
            background=OllamaColors.LIGHT_GRAY,
            troughcolor=OllamaColors.SNOW,
            borderwidth=0,
            thickness=4,
        )

        return style


class AISummaryApp:
    """Main application class with Ollama-inspired UI"""

    def __init__(self, root):
        self.root = root
        self.root.title("FITHPUni AI Student")
        self.root.geometry("1000x750")
        self.root.configure(bg=OllamaColors.PURE_WHITE)
        self.root.minsize(900, 650)

        self.style = OllamaStyle.configure_styles(self.root)

        self.file_reader = FileReader()
        self.ai_summarizer = AISummarizer()
        self.current_file = None
        self.current_summary = ""
        self.original_content = ""
        self.original_word_count = 0
        self.summary_word_count = 0
        self.stop_event = threading.Event()
        self.translation_cache = {}
        self.original_summary = None

        # Shared variables for all views
        self.model_var = tk.StringVar(value=self.ai_summarizer.model_name)
        self.length_var = tk.IntVar(value=500)
        self.summary_type = tk.StringVar(value="normal")
        self.translate_var = tk.StringVar(value="none")

        self.current_view = "chat"

        self.create_menu()
        self.create_main_container()
        self.show_view("chat")

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(
            self.root,
            bg=OllamaColors.PURE_WHITE,
            fg=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 11),
            bd=0,
            relief="flat",
        )
        self.root.config(menu=menubar)

        # Chế độ menu - để chuyển đổi giữa các chế độ
        mode_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=OllamaColors.PURE_WHITE,
            fg=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 11),
        )
        menubar.add_cascade(label="Chế độ", menu=mode_menu)
        mode_menu.add_command(label="Chat", command=lambda: self.show_view("chat"))
        mode_menu.add_command(
            label="Tóm tắt file", command=lambda: self.show_view("summary")
        )
        mode_menu.add_separator()
        mode_menu.add_command(
            label="Cấu hình...", command=lambda: self.show_view("config")
        )

        # File menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=OllamaColors.PURE_WHITE,
            fg=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 11),
        )
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Mở file...", command=self.open_file_and_switch)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.root.quit)

        # Trợ giúp menu
        help_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=OllamaColors.PURE_WHITE,
            fg=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 11),
        )
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="Giới thiệu", command=self.show_about)

    def open_file_and_switch(self):
        """Open file dialog and switch to summary view"""
        self.show_view("summary")
        self.select_file()

    def show_help(self):
        help_text = """HƯỚNG DẪN SỬ DỤNG

1. CHAT (menu Chế độ > Chat)
   - Chat trực tiếp với AI
   - Nhập câu hỏi và nhấn Enter

2. TÓM TẮT FILE (menu Chế độ > Tóm tắt file)
   - Tải file lên và tóm tắt
   - Hỏi đáp về nội dung file

3. CẤU HÌNH (menu Chế độ > Cấu hình)
   - Chọn model AI
   - Đặt độ dài tóm tắt mặc định

Phím tắt:
- Menu Chế độ để chuyển chế độ
- Menu File > Mở file để tải file
"""
        messagebox.showinfo("Hướng dẫn", help_text)

    def show_about(self):
        messagebox.showinfo(
            "Giới thiệu",
            "FITHPUni AI Student v1.0\n\nỨng dụng tóm tắt văn bản sử dụng AI\n© 2026",
        )

    def create_main_container(self):
        """Create main container"""
        self.main_container = tk.Frame(self.root, bg=OllamaColors.PURE_WHITE)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=32, pady=16)

        # Content frame (will be switched between views)
        self.content_frame = tk.Frame(self.main_container, bg=OllamaColors.PURE_WHITE)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Create all views (hidden initially)
        self.chat_view = None
        self.config_view = None
        self.summary_view = None

        # Status bar
        self.create_status_bar()

    def show_view(self, view_name):
        """Switch between views"""
        self.current_view = view_name

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if view_name == "chat":
            self.create_chat_view()
        elif view_name == "config":
            self.create_config_view()
        elif view_name == "summary":
            self.create_summary_view()

    def create_chat_view(self):
        """Create chat view"""
        chat_container = tk.Frame(self.content_frame, bg=OllamaColors.PURE_WHITE)
        chat_container.pack(fill=tk.BOTH, expand=True)

        # Chat history area
        chat_frame = tk.Frame(
            chat_container, bg=OllamaColors.SNOW, relief="solid", bd=1
        )
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        self.chat_scroll = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 13),
            bg=OllamaColors.SNOW,
            fg=OllamaColors.PURE_BLACK,
            relief="flat",
            bd=0,
            padx=20,
            pady=20,
            state="disabled",
        )
        self.chat_scroll.pack(fill=tk.BOTH, expand=True)

        self.chat_scroll.tag_configure(
            "user", justify="right", lmargin1=100, lmargin2=20, rmargin=20
        )
        self.chat_scroll.tag_configure(
            "ai", justify="left", lmargin1=20, lmargin2=20, rmargin=100
        )
        self.chat_scroll.tag_configure(
            "timestamp",
            foreground=OllamaColors.SILVER,
            font=("Segoe UI", 9),
            justify="center",
        )
        self.chat_scroll.tag_configure(
            "system",
            foreground=OllamaColors.STONE,
            font=("Segoe UI", 11, "italic"),
            justify="center",
        )

        # Welcome message
        self.chat_scroll.config(state="normal")
        self.chat_scroll.insert(tk.END, "\n" + "=" * 60 + "\n", "system")
        self.chat_scroll.insert(
            tk.END, "Xin chào, tôi là AI Assistant của FITHPUni!\n", "system"
        )
        self.chat_scroll.insert(
            tk.END, "Tôi sẽ giúp bạn tư vấn về nội dung các môn học.\n", "system"
        )
        self.chat_scroll.insert(tk.END, "=" * 60 + "\n\n", "system")
        self.chat_scroll.config(state="disabled")

        # Input area
        input_frame = tk.Frame(chat_container, bg=OllamaColors.PURE_WHITE)
        input_frame.pack(fill=tk.X, pady=(0, 8))
        input_frame.columnconfigure(0, weight=1)

        self.chat_entry = ttk.Entry(
            input_frame, style="Ollama.TEntry", font=("Segoe UI", 13)
        )
        self.chat_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 12))
        self.chat_entry.bind("<Return>", lambda e: self.send_chat_message())

        self.send_btn = ttk.Button(
            input_frame,
            text="Gửi",
            style="BlackPill.TButton",
            command=self.send_chat_message,
        )
        self.send_btn.grid(row=0, column=1)

        self.chat_model_label = tk.Label(
            input_frame,
            text=f"Model: {self.ai_summarizer.model_name}",
            font=("Segoe UI", 10),
            fg=OllamaColors.SILVER,
            bg=OllamaColors.PURE_WHITE,
        )
        self.chat_model_label.grid(row=0, column=2, padx=(16, 0))

    def create_config_view(self):
        """Create configuration view"""
        config_container = tk.Frame(self.content_frame, bg=OllamaColors.PURE_WHITE)
        config_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        tk.Label(
            config_container,
            text="Cấu hình",
            font=("Segoe UI", 20, "normal"),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(anchor="w", pady=(0, 32))

        # Model section
        model_frame = tk.Frame(
            config_container, bg=OllamaColors.SNOW, relief="solid", bd=1
        )
        model_frame.pack(fill=tk.X, pady=(0, 24), ipady=16, ipadx=16)

        tk.Label(
            model_frame,
            text="Model AI",
            font=("Segoe UI", 12, "bold"),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.SNOW,
        ).pack(anchor="w", pady=(0, 12))

        self.model_var = tk.StringVar(value=self.ai_summarizer.model_name)
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=self.ai_summarizer.get_available_models(),
            state="readonly",
            width=30,
            style="Ollama.TCombobox",
        )
        self.model_combo.pack(anchor="w")

        # Length section
        length_frame = tk.Frame(
            config_container, bg=OllamaColors.SNOW, relief="solid", bd=1
        )
        length_frame.pack(fill=tk.X, pady=(0, 24), ipady=16, ipadx=16)

        tk.Label(
            length_frame,
            text="Độ dài tóm tắt mặc định",
            font=("Segoe UI", 12, "bold"),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.SNOW,
        ).pack(anchor="w", pady=(0, 12))

        length_row = tk.Frame(length_frame, bg=OllamaColors.SNOW)
        length_row.pack(anchor="w")

        self.length_var = tk.IntVar(value=500)
        self.length_slider = ttk.Scale(
            length_row,
            from_=100,
            to=1000,
            variable=self.length_var,
            orient=tk.HORIZONTAL,
            length=300,
            style="Ollama.Horizontal.TScale",
            command=self.update_length_label,
        )
        self.length_slider.pack(side=tk.LEFT)

        self.length_label = tk.Label(
            length_row,
            text="500 từ",
            font=("Segoe UI", 12),
            fg=OllamaColors.STONE,
            bg=OllamaColors.SNOW,
            width=10,
        )
        self.length_label.pack(side=tk.LEFT, padx=(16, 0))

    def create_summary_view(self):
        """Create summary view"""
        summary_container = tk.Frame(self.content_frame, bg=OllamaColors.PURE_WHITE)
        summary_container.pack(fill=tk.BOTH, expand=True)

        # File selection row
        file_row = tk.Frame(summary_container, bg=OllamaColors.PURE_WHITE)
        file_row.pack(fill=tk.X, pady=(0, 16))

        self.select_btn = ttk.Button(
            file_row,
            text="Chọn File",
            style="GrayPill.TButton",
            command=self.select_file,
        )
        self.select_btn.pack(side=tk.LEFT)

        self.file_label = tk.Label(
            file_row,
            text="Chưa chọn file nào",
            font=("system-ui", 13),
            fg=OllamaColors.SILVER,
            bg=OllamaColors.PURE_WHITE,
            anchor="w",
        )
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(16, 0))

        self.word_count_label = tk.Label(
            file_row,
            text="",
            font=("Segoe UI", 12),
            fg=OllamaColors.STONE,
            bg=OllamaColors.PURE_WHITE,
        )
        self.word_count_label.pack(side=tk.LEFT, padx=(16, 0))

        # Configuration row
        config_row = tk.Frame(summary_container, bg=OllamaColors.PURE_WHITE)
        config_row.pack(fill=tk.X, pady=(0, 16))

        tk.Label(
            config_row,
            text="Kiểu",
            font=("Segoe UI", 12),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(side=tk.LEFT)

        ttk.Radiobutton(
            config_row,
            text="Thông thường",
            variable=self.summary_type,
            value="normal",
            style="Ollama.TRadiobutton",
        ).pack(side=tk.LEFT, padx=(12, 8))

        ttk.Radiobutton(
            config_row,
            text="Điểm chính",
            variable=self.summary_type,
            value="bullet",
            style="Ollama.TRadiobutton",
        ).pack(side=tk.LEFT, padx=(0, 24))

        tk.Label(
            config_row,
            text="Dịch",
            font=("Segoe UI", 12),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(side=tk.LEFT)

        self.translate_combo = ttk.Combobox(
            config_row,
            values=["Tiếng Việt", "English"],
            state="readonly",
            width=12,
            style="Ollama.TCombobox",
        )
        self.translate_combo.current(0)
        self.translate_combo.pack(side=tk.LEFT, padx=(8, 24))
        self.translate_combo.bind("<<ComboboxSelected>>", self.on_language_change)

        self.summarize_btn = ttk.Button(
            config_row,
            text="Tóm tắt",
            style="BlackPill.TButton",
            command=self.summarize_file,
            state="disabled",
        )
        self.summarize_btn.pack(side=tk.LEFT, padx=(0, 8))

        # Result area
        result_frame = tk.Frame(
            summary_container, bg=OllamaColors.SNOW, relief="solid", bd=1
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=("system-ui", 13),
            bg=OllamaColors.SNOW,
            relief="flat",
            bd=0,
            padx=16,
            pady=16,
            state="disabled",
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Q&A section
        qa_frame = tk.Frame(summary_container, bg=OllamaColors.PURE_WHITE)
        qa_frame.pack(fill=tk.X, pady=(0, 16))

        tk.Label(
            qa_frame,
            text="Hỏi đáp:",
            font=("Segoe UI", 12),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(side=tk.LEFT)

        self.qa_entry = ttk.Entry(
            qa_frame, style="Ollama.TEntry", font=("Segoe UI", 12)
        )
        self.qa_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(12, 8))
        self.qa_entry.bind("<Return>", lambda e: self.ask_about_file())

        self.ask_btn = ttk.Button(
            qa_frame,
            text="Hỏi",
            style="GrayPill.TButton",
            command=self.ask_about_file,
            state="disabled",
        )
        self.ask_btn.pack(side=tk.LEFT)

        # Action buttons
        tab_actions = tk.Frame(summary_container, bg=OllamaColors.PURE_WHITE)
        tab_actions.pack(fill=tk.X)

        self.copy_btn = ttk.Button(
            tab_actions,
            text="Copy",
            style="WhitePill.TButton",
            command=self.copy_result,
            state="disabled",
        )
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.save_btn = ttk.Button(
            tab_actions,
            text="Save",
            style="WhitePill.TButton",
            command=self.save_result,
            state="disabled",
        )
        self.save_btn.pack(side=tk.LEFT)

    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.main_container, bg=OllamaColors.PURE_WHITE)
        status_frame.pack(fill=tk.X, pady=(8, 0))

        self.progress = ttk.Progressbar(
            status_frame,
            mode="indeterminate",
            length=200,
            style="Ollama.Horizontal.TProgressbar",
        )
        self.progress.pack(side=tk.LEFT, pady=(0, 8))

        self.status_label = tk.Label(
            status_frame,
            text="Sẵn sàng",
            font=("Segoe UI", 11),
            fg=OllamaColors.STONE,
            bg=OllamaColors.PURE_WHITE,
        )
        self.status_label.pack(side=tk.LEFT, padx=(16, 0))

    # ========== CHAT METHODS ==========

    def send_chat_message(self):
        """Send chat message to AI"""
        message = self.chat_entry.get().strip()
        if not message:
            return

        self.chat_entry.delete(0, tk.END)
        self.send_btn.config(state="disabled")

        self.add_chat_message("user", message)

        self.progress.start(10)
        self.status_label.config(text="AI đang trả lời...", fg=OllamaColors.MID_GRAY)

        thread = threading.Thread(
            target=self.get_ai_response, args=(message,), daemon=True
        )
        thread.start()

    def add_chat_message(self, role, content):
        """Add message to chat"""
        timestamp = datetime.now().strftime("%H:%M")

        self.chat_scroll.config(state="normal")

        if role == "user":
            self.chat_scroll.insert(tk.END, f"\n[{timestamp}] Bạn:\n", "timestamp")
            self.chat_scroll.insert(tk.END, f"{content}\n", "user")
        elif role == "ai":
            self.chat_scroll.insert(tk.END, f"\n[{timestamp}] AI:\n", "timestamp")
            self.chat_scroll.insert(tk.END, f"{content}\n", "ai")
        else:
            self.chat_scroll.insert(tk.END, f"\n{content}\n", "system")

        self.chat_scroll.see(tk.END)
        self.chat_scroll.config(state="disabled")

    def get_ai_response(self, user_message):
        """Get AI response"""
        try:
            import ollama

            response = ollama.chat(
                model=self.model_var.get(),
                messages=[{"role": "user", "content": user_message}],
            )

            ai_response = response["message"]["content"].strip()

            def update_ui():
                self.add_chat_message("ai", ai_response)
                self.progress.stop()
                self.send_btn.config(state="normal")
                self.status_label.config(text="Sẵn sàng", fg=OllamaColors.STONE)

            self.root.after(0, update_ui)

        except Exception as e:

            def show_error():
                self.add_chat_message("ai", f"Lỗi: {str(e)}")
                self.progress.stop()
                self.send_btn.config(state="normal")
                self.status_label.config(text="Lỗi!", fg=OllamaColors.STONE)

            self.root.after(0, show_error)

    # ========== CONFIG METHODS ==========

    def update_length_label(self, value):
        length = int(float(value))
        self.length_label.config(text=f"{length} từ")

    # ========== SUMMARY METHODS ==========

    def on_language_change(self, event=None):
        """Handle language change"""
        if not self.current_summary or not self.original_summary:
            return

        selected_lang = self.translate_combo.get()

        if selected_lang == "Tiếng Việt":
            self.display_summary_text(self.original_summary)
            return

        if "English" in self.translation_cache:
            self.display_summary_text(self.translation_cache["English"])
            return

        self.status_label.config(text="Đang dịch...", fg=OllamaColors.MID_GRAY)
        self.progress.start(10)

        thread = threading.Thread(
            target=self.translate_summary_thread,
            args=(self.original_summary,),
            daemon=True,
        )
        thread.start()

    def translate_summary_thread(self, text):
        """Translate text to English"""
        try:
            import ollama

            prompt = f"Translate to English:\n\n{text}"
            response = ollama.chat(
                model=self.model_var.get(),
                messages=[{"role": "user", "content": prompt}],
            )

            translated = response["message"]["content"].strip()
            self.translation_cache["English"] = translated
            self.root.after(0, lambda: self.display_summary_text(translated))

        except Exception as e:
            self.root.after(
                0,
                lambda: self.status_label.config(
                    text=f"Lỗi dịch", fg=OllamaColors.STONE
                ),
            )

    def display_summary_text(self, text):
        """Display summary text"""
        if hasattr(self, "result_text"):
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, text)
            self.result_text.config(state="disabled")
        self.progress.stop()
        self.status_label.config(text="Xong", fg=OllamaColors.STONE)

    def select_file(self):
        """Handle file selection"""
        file_path = filedialog.askopenfilename(
            title="Chọn file để tóm tắt",
            filetypes=[
                ("All Supported", "*.txt *.pdf *.docx"),
                ("Text Files", "*.txt"),
                ("PDF Files", "*.pdf"),
                ("Word Files", "*.docx"),
            ],
        )

        if file_path:
            self.current_file = file_path
            import os

            file_name = os.path.basename(file_path)

            if hasattr(self, "file_label"):
                self.file_label.config(text=file_name, fg=OllamaColors.PURE_BLACK)
            if hasattr(self, "summarize_btn"):
                self.summarize_btn.config(state="normal")

            try:
                self.original_content = self.file_reader.read_file(file_path)
                self.original_word_count = len(self.original_content.split())
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
                self.original_content = ""

            if hasattr(self, "result_text"):
                self.result_text.config(state="normal")
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(
                    1.0,
                    f"File: {file_name}\n({self.original_word_count} từ)\n\nNhấn 'Tóm tắt' để xử lý...",
                )
                self.result_text.config(state="disabled")

    def summarize_file(self):
        """Handle file summarization"""
        if not self.current_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return

        if hasattr(self, "select_btn"):
            self.select_btn.config(state="disabled")
        if hasattr(self, "summarize_btn"):
            self.summarize_btn.config(state="disabled")
        self.stop_event.clear()

        self.progress.start(10)
        self.status_label.config(text="Đang xử lý...", fg=OllamaColors.MID_GRAY)

        if hasattr(self, "result_text"):
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, "Đang tóm tắt...\nVui lòng chờ...\n")
            self.result_text.config(state="disabled")

        thread = threading.Thread(target=self._do_summarize, daemon=True)
        thread.start()

    def _do_summarize(self):
        """Perform summarization"""
        try:
            content = self.file_reader.read_file(self.current_file)

            if not content.strip():
                raise Exception("File trống!")

            self.original_content = content
            self.original_word_count = len(content.split())

            max_length = self.length_var.get() if hasattr(self, "length_var") else 500
            summary_type = (
                self.summary_type.get() if hasattr(self, "summary_type") else "normal"
            )

            if summary_type == "bullet":
                summary = self.ai_summarizer.summarize_with_bullet_points(content)
            else:
                summary = self.ai_summarizer.summarize(content, max_length=max_length)

            self.original_summary = summary
            self.current_summary = summary
            self.translation_cache = {}

            self.display_result(summary)

        except Exception as e:
            self.display_result(f"Lỗi: {str(e)}", success=False)

    def display_result(self, result, success=True):
        """Display summarization result"""

        def update_ui():
            self.progress.stop()

            if hasattr(self, "result_text"):
                self.result_text.config(state="normal")
                self.result_text.delete(1.0, tk.END)

            if success:
                self.summary_word_count = len(result.split())
                info = f"Gốc: {self.original_word_count} từ | Tóm tắt: {self.summary_word_count} từ\n\n"
                if hasattr(self, "result_text"):
                    self.result_text.insert(1.0, f"{info}{result}")
                self.status_label.config(text="Hoàn thành!", fg=OllamaColors.STONE)
                if hasattr(self, "copy_btn"):
                    self.copy_btn.config(state="normal")
                if hasattr(self, "save_btn"):
                    self.save_btn.config(state="normal")
            else:
                if hasattr(self, "result_text"):
                    self.result_text.insert(1.0, result)
                self.status_label.config(text="Lỗi!", fg=OllamaColors.STONE)
                if hasattr(self, "copy_btn"):
                    self.copy_btn.config(state="disabled")
                if hasattr(self, "save_btn"):
                    self.save_btn.config(state="disabled")

            if hasattr(self, "result_text"):
                self.result_text.config(state="disabled")
            if hasattr(self, "select_btn"):
                self.select_btn.config(state="normal")
            if hasattr(self, "summarize_btn"):
                self.summarize_btn.config(state="normal")
            if hasattr(self, "ask_btn") and success:
                self.ask_btn.config(state="normal")

        self.root.after(0, update_ui)

    def ask_about_file(self):
        """Ask AI about the file content"""
        question = self.qa_entry.get().strip()
        if not question:
            return

        if not self.original_content:
            messagebox.showwarning("Cảnh báo", "Chưa có nội dung file!")
            return

        self.qa_entry.delete(0, tk.END)
        if hasattr(self, "ask_btn"):
            self.ask_btn.config(state="disabled")

        self.progress.start(10)
        self.status_label.config(text="Đang trả lời...", fg=OllamaColors.MID_GRAY)

        if hasattr(self, "result_text"):
            self.result_text.config(state="normal")
            self.result_text.insert(tk.END, "\n\nĐang hỏi...\n")
            self.result_text.see(tk.END)
            self.result_text.config(state="disabled")

        thread = threading.Thread(target=self._do_ask, args=(question,), daemon=True)
        thread.start()

    def _do_ask(self, question):
        """Get answer about file content"""
        try:
            prompt = f"""Bạn là trợ lý AI đọc và trả lời câu hỏi dựa trên văn bản được cung cấp.

QUY TẮC:
1. Đọc KỸ văn bản bên dưới
2. Trả lời câu hỏi dựa trên THÔNG TIN TRONG VĂN BẢN
3. Nếu câu hỏi liên quan đến chủ đề/cụm từ có trong văn bản → TRẢ LỜI bằng thông tin đó
4. Nếu câu hỏi hỏi về khái niệm (ví dụ "railway là gì") mà văn bản đề cập → dùng THÔNG TIN TRONG VĂN BẢN để giải thích
5. Trả lời NGẮN GỌN, ĐI THẲNG VÀO VẤN ĐỀ
6. Dùng tiếng Việt

VĂN BẢN:
{self.original_content}

CÂU HỎI: {question}

TRẢ LỜI:"""

            import ollama

            response = ollama.chat(
                model=self.model_var.get(),
                messages=[{"role": "user", "content": prompt}],
            )

            answer = response["message"]["content"].strip()

            def update_ui():
                self.progress.stop()
                if hasattr(self, "result_text"):
                    self.result_text.config(state="normal")
                    self.result_text.insert(
                        tk.END, f"\n\nCâu hỏi: {question}\n\nĐáp: {answer}\n"
                    )
                    self.result_text.see(tk.END)
                    self.result_text.config(state="disabled")
                if hasattr(self, "ask_btn"):
                    self.ask_btn.config(state="normal")
                self.status_label.config(text="Sẵn sàng", fg=OllamaColors.STONE)

            self.root.after(0, update_ui)

        except Exception as e:

            def show_error():
                self.progress.stop()
                if hasattr(self, "result_text"):
                    self.result_text.config(state="normal")
                    self.result_text.insert(tk.END, f"\n\nLỗi: {str(e)}\n")
                    self.result_text.config(state="disabled")
                if hasattr(self, "ask_btn"):
                    self.ask_btn.config(state="normal")
                self.status_label.config(text="Lỗi!", fg=OllamaColors.STONE)

            self.root.after(0, show_error)

    def copy_result(self):
        """Copy result to clipboard"""
        if self.current_summary:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_summary)
            self.root.update()
            messagebox.showinfo("Thành công", "Đã copy!")

    def save_result(self):
        """Save result to file"""
        if not self.current_summary:
            messagebox.showwarning("Cảnh báo", "Không có kết quả!")
            return

        import os

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"summary_{timestamp}.txt"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Lưu kết quả",
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_summary)
                messagebox.showinfo("Thành công", f"Đã lưu!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")


def main():
    root = tk.Tk()
    app = AISummaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
