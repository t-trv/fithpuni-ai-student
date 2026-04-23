"""
AI Summary Application - Ollama-Inspired Design
Ứng dụng tóm tắt văn bản sử dụng AI
Sử dụng Ollama local models để tóm tắt file .txt, .pdf, .docx
Design inspired by Ollama - Radical minimalism, pure grayscale
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import tkinter.font as tkfont
import threading
from datetime import datetime
from ..logic.file_reader import FileReader
from ..logic.ai_summarizer import AISummarizer


# Ollama Design System Colors
class OllamaColors:
    # Primary
    PURE_BLACK = "#000000"
    NEAR_BLACK = "#262626"
    DARKEST_SURFACE = "#090909"

    # Surface & Background
    PURE_WHITE = "#ffffff"
    SNOW = "#fafafa"
    LIGHT_GRAY = "#e5e5e5"

    # Neutrals & Text
    STONE = "#737373"
    MID_GRAY = "#525252"
    SILVER = "#a3a3a3"
    BUTTON_TEXT_DARK = "#404040"

    # Focus
    RING_BLUE = "#3b82f6"
    BORDER_LIGHT = "#d4d4d4"


# Font definitions - using standard Windows fonts with fallback
TITLE_FONT = ("Segoe UI", 24, "normal")
SUBTITLE_FONT = ("Segoe UI", 14, "normal")
SECTION_FONT = ("Segoe UI", 12, "normal")
BODY_FONT = ("Segoe UI", 13, "normal")
SMALL_FONT = ("Segoe UI", 11, "normal")
TINY_FONT = ("Segoe UI", 10, "normal")


class OllamaStyle:
    """Custom ttk styles following Ollama design system"""

    @staticmethod
    def configure_styles(root):
        """Configure all ttk styles for Ollama-inspired design"""
        style = ttk.Style(root)

        # Use a clean theme as base
        available_themes = style.theme_names()
        if "clam" in available_themes:
            style.theme_use("clam")
        elif "alt" in available_themes:
            style.theme_use("alt")

        # ==== Frame Styles ====
        style.configure("Ollama.TFrame", background=OllamaColors.PURE_WHITE)

        style.configure(
            "OllamaContainer.TFrame",
            background=OllamaColors.SNOW,
            relief="solid",
            borderwidth=1,
            bordercolor=OllamaColors.LIGHT_GRAY,
        )

        # ==== Label Styles ====
        style.configure(
            "Ollama.TLabel",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 14),
        )

        style.configure(
            "OllamaTitle.TLabel",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 24, "normal"),
            anchor="center",
        )

        style.configure(
            "OllamaSection.TLabel",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 12, "normal"),
        )

        style.configure(
            "OllamaMuted.TLabel",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.STONE,
            font=("Segoe UI", 12),
        )

        style.configure(
            "OllamaSmall.TLabel",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.SILVER,
            font=("Segoe UI", 10),
        )

        # ==== Button Styles - Pill-shaped (9999px) ====

        # Primary Gray Pill Button
        style.configure(
            "GrayPill.TButton",
            background=OllamaColors.LIGHT_GRAY,
            foreground=OllamaColors.NEAR_BLACK,
            font=("Segoe UI", 13, "normal"),
            padding=(24, 10),
            borderwidth=1,
            relief="solid",
            bordercolor=OllamaColors.LIGHT_GRAY,
        )
        style.map(
            "GrayPill.TButton",
            background=[
                ("active", OllamaColors.MID_GRAY),
                ("disabled", OllamaColors.SNOW),
            ],
            foreground=[("disabled", OllamaColors.SILVER)],
        )

        # Secondary White Pill Button
        style.configure(
            "WhitePill.TButton",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.BUTTON_TEXT_DARK,
            font=("Segoe UI", 13, "normal"),
            padding=(24, 10),
            borderwidth=1,
            relief="solid",
            bordercolor=OllamaColors.BORDER_LIGHT,
        )
        style.map(
            "WhitePill.TButton",
            background=[
                ("active", OllamaColors.LIGHT_GRAY),
                ("disabled", OllamaColors.SNOW),
            ],
            foreground=[("disabled", OllamaColors.SILVER)],
        )

        # CTA Black Pill Button
        style.configure(
            "BlackPill.TButton",
            background=OllamaColors.PURE_BLACK,
            foreground=OllamaColors.PURE_WHITE,
            font=("Segoe UI", 13, "normal"),
            padding=(24, 10),
            borderwidth=0,
            relief="flat",
        )
        style.map(
            "BlackPill.TButton",
            background=[
                ("active", OllamaColors.NEAR_BLACK),
                ("disabled", OllamaColors.MID_GRAY),
            ],
        )

        # Stop Button - Distinct style
        style.configure(
            "StopPill.TButton",
            background=OllamaColors.PURE_BLACK,
            foreground=OllamaColors.PURE_WHITE,
            font=("Segoe UI", 13, "normal"),
            padding=(24, 10),
            borderwidth=0,
            relief="flat",
        )
        style.map(
            "StopPill.TButton",
            background=[
                ("active", OllamaColors.NEAR_BLACK),
                ("disabled", OllamaColors.MID_GRAY),
            ],
        )

        # ==== LabelFrame Styles - 12px radius containers ====
        style.configure(
            "Ollama.TLabelframe",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 12, "normal"),
            labelmargins=(12, 8),
            borderwidth=1,
            relief="solid",
            bordercolor=OllamaColors.LIGHT_GRAY,
        )
        style.configure(
            "Ollama.TLabelframe.Label",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 11, "normal"),
        )

        # ==== Notebook Styles ====
        style.configure(
            "Ollama.TNotebook",
            background=OllamaColors.PURE_WHITE,
            borderwidth=0,
            tabmargins=0,
        )
        style.configure(
            "Ollama.TNotebook.Tab",
            background=OllamaColors.SNOW,
            foreground=OllamaColors.STONE,
            font=("Segoe UI", 12),
            padding=(16, 8),
            borderwidth=1,
            relief="solid",
            bordercolor=OllamaColors.LIGHT_GRAY,
        )
        style.map(
            "Ollama.TNotebook.Tab",
            background=[
                ("selected", OllamaColors.PURE_WHITE),
                ("active", OllamaColors.LIGHT_GRAY),
            ],
            foreground=[
                ("selected", OllamaColors.PURE_BLACK),
                ("active", OllamaColors.NEAR_BLACK),
            ],
        )

        # ==== Entry Styles - Pill-shaped ====
        style.configure(
            "Ollama.TEntry",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            fieldbackground=OllamaColors.PURE_WHITE,
            borderwidth=1,
            relief="solid",
            bordercolor=OllamaColors.LIGHT_GRAY,
            insertcolor=OllamaColors.PURE_BLACK,
            padding=(12, 8),
            font=("Segoe UI", 12),
        )
        style.map(
            "Ollama.TEntry",
            fieldbackground=[("focus", OllamaColors.PURE_WHITE)],
            bordercolor=[("focus", OllamaColors.NEAR_BLACK)],
        )

        # ==== Combobox Styles ====
        style.configure(
            "Ollama.TCombobox",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            fieldbackground=OllamaColors.PURE_WHITE,
            borderwidth=1,
            relief="solid",
            bordercolor=OllamaColors.LIGHT_GRAY,
            padding=(8, 6),
            font=("Segoe UI", 12),
        )
        style.map(
            "Ollama.TCombobox",
            fieldbackground=[
                ("readonly", OllamaColors.PURE_WHITE),
                ("focus", OllamaColors.PURE_WHITE),
            ],
            bordercolor=[("focus", OllamaColors.NEAR_BLACK)],
            arrowcolor=[("active", OllamaColors.PURE_BLACK)],
        )

        # ==== Radiobutton Styles ====
        style.configure(
            "Ollama.TRadiobutton",
            background=OllamaColors.PURE_WHITE,
            foreground=OllamaColors.PURE_BLACK,
            font=("Segoe UI", 12),
            padding=(8, 4),
            indicatorbackground=OllamaColors.PURE_WHITE,
            indicatorforeground=OllamaColors.PURE_BLACK,
            indicatormargin=(0, 0, 8, 0),
        )
        style.map(
            "Ollama.TRadiobutton",
            background=[("selected", OllamaColors.PURE_WHITE)],
            foreground=[
                ("selected", OllamaColors.PURE_BLACK),
                ("active", OllamaColors.NEAR_BLACK),
            ],
            indicatorcolor=[("selected", OllamaColors.PURE_BLACK)],
        )

        # ==== Scale/Slider Styles ====
        style.configure(
            "Ollama.Horizontal.TScale",
            background=OllamaColors.PURE_WHITE,
            troughcolor=OllamaColors.LIGHT_GRAY,
            slidercolor=OllamaColors.PURE_BLACK,
            borderwidth=0,
            thickness=4,
        )

        # ==== Progressbar Styles ====
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
        """Initialize application interface"""
        self.root = root
        self.root.title("FITHPUni AI Student")
        self.root.geometry("900x800")
        self.root.configure(bg=OllamaColors.PURE_WHITE)
        self.root.minsize(800, 700)

        # Configure styles
        self.style = OllamaStyle.configure_styles(self.root)

        # Initialize components
        self.file_reader = FileReader()
        self.ai_summarizer = AISummarizer()
        self.current_file = None
        self.current_summary = ""
        self.original_content = ""
        self.original_word_count = 0
        self.summary_word_count = 0
        self.summary_thread = None
        self.stop_event = threading.Event()

        # Translation cache
        self.translation_cache = {}
        self.original_summary = None
        self.current_summary_language = "original"

        # Create interface
        self.create_widgets()

    def _create_pill_entry(self, parent, **kwargs):
        """Create a pill-shaped entry widget"""
        entry = ttk.Entry(parent, style="Ollama.TEntry", **kwargs)
        # Apply rounded corners via grid sticky
        return entry

    def create_widgets(self):
        """Create all UI widgets following Ollama design"""

        # Main container - pure white background
        main_container = tk.Frame(self.root, bg=OllamaColors.PURE_WHITE)
        main_container.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)

        # ==== HEADER SECTION ====
        header_frame = tk.Frame(main_container, bg=OllamaColors.PURE_WHITE)
        header_frame.pack(fill=tk.X, pady=(0, 24))

        # ==== FILE SELECTION SECTION ====
        file_section = tk.Frame(main_container, bg=OllamaColors.PURE_WHITE)
        file_section.pack(fill=tk.X, pady=(0, 16))

        # File selection row
        file_row = tk.Frame(file_section, bg=OllamaColors.PURE_WHITE)
        file_row.pack(fill=tk.X)

        # Select file button - Gray Pill
        self.select_btn = ttk.Button(
            file_row,
            text="Chọn File",
            style="GrayPill.TButton",
            command=self.select_file,
        )
        self.select_btn.pack(side=tk.LEFT)

        # File name label
        self.file_label = tk.Label(
            file_row,
            text="Chưa chọn file nào",
            font=("system-ui", 13),
            fg=OllamaColors.SILVER,
            bg=OllamaColors.PURE_WHITE,
            anchor="w",
        )
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(16, 0))

        # Word count label
        self.word_count_label = tk.Label(
            file_row,
            text="",
            font=("Segoe UI", 12),
            fg=OllamaColors.STONE,
            bg=OllamaColors.PURE_WHITE,
        )
        self.word_count_label.pack(side=tk.LEFT, padx=(16, 0))

        # ==== CONFIGURATION SECTION ====
        config_container = tk.Frame(main_container, bg=OllamaColors.PURE_WHITE)
        config_container.pack(fill=tk.X, pady=(0, 16))

        # Configuration row 1: Model + Type
        config_row1 = tk.Frame(config_container, bg=OllamaColors.PURE_WHITE)
        config_row1.pack(fill=tk.X, pady=(0, 12))

        # Model selection
        tk.Label(
            config_row1,
            text="Model",
            font=("Segoe UI", 12, "normal"),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(side=tk.LEFT)

        self.model_var = tk.StringVar(value="llama3.2:1b")
        self.model_combo = ttk.Combobox(
            config_row1,
            textvariable=self.model_var,
            values=self.ai_summarizer.get_available_models(),
            state="readonly",
            width=18,
            style="Ollama.TCombobox",
        )
        self.model_combo.pack(side=tk.LEFT, padx=(12, 24))
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_change)

        # Summary type - Radiobuttons
        tk.Label(
            config_row1,
            text="Kiểu",
            font=("Segoe UI", 12, "normal"),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(side=tk.LEFT)

        self.summary_type = tk.StringVar(value="normal")

        rb_normal = ttk.Radiobutton(
            config_row1,
            text="Thông thường",
            variable=self.summary_type,
            value="normal",
            style="Ollama.TRadiobutton",
        )
        rb_normal.pack(side=tk.LEFT, padx=(12, 8))

        rb_bullet = ttk.Radiobutton(
            config_row1,
            text="Điểm chính",
            variable=self.summary_type,
            value="bullet",
            style="Ollama.TRadiobutton",
        )
        rb_bullet.pack(side=tk.LEFT)

        # Configuration row 2: Length slider
        config_row2 = tk.Frame(config_container, bg=OllamaColors.PURE_WHITE)
        config_row2.pack(fill=tk.X, pady=(0, 12))

        tk.Label(
            config_row2,
            text="Độ dài",
            font=("Segoe UI", 12, "normal"),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(side=tk.LEFT)

        self.length_var = tk.IntVar(value=500)
        self.length_slider = ttk.Scale(
            config_row2,
            from_=100,
            to=1000,
            variable=self.length_var,
            orient=tk.HORIZONTAL,
            length=200,
            style="Ollama.Horizontal.TScale",
            command=self.update_length_label,
        )
        self.length_slider.pack(side=tk.LEFT, padx=(12, 8))

        self.length_label = tk.Label(
            config_row2,
            text="500 tu",
            font=("Segoe UI", 12),
            fg=OllamaColors.STONE,
            bg=OllamaColors.PURE_WHITE,
            width=8,
        )
        self.length_label.pack(side=tk.LEFT)

        # Configuration row 3: Translation + Action buttons
        config_row3 = tk.Frame(config_container, bg=OllamaColors.PURE_WHITE)
        config_row3.pack(fill=tk.X)

        tk.Label(
            config_row3,
            text="Dịch sang",
            font=("Segoe UI", 12, "normal"),
            fg=OllamaColors.PURE_BLACK,
            bg=OllamaColors.PURE_WHITE,
        ).pack(side=tk.LEFT)

        self.translate_var = tk.StringVar(value="none")
        translate_options = ["Tiếng Việt", "English"]
        translate_values = ["none", "en"]
        self.translate_combo = ttk.Combobox(
            config_row3,
            values=translate_options,
            state="readonly",
            width=15,
            style="Ollama.TCombobox",
        )
        self.translate_combo.current(0)
        self.translate_combo.pack(side=tk.LEFT, padx=(12, 24))

        def on_translate_selected(e):
            idx = self.translate_combo.current()
            self.translate_var.set(translate_values[idx])
            self.on_language_change()

        self.translate_combo.bind("<<ComboboxSelected>>", on_translate_selected)

        # Action buttons
        self.summarize_btn = ttk.Button(
            config_row3,
            text="Tóm tắt",
            style="BlackPill.TButton",
            command=self.summarize_file,
            state="disabled",
        )
        self.summarize_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.stop_btn = ttk.Button(
            config_row3,
            text="STOP",
            style="StopPill.TButton",
            command=self.stop_summarization,
            state="disabled",
        )
        self.stop_btn.pack(side=tk.LEFT)

        # ==== CONTENT AREA - Tabs ====
        tabs_container = tk.Frame(main_container, bg=OllamaColors.PURE_WHITE)
        tabs_container.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        # Notebook with Ollama styling
        self.notebook = ttk.Notebook(tabs_container, style="Ollama.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Summary
        summary_tab = tk.Frame(self.notebook, bg=OllamaColors.PURE_WHITE)
        self.notebook.add(summary_tab, text="Tóm tắt")

        summary_tab.columnconfigure(0, weight=1)
        summary_tab.rowconfigure(0, weight=1)

        # Result text area - clean border, no shadow
        result_frame = tk.Frame(summary_tab, bg=OllamaColors.SNOW, relief="solid", bd=1)
        result_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0, pady=(0, 12)
        )

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=("system-ui", 13),
            bg=OllamaColors.SNOW,
            fg=OllamaColors.PURE_BLACK,
            insertbackground=OllamaColors.PURE_BLACK,
            relief="flat",
            bd=0,
            padx=16,
            pady=16,
            state="disabled",
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Tab action buttons
        tab_actions = tk.Frame(summary_tab, bg=OllamaColors.PURE_WHITE)
        tab_actions.grid(row=1, column=0, sticky=tk.W)

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

        # Tab 2: Q&A
        qa_tab = tk.Frame(self.notebook, bg=OllamaColors.PURE_WHITE)
        self.qa_tab = qa_tab
        self.notebook.add(qa_tab, text="Hỏi đáp", state="disabled")

        qa_tab.columnconfigure(0, weight=1)
        qa_tab.rowconfigure(0, weight=1)

        # Q&A text area
        qa_frame = tk.Frame(qa_tab, bg=OllamaColors.SNOW, relief="solid", bd=1)
        qa_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0, pady=(0, 12)
        )

        self.qa_text = scrolledtext.ScrolledText(
            qa_frame,
            wrap=tk.WORD,
            font=("system-ui", 13),
            bg=OllamaColors.SNOW,
            fg=OllamaColors.PURE_BLACK,
            insertbackground=OllamaColors.PURE_BLACK,
            relief="flat",
            bd=0,
            padx=16,
            pady=16,
            state="disabled",
        )
        self.qa_text.pack(fill=tk.BOTH, expand=True)

        # Q&A input row
        qa_input_row = tk.Frame(qa_tab, bg=OllamaColors.PURE_WHITE)
        qa_input_row.grid(row=1, column=0, sticky=(tk.W, tk.E))
        qa_input_row.columnconfigure(0, weight=1)

        self.question_entry = ttk.Entry(
            qa_input_row, style="Ollama.TEntry", font=("system-ui", 13)
        )
        self.question_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 12))

        def on_enter(event):
            self.ask_question()
            return "break"

        self.question_entry.bind("<Return>", on_enter)

        self.ask_btn = ttk.Button(
            qa_input_row,
            text="Hỏi",
            style="GrayPill.TButton",
            command=self.ask_question,
        )
        self.ask_btn.grid(row=0, column=1)

        # ==== FOOTER SECTION ====
        footer_frame = tk.Frame(main_container, bg=OllamaColors.PURE_WHITE)
        footer_frame.pack(fill=tk.X, pady=(8, 0))

        # Progress bar
        self.progress = ttk.Progressbar(
            footer_frame,
            mode="indeterminate",
            length=300,
            style="Ollama.Horizontal.TProgressbar",
        )
        self.progress.pack(pady=(0, 12))

        # Status label - minimal
        self.status_label = tk.Label(
            footer_frame,
            text="Sẵn sàng",
            font=("Segoe UI", 12),
            fg=OllamaColors.STONE,
            bg=OllamaColors.PURE_WHITE,
            anchor="center",
        )
        self.status_label.pack()

    def update_length_label(self, value):
        """Update length display label"""
        length = int(float(value))
        self.length_label.config(text=f"{length} từ")

    def on_language_change(self):
        """Auto-translate when language selection changes"""
        if not self.current_summary or not self.original_summary:
            return

        selected_lang = self.translate_combo.get()

        if selected_lang == "Tiếng Việt":
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            word_info = f"Gốc: {self.original_word_count} từ | Tóm tắt: {len(self.original_summary.split())} từ\n\n"
            self.result_text.insert(
                1.0, f"KẾT QUẢ (Tiếng Việt):\n\n{word_info}{self.original_summary}"
            )
            self.current_summary = self.original_summary
            self.current_summary_language = "vi"
            self.result_text.config(state="disabled")
            self.status_label.config(
                text="Hiển thị bản Tiếng Việt", fg=OllamaColors.STONE
            )
            return

        if "English" in self.translation_cache:
            translated = self.translation_cache["English"]
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            word_info = f"Original: {self.original_word_count} words | Summary: {len(translated.split())} words\n\n"
            self.result_text.insert(
                1.0, f"RESULT (English):\n\n{word_info}{translated}"
            )
            self.current_summary = translated
            self.current_summary_language = "en"
            self.result_text.config(state="disabled")
            self.status_label.config(
                text="Showing English version (from cache)", fg=OllamaColors.STONE
            )
            return

        self.status_label.config(
            text="Đang dịch sang English...", fg=OllamaColors.MID_GRAY
        )
        self.progress.start(10)

        thread = threading.Thread(
            target=self.translate_summary_thread,
            args=(self.original_summary,),
            daemon=True,
        )
        thread.start()

    def translate_summary_thread(self, text):
        """Thread for translating text to English"""
        try:
            prompt = f"""Translate the following Vietnamese text to English. 
