"""
AI Summary Application - Ứng dụng tóm tắt văn bản sử dụng AI
Sử dụng Ollama local models để tóm tắt file .txt, .pdf, .docx
Version 2 với các tính năng mở rộng
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from datetime import datetime
from ..logic.file_reader import FileReader
from ..logic.ai_summarizer import AISummarizer


class AISummaryApp:
    """Class chính cho ứng dụng AI Summary"""

    def __init__(self, root):
        """Khởi tạo giao diện ứng dụng"""
        self.root = root
        self.root.title("AI Summary - Advanced AI Text Summarizer")
        self.root.geometry("1000x800")

        # Khởi tạo components
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
        self.translation_cache = {}  # {language: translated_text}
        self.original_summary = None  # Lưu bản tóm tắt gốc (chưa dịch)
        self.current_summary_language = "original"  # Ngôn ngữ hiện tại

        # Tạo giao diện
        self.create_widgets()

    def create_widgets(self):
        """Tạo các widgets cho giao diện"""

        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="🤖 AI Document Assistant",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Frame cho file selection
        file_frame = ttk.LabelFrame(main_frame, text="Chọn File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3,
                        sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(1, weight=1)

        self.select_btn = ttk.Button(
            file_frame, text="📁 Chọn File", command=self.select_file)
        self.select_btn.grid(row=0, column=0, padx=5)

        self.file_label = ttk.Label(
            file_frame, text="Chưa chọn file nào", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # Word count label
        self.word_count_label = ttk.Label(
            file_frame, text="", foreground="blue")
        self.word_count_label.grid(row=0, column=2, padx=5)

        # Frame cho model selection và options
        config_frame = ttk.LabelFrame(
            main_frame, text="Cấu hình AI", padding="10")
        config_frame.grid(row=2, column=0, columnspan=3,
                          sticky=(tk.W, tk.E), pady=5)

        # Row 1: Model, Summary Type, Buttons
        ttk.Label(config_frame, text="Model:").grid(
            row=0, column=0, padx=5, sticky=tk.W)
        self.model_var = tk.StringVar(value="llama3.2:1b")
        self.model_combo = ttk.Combobox(
            config_frame, textvariable=self.model_var,
            values=self.ai_summarizer.get_available_models(),
            state="readonly", width=15
        )
        self.model_combo.grid(row=0, column=1, padx=5, sticky=tk.W)

        ttk.Label(config_frame, text="Kiểu:").grid(
            row=0, column=2, padx=5, sticky=tk.W)
        self.summary_type = tk.StringVar(value="normal")
        ttk.Radiobutton(config_frame, text="Thông Thường", variable=self.summary_type,
                        value="normal").grid(row=0, column=3, padx=2)
        ttk.Radiobutton(config_frame, text="Điểm Chính",
                        variable=self.summary_type, value="bullet").grid(row=0, column=4, padx=2)

        self.summarize_btn = ttk.Button(
            config_frame, text="✨ Tóm tắt", command=self.summarize_file, state="disabled")
        self.summarize_btn.grid(row=0, column=5, padx=5)

        self.stop_btn = ttk.Button(
            config_frame, text="⏹ STOP", command=self.stop_summarization, state="disabled")
        self.stop_btn.grid(row=0, column=6, padx=5)

        # Row 2: Length Slider
        ttk.Label(config_frame, text="Độ dài:").grid(
            row=1, column=0, padx=5, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=500)
        self.length_slider = ttk.Scale(
            config_frame, from_=100, to=1000, variable=self.length_var,
            orient=tk.HORIZONTAL, length=200
        )
        self.length_slider.grid(
            row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.length_label = ttk.Label(config_frame, text="500 từ")
        self.length_label.grid(row=1, column=3, padx=5)
        self.length_slider.config(command=self.update_length_label)

        # Row 3: Translation Option
        ttk.Label(config_frame, text="Dịch sang:").grid(
            row=2, column=0, padx=5, sticky=tk.W)
        self.translate_var = tk.StringVar(value="none")
        translate_options = ["Tiếng Việt", "English"]
        translate_values = ["none", "en"]
        self.translate_combo = ttk.Combobox(
            config_frame, values=translate_options, state="readonly", width=15
        )
        self.translate_combo.current(0)
        self.translate_combo.grid(row=2, column=1, padx=5, sticky=tk.W)

        # Bind events: update var + auto-translate
        def on_translate_selected(e):
            self.translate_var.set(
                translate_values[self.translate_combo.current()])
            self.on_language_change()

        self.translate_combo.bind(
            '<<ComboboxSelected>>', on_translate_selected)

        # Notebook with tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=3, column=0, columnspan=3,
                           sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Tab 1: Summary
        summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(summary_tab, text="📝 Tóm tắt")

        summary_tab.columnconfigure(0, weight=1)
        summary_tab.rowconfigure(0, weight=1)

        self.result_text = scrolledtext.ScrolledText(
            summary_tab, wrap=tk.WORD, font=("Arial", 10))
        self.result_text.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        button_frame = ttk.Frame(summary_tab)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        self.copy_btn = ttk.Button(
            button_frame, text="✏️ Copy", command=self.copy_result, state="disabled")
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = ttk.Button(
            button_frame, text="💾 Save", command=self.save_result, state="disabled")
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Tab 2: Q&A
        qa_tab = ttk.Frame(self.notebook)
        self.qa_tab = qa_tab  # Store reference to enable/disable tab
        self.notebook.add(qa_tab, text="📝 Hỏi đáp",
                          state="disabled")  # Disabled by default

        qa_tab.columnconfigure(0, weight=1)
        qa_tab.rowconfigure(0, weight=1)

        self.qa_text = scrolledtext.ScrolledText(
            qa_tab, wrap=tk.WORD, font=("Arial", 10), state="disabled")
        self.qa_text.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        qa_input_frame = ttk.Frame(qa_tab)
        qa_input_frame.grid(row=1, column=0, sticky=(
            tk.W, tk.E), padx=5, pady=5)
        qa_input_frame.columnconfigure(0, weight=1)

        ttk.Label(qa_input_frame, text="Câu hỏi:").grid(
            row=0, column=0, sticky=tk.W, pady=2)

        self.question_entry = ttk.Entry(qa_input_frame, width=60)
        self.question_entry.grid(
            row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        # Bind Enter key - return 'break' to prevent default behavior

        def on_enter(event):
            self.ask_question()
            return 'break'  # Prevent default Enter behavior
        self.question_entry.bind('<Return>', on_enter)

        self.ask_btn = ttk.Button(
            qa_input_frame, text="🤔 Hỏi", command=self.ask_question)
        self.ask_btn.grid(row=1, column=1)

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame, mode='indeterminate', length=300)
        self.progress.grid(row=4, column=0, columnspan=3, pady=5)

        # Status label
        self.status_label = ttk.Label(
            main_frame, text="Sẵn sàng", foreground="green")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)

    def update_length_label(self, value):
        """Cập nhật label hiển thị độ dài"""
        length = int(float(value))
        self.length_label.config(text=f"{length} từ")

    def on_language_change(self):
        """Tự động dịch khi thay đổi ngôn ngữ từ dropdown"""
        if not self.current_summary or not self.original_summary:
            return

        selected_lang = self.translate_combo.get()

        # Nếu chọn "Tiếng Việt", hiển thị bản gốc
        if selected_lang == "Tiếng Việt":
            self.result_text.delete(1.0, tk.END)
            word_info = f"📊 Gốc: {self.original_word_count} từ → Tóm tắt: {len(self.original_summary.split())} từ ({len(self.original_summary.split())*100//max(self.original_word_count, 1)}%)\n\n"
            self.result_text.insert(
                1.0, f"📝 KẾT QUẢ (Tiếng Việt):\n\n{word_info}{self.original_summary}")
            self.current_summary = self.original_summary
            self.current_summary_language = "vi"
            self.status_label.config(
                text="✅ Hiển thị bản Tiếng Việt", foreground="green")
            return

        # Chọn "English" - Kiểm tra cache trước
        if "English" in self.translation_cache:
            translated = self.translation_cache["English"]
            self.result_text.delete(1.0, tk.END)
            word_info = f"📊 Original: {self.original_word_count} words → Summary: {len(translated.split())} words\n\n"
            self.result_text.insert(
                1.0, f"📝 RESULT (English):\n\n{word_info}{translated}")
            self.current_summary = translated
            self.current_summary_language = "en"
            self.status_label.config(
                text="✅ Showing English version (from cache)", foreground="green")
            return

        # Dịch mới sang English
        self.status_label.config(
            text="🔄 Translating to English...", foreground="orange")
        self.progress.start(10)

        # Chạy trong thread riêng
        thread = threading.Thread(
            target=self.translate_summary_thread,
            args=(self.original_summary,),
            daemon=True
        )
        thread.start()

    def translate_summary_thread(self, text):
        """Thread dịch văn bản sang English"""
        try:
            prompt = f"""Translate the following Vietnamese text to English. 