Keep the formatting and structure. Only provide the English translation, no explanations.

Vietnamese text:
{text}

English translation:"""

            import ollama

            response = ollama.chat(
                model=self.model_var.get(),
                messages=[{"role": "user", "content": prompt}],
            )

            translated = response["message"]["content"].strip()
            self.translation_cache["English"] = translated
            self.root.after(0, self.display_translation, translated)

        except Exception as e:
            self.root.after(0, self.show_translation_error, str(e))

    def display_translation(self, translated_text):
        """Display English translation"""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        word_info = f"Original: {self.original_word_count} words | Summary: {len(translated_text.split())} words\n\n"
        self.result_text.insert(
            1.0, f"RESULT (English):\n\n{word_info}{translated_text}"
        )
        self.current_summary = translated_text
        self.current_summary_language = "en"
        self.result_text.config(state="disabled")

        words = len(translated_text.split())
        self.status_label.config(
            text=f"Đã dịch sang English ({words} từ)", fg=OllamaColors.STONE
        )
        self.progress.stop()

    def show_translation_error(self, error):
        """Show translation error"""
        self.status_label.config(text=f"Lỗi dịch: {error}", fg=OllamaColors.STONE)
        self.progress.stop()
        messagebox.showerror("Lỗi dịch", f"Không thể dịch: {error}")

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
            self.file_label.config(text=file_name, fg=OllamaColors.PURE_BLACK)
            self.summarize_btn.config(state="normal")

            self.notebook.tab(1, state="normal")
            try:
                self.original_content = self.file_reader.read_file(file_path)
                self.original_word_count = len(self.original_content.split())
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
                self.original_content = ""

            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(
                1.0, f"File đã chọn: {file_name}\n\nNhấn nút 'Tóm tắt' để bắt đầu..."
            )
            self.result_text.config(state="disabled")

    def on_model_change(self, event):
        """Handle model change"""
        selected_model = self.model_var.get()
        self.ai_summarizer.set_model(selected_model)

    def summarize_file(self):
        """Handle file summarization"""
        if not self.current_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return

        self.select_btn.config(state="disabled")
        self.summarize_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.stop_event.clear()

        self.progress.start(10)
        self.status_label.config(text="Đang xử lý...", fg=OllamaColors.MID_GRAY)

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, "Đang đọc file và tóm tắt...\nVui lòng chờ...\n\n")
        self.result_text.config(state="disabled")

        self.summary_thread = threading.Thread(target=self._do_summarize)
        self.summary_thread.daemon = True
        self.summary_thread.start()

    def _do_summarize(self):
        """Perform summarization"""
        try:
            self.update_status("Đang đọc file...")
            content = self.file_reader.read_file(self.current_file)

            if not content.strip():
                raise Exception("File trống!")

            self.original_content = content
            self.original_word_count = len(content.split())

            self.update_status(f"Đang tóm tắt với model {self.model_var.get()}...")

            if self.stop_event.is_set():
                self.display_result("Đã dừng!", success=False)
                return

            max_length = self.length_var.get()

            if self.summary_type.get() == "bullet":
                summary = self.ai_summarizer.summarize_with_bullet_points(content)
            else:
                summary = self.ai_summarizer.summarize(content, max_length=max_length)

            if self.translate_var.get() != "none":
                self.update_status(f"Đang dịch sang {self.translate_combo.get()}...")
                summary = self.translate_text(summary, self.translate_var.get())

            self.display_result(summary, success=True)
        except Exception as e:
            self.display_result(f"Lỗi: {str(e)}", success=False)

    def translate_text(self, text, target_lang):
        """Translate text to target language"""
        lang_names = {"en": "English", "vi": "Vietnamese (Tiếng Việt)"}

        prompt = f"""Translate the following text to {lang_names.get(target_lang, target_lang)}.
Only return the translated text, no explanations.

Text to translate:
{text}

Translation:"""

        try:
            import ollama

            response = ollama.chat(
                model=self.model_var.get(),
                messages=[{"role": "user", "content": prompt}],
            )
            return response["message"]["content"].strip()
        except Exception as e:
            return f"[Lỗi dịch: {str(e)}]\n\n{text}"

    def ask_question(self):
        """Handle Q&A about the document"""
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập câu hỏi!")
            return

        if not self.original_content:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return

        self.question_entry.delete(0, tk.END)
        self.ask_btn.config(state="disabled")
        self.question_entry.config(state="disabled")

        self.progress.start(10)
        self.status_label.config(text="Đang suy nghĩ...", fg=OllamaColors.MID_GRAY)

        self.qa_text.config(state="normal")
        self.qa_text.insert(tk.END, f"\n{'='*50}\n")
        self.qa_text.insert(tk.END, f"Câu hỏi: {question}\n\n")
        self.qa_text.insert(tk.END, "Đang suy nghĩ... Vui lòng chờ...\n")
        self.qa_text.see(tk.END)
        self.qa_text.config(state="disabled")

        def do_qa():
            try:
                prompt = f"""Based on the following text, answer the question.

Text:
{self.original_content[:3000]}

Question: {question}