Keep the formatting and structure. Only provide the English translation, no explanations.

Vietnamese text:
{text}

English translation:"""

            import ollama
            response = ollama.chat(
                model=self.model_var.get(),
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )

            translated = response['message']['content'].strip()

            # Lưu vào cache với key "English"
            self.translation_cache["English"] = translated

            # Cập nhật UI trong main thread
            self.root.after(0, self.display_translation, translated)

        except Exception as e:
            self.root.after(0, self.show_translation_error, str(e))

    def display_translation(self, translated_text):
        """Hiển thị bản dịch English"""
        self.result_text.delete(1.0, tk.END)
        word_info = f"📊 Original: {self.original_word_count} words → Summary: {len(translated_text.split())} words\n\n"
        self.result_text.insert(
            1.0, f"📝 RESULT (English):\n\n{word_info}{translated_text}")
        self.current_summary = translated_text
        self.current_summary_language = "en"

        words = len(translated_text.split())
        self.status_label.config(
            text=f"✅ Translated to English ({words} words)", foreground="green")
        self.progress.stop()

    def show_translation_error(self, error):
        """Hiển thị lỗi dịch"""
        self.status_label.config(text=f"❌ Lỗi dịch: {error}", foreground="red")
        self.progress.stop()
        messagebox.showerror("Lỗi dịch", f"Không thể dịch: {error}")

    def select_file(self):
        """Xử lý chọn file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file để tóm tắt",
            filetypes=[
                ("All Supported", "*.txt *.pdf *.docx"),
                ("Text Files", "*.txt"),
                ("PDF Files", "*.pdf"),
                ("Word Files", "*.docx")
            ]
        )

        if file_path:
            self.current_file = file_path
            import os
            file_name = os.path.basename(file_path)
            self.file_label.config(text=file_name, foreground="black")
            self.summarize_btn.config(state="normal")

            # Enable Q&A tab and read file content
            self.notebook.tab(1, state="normal")  # Enable Q&A tab (index 1)
            try:
                self.original_content = self.file_reader.read_file(file_path)
                self.original_word_count = len(self.original_content.split())
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
                self.original_content = ""

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(
                1.0, f"File đã chọn: {file_name}\n\nNhấn nút 'Tóm tắt' để bắt đầu...")

    def on_model_change(self, event):
        """Xử lý khi thay đổi model"""
        selected_model = self.model_var.get()
        self.ai_summarizer.set_model(selected_model)

    def summarize_file(self):
        """Xử lý tóm tắt file"""
        if not self.current_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return

        self.select_btn.config(state="disabled")
        self.summarize_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.stop_event.clear()

        self.progress.start(10)
        self.status_label.config(text="Đang xử lý...", foreground="orange")

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(
            1.0, "Đang đọc file và tóm tắt...\nVui lòng đợi...\n\n")

        self.summary_thread = threading.Thread(target=self._do_summarize)
        self.summary_thread.daemon = True
        self.summary_thread.start()

    def _do_summarize(self):
        """Thực hiện summarization"""
        try:
            self.update_status("Đang đọc file...")
            content = self.file_reader.read_file(self.current_file)

            if not content.strip():
                raise Exception("File trống!")

            self.original_content = content
            self.original_word_count = len(content.split())

            self.update_status(
                f"Đang tóm tắt với model {self.model_var.get()}...")

            if self.stop_event.is_set():
                self.display_result("Đã dừng!", success=False)
                return

            # Get max_length from slider
            max_length = self.length_var.get()

            if self.summary_type.get() == "bullet":
                summary = self.ai_summarizer.summarize_with_bullet_points(
                    content)
            else:
                summary = self.ai_summarizer.summarize(
                    content, max_length=max_length)

            # Translation if needed
            if self.translate_var.get() != "none":
                self.update_status(
                    f"Đang dịch sang {self.translate_combo.get()}...")
                summary = self.translate_text(
                    summary, self.translate_var.get())

            self.display_result(summary, success=True)
        except Exception as e:
            self.display_result(f"Lỗi: {str(e)}", success=False)

    def translate_text(self, text, target_lang):
        """Dịch văn bản sang ngôn ngữ khác"""
        lang_names = {
            "en": "English",
            "vi": "Vietnamese (Tiếng Việt)",
            "zh": "Chinese (中文)",
            "ja": "Japanese (日本語)",
            "ko": "Korean (한국어)"
        }

        prompt = f"""Translate the following text to {lang_names.get(target_lang, target_lang)}.
Only return the translated text, no explanations.

Text to translate:
{text}

Translation:"""

        try:
            import ollama
            response = ollama.chat(
                model=self.model_var.get(),
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content'].strip()
        except Exception as e:
            return f"[Lỗi dịch: {str(e)}]\n\n{text}"

    def ask_question(self):
        """Ủ lý hỏi đáp về văn bản"""
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập câu hỏi!")
            return

        if not self.original_content:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return

        # Clear input immediately after getting the question
        self.question_entry.delete(0, tk.END)
        self.ask_btn.config(state="disabled")
        self.question_entry.config(state="disabled")

        self.progress.start(10)
        self.status_label.config(
            text="🤔 Đang suy nghĩ...", foreground="orange")

        # Show loading in Q&A text area
        self.qa_text.config(state="normal")
        self.qa_text.insert(tk.END, f"\n{'='*50}\n")
        self.qa_text.insert(tk.END, f"❓ Câu hỏi: {question}\n\n")
        self.qa_text.insert(tk.END, "💭 Đang suy nghĩ... Vui lòng đợi...\n")
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
                    messages=[{'role': 'user', 'content': prompt}]
                )
                answer = response['message']['content'].strip()

                def update_qa():
                    self.qa_text.config(state="normal")
                    # Remove loading message (last 2 lines)
                    content = self.qa_text.get(1.0, tk.END)
                    lines = content.split('\n')
                    # Remove "💭 Đang suy nghĩ..." line
                    if "💭 Đang suy nghĩ" in content:
                        # Delete last occurrence of loading message
                        self.qa_text.delete("end-2l", "end-1l")

                    self.qa_text.insert(tk.END, f"💡 Trả lời: {answer}\n")
                    self.qa_text.see(tk.END)
                    self.qa_text.config(state="disabled")
                    # Input already cleared, just re-enable and focus
                    self.question_entry.config(state="normal")
                    self.question_entry.focus()
                    self.ask_btn.config(state="normal")
                    self.progress.stop()
                    self.status_label.config(
                        text="Hoàn thành Q&A!", foreground="green")

                self.root.after(0, update_qa)

            except Exception as e:
                def show_error():
                    # Remove loading message
                    self.qa_text.config(state="normal")
                    content = self.qa_text.get(1.0, tk.END)
                    if "💭 Đang suy nghĩ" in content:
                        self.qa_text.delete("end-2l", "end-1l")
                    self.qa_text.insert(tk.END, f"❌ Lỗi: {str(e)}\n")
                    self.qa_text.see(tk.END)
                    self.qa_text.config(state="disabled")

                    self.question_entry.config(state="normal")
                    self.ask_btn.config(state="normal")
                    self.progress.stop()
                    self.status_label.config(text="❌ Lỗi!", foreground="red")
                self.root.after(0, show_error)

        qa_thread = threading.Thread(target=do_qa)
        qa_thread.daemon = True
        qa_thread.start()

    def stop_summarization(self):
        """Dừng quá trình AI"""
        self.stop_event.set()
        self.progress.stop()
        self.status_label.config(text="⏹ Đã dừng!", foreground="red")
        self.stop_btn.config(state="disabled")
        self.select_btn.config(state="normal")
        self.summarize_btn.config(state="normal")

    def update_status(self, message):
        """Cập nhật status"""
        self.root.after(0, lambda: self.status_label.config(
            text=message, foreground="orange"))
        self.root.after(0, lambda: self.result_text.insert(
            tk.END, f"{message}\n"))

    def copy_result(self):
        """Copy kết quả"""
        if self.current_summary:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_summary)
            self.root.update()
            messagebox.showinfo("Thành công", "Đã copy vào clipboard!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có kết quả!")

    def save_result(self):
        """Lưu kết quả"""
        if not self.current_summary:
            messagebox.showwarning("Cảnh báo", "Không có kết quả để lưu!")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"summary_{timestamp}.txt"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Lưu kết quả"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_summary)
                messagebox.showinfo("Thành công", f"Đã lưu vào:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")

    def display_result(self, result, success=True):
        """Hiển thị kết quả"""
        def update_ui():
            self.progress.stop()
            self.result_text.delete(1.0, tk.END)

            if success:
                self.summary_word_count = len(result.split())
                word_info = f"📊 Gốc: {self.original_word_count} từ → Tóm tắt: {self.summary_word_count} từ ({self.summary_word_count*100//max(self.original_word_count, 1)}%)\n\n"

                self.result_text.insert(
                    1.0, f"📝 KẾT QUẢ:\n\n{word_info}{result}")
                self.status_label.config(
                    text="✅ Hoàn thành!", foreground="green")

                # Lưu bản gốc và reset cache
                self.original_summary = result
                self.current_summary = result
                self.current_summary_language = "vi"
                self.translation_cache = {}  # Reset cache khi có summary mới

                # Reset dropdown về "Tiếng Việt"
                self.translate_combo.set("Tiếng Việt")

                self.copy_btn.config(state="normal")
                self.save_btn.config(state="normal")
                self.ask_btn.config(state="normal")

                self.word_count_label.config(
                    text=f"📊 {self.original_word_count} từ → {self.summary_word_count} từ"
                )
            else:
                self.result_text.insert(1.0, f"❌ {result}")
                self.status_label.config(text="Lỗi!", foreground="red")
                self.current_summary = ""
                self.copy_btn.config(state="disabled")
                self.save_btn.config(state="disabled")

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