Answer:"""

                import ollama

                response = ollama.chat(
                    model=self.model_var.get(),
                    messages=[{"role": "user", "content": prompt}],
                )
                answer = response["message"]["content"].strip()

                def update_qa():
                    self.qa_text.config(state="normal")
                    content = self.qa_text.get(1.0, tk.END)
                    if "Đang suy nghĩ" in content:
                        self.qa_text.delete("end-2l", "end-1l")
                    self.qa_text.insert(tk.END, f"Trả lời: {answer}\n")
                    self.qa_text.see(tk.END)
                    self.qa_text.config(state="disabled")
                    self.question_entry.config(state="normal")
                    self.question_entry.focus()
                    self.ask_btn.config(state="normal")
                    self.progress.stop()
                    self.status_label.config(
                        text="Hoàn thành Q&A!", fg=OllamaColors.STONE
                    )

                self.root.after(0, update_qa)

            except Exception as e:

                def show_error():
                    self.qa_text.config(state="normal")
                    content = self.qa_text.get(1.0, tk.END)
                    if "Đang suy nghĩ" in content:
                        self.qa_text.delete("end-2l", "end-1l")
                    self.qa_text.insert(tk.END, f"Lỗi: {str(e)}\n")
                    self.qa_text.see(tk.END)
                    self.qa_text.config(state="disabled")
                    self.question_entry.config(state="normal")
                    self.ask_btn.config(state="normal")
                    self.progress.stop()
                    self.status_label.config(text="Loi!", fg=OllamaColors.STONE)

                self.root.after(0, show_error)

        qa_thread = threading.Thread(target=do_qa)
        qa_thread.daemon = True
        qa_thread.start()

    def stop_summarization(self):
        """Stop AI processing"""
        self.stop_event.set()
        self.progress.stop()
        self.status_label.config(text="Đã dừng!", fg=OllamaColors.STONE)
        self.stop_btn.config(state="disabled")
        self.select_btn.config(state="normal")
        self.summarize_btn.config(state="normal")

    def update_status(self, message):
        """Update status message"""
        self.root.after(
            0, lambda: self.status_label.config(text=message, fg=OllamaColors.MID_GRAY)
        )
        self.root.after(
            0,
            lambda: self.result_text.config(state="normal")
            or self.result_text.insert(tk.END, f"{message}\n")
            or self.result_text.config(state="disabled"),
        )

    def copy_result(self):
        """Copy result to clipboard"""
        if self.current_summary:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_summary)
            self.root.update()
            messagebox.showinfo("Thành công", "Đã copy vào clipboard!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có kết quả!")

    def save_result(self):
        """Save result to file"""
        if not self.current_summary:
            messagebox.showwarning("Cảnh báo", "Không có kết quả để lưu!")
            return

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
                messagebox.showinfo("Thành công", f"Đã lưu vào:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")

    def display_result(self, result, success=True):
        """Display summarization result"""

        def update_ui():
            self.progress.stop()
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)

            if success:
                self.summary_word_count = len(result.split())
                word_info = f"Gốc: {self.original_word_count} từ | Tóm tắt: {self.summary_word_count} từ\n\n"

                self.result_text.insert(1.0, f"KẾT QUẢ:\n\n{word_info}{result}")
                self.status_label.config(text="Hoàn thành!", fg=OllamaColors.STONE)

                self.original_summary = result
                self.current_summary = result
                self.current_summary_language = "vi"
                self.translation_cache = {}

                self.translate_combo.set("Tiếng Việt")

                self.copy_btn.config(state="normal")
                self.save_btn.config(state="normal")
                self.ask_btn.config(state="normal")

                self.word_count_label.config(
                    text=f"{self.original_word_count} từ | {self.summary_word_count} từ"
                )
            else:
                self.result_text.insert(1.0, f"Lỗi: {result}")
                self.status_label.config(text="Loi!", fg=OllamaColors.STONE)
                self.current_summary = ""
                self.copy_btn.config(state="disabled")
                self.save_btn.config(state="disabled")

            self.result_text.config(state="disabled")
            self.select_btn.config(state="normal")
            self.summarize_btn.config(state="normal")

        self.root.after(0, update_ui)


def main():
    """Main function"""
    root = tk.Tk()
    app = AISummaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
