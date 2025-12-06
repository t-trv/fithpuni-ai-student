"""
AI Summary Application - Ứng dụng tóm tắt văn bản sử dụng AI
Sử dụng Ollama local models để tóm tắt file .txt, .pdf, .docx
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from datetime import datetime
from file_reader import FileReader
from ai_summarizer import AISummarizer


class AISummaryApp:
    """Class chính cho ứng dụng AI Summary"""

    def __init__(self, root):
        """Khởi tạo giao diện ứng dụng"""
        self.root = root
        self.root.title("AI Summary - Tóm tắt văn bản bằng AI")
        self.root.geometry("900x700")

        # Khởi tạo components
        self.file_reader = FileReader()
        self.ai_summarizer = AISummarizer()
        self.current_file = None
        self.current_summary = ""  # Lưu kết quả tóm tắt hiện tại
        self.original_content = ""  # Lưu nội dung gốc để hỏi đáp
        self.original_word_count = 0
        self.summary_word_count = 0
        self.summary_thread = None
        self.stop_event = threading.Event()

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
            text="🤖 AI Summary Application",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Frame cho file selection
        file_frame = ttk.LabelFrame(main_frame, text="Chọn File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3,
                        sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(1, weight=1)

        # Button chọn file
        self.select_btn = ttk.Button(
            file_frame,
            text="📁 Chọn File",
            command=self.select_file
        )
        self.select_btn.grid(row=0, column=0, padx=5)

        # Label hiển thị file đã chọn
        self.file_label = ttk.Label(
            file_frame, text="Chưa chọn file nào", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # Frame cho model selection
        model_frame = ttk.LabelFrame(
            main_frame, text="Cấu hình AI", padding="10")
        model_frame.grid(row=2, column=0, columnspan=3,
                         sticky=(tk.W, tk.E), pady=5)
        model_frame.columnconfigure(1, weight=1)

        # Model selection
        ttk.Label(model_frame, text="Model:").grid(
            row=0, column=0, padx=5, sticky=tk.W)
        self.model_var = tk.StringVar(value="llama3.2:1b")
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=self.ai_summarizer.get_available_models(),
            state="readonly",
            width=20
        )
        self.model_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
        self.model_combo.bind('<<ComboboxSelected>>', self.on_model_change)

        # Summary type
        ttk.Label(model_frame, text="Kiểu tóm tắt:").grid(
            row=0, column=2, padx=5, sticky=tk.W)
        self.summary_type = tk.StringVar(value="normal")
        ttk.Radiobutton(
            model_frame,
            text="Tóm tắt thường",
            variable=self.summary_type,
            value="normal"
        ).grid(row=0, column=3, padx=5)
        ttk.Radiobutton(
            model_frame,
            text="Điểm chính",
            variable=self.summary_type,
            value="bullet"
        ).grid(row=0, column=4, padx=5)

        # Button summarize
        self.summarize_btn = ttk.Button(
            model_frame,
            text="✨ Tóm tắt",
            command=self.summarize_file,
            state="disabled"
        )
        self.summarize_btn.grid(row=0, column=5, padx=10)

        # Button STOP
        self.stop_btn = ttk.Button(
            model_frame,
            text="⏹ STOP",
            command=self.stop_summarization,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=6, padx=10)

        # Frame cho kết quả
        result_frame = ttk.LabelFrame(
            main_frame, text="Kết quả tóm tắt", padding="10")
        result_frame.grid(row=3, column=0, columnspan=3,
                          sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        # Text area hiển thị kết quả
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Arial", 10)
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Button frame cho Copy và Save
        button_frame = ttk.Frame(result_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        self.copy_btn = ttk.Button(
            button_frame,
            text="✏️ Copy",
            command=self.copy_result,
            state="disabled"
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = ttk.Button(
            button_frame,
            text="💾 Save",
            command=self.save_result,
            state="disabled"
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=4, column=0, columnspan=3, pady=5)

        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Sẵn sàng",
            foreground="green"
        )
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)

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
            # Hiển thị tên file
            import os
            file_name = os.path.basename(file_path)
            self.file_label.config(text=file_name, foreground="black")
            self.summarize_btn.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(
                1.0, f"File đã chọn: {file_name}\n\nNhấn nút 'Tóm tắt' để bắt đầu...")

    def on_model_change(self, event):
        """Xử lý khi thay đổi model"""
        selected_model = self.model_var.get()
        self.ai_summarizer.set_model(selected_model)
        self.status_label.config(
            text=f"Đã chọn model: {selected_model}", foreground="blue")

    def summarize_file(self):
        """Xử lý tóm tắt file"""
        if not self.current_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return

        # Disable buttons
        self.select_btn.config(state="disabled")
        self.summarize_btn.config(state="disabled")

        self.stop_btn.config(state="normal")
        self.stop_event.clear()

        # Start progress bar
        self.progress.start(10)
        self.status_label.config(text="Đang xử lý...", foreground="orange")

        # Clear result
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(
            1.0, "Đang đọc file và tóm tắt...\nVui lòng đợi...\n\n")

        # Run summarization in thread to avoid freezing UI
        self.summary_thread = threading.Thread(target=self._do_summarize)
        self.summary_thread.daemon = True
        self.summary_thread.start()

    def _do_summarize(self):
        """Thực hiện summarization (chạy trong thread riêng)"""
        try:
            # Đọc file
            self.update_status("Đang đọc file...")
            content = self.file_reader.read_file(self.current_file)

            if not content.strip():
                raise Exception("File trống hoặc không có nội dung text!")

            # Tóm tắt
            self.update_status(
                f"Đang tóm tắt với model {self.model_var.get()}...")

            summary = None
            if not self.stop_event.is_set():
                if self.summary_type.get() == "bullet":
                    summary = self.ai_summarizer.summarize_with_bullet_points(
                        content)
                else:
                    summary = self.ai_summarizer.summarize(content)
            if self.stop_event.is_set():
                self.display_result(
                    "Đã dừng quá trình tóm tắt!", success=False)
            else:
                self.display_result(summary, success=True)
        except Exception as e:
            self.display_result(f"Lỗi: {str(e)}", success=False)

    def stop_summarization(self):
        """Dừng quá trình AI summarization và cho phép tiếp tục sử dụng các chức năng khác"""
        self.stop_event.set()
        self.progress.stop()
        self.status_label.config(
            text="⏹ Đã dừng quá trình AI!", foreground="red")
        self.stop_btn.config(state="disabled")
        # Enable lại các nút để người dùng tiếp tục thao tác
        self.select_btn.config(state="normal")
        self.summarize_btn.config(state="normal")

    def update_status(self, message):
        """Cập nhật status label"""
        self.root.after(0, lambda: self.status_label.config(
            text=message, foreground="orange"))
        self.root.after(0, lambda: self.result_text.insert(
            tk.END, f"{message}\n"))

    def copy_result(self):
        """Copy kết quả tóm tắt vào clipboard"""
        if self.current_summary:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_summary)
            self.root.update()
            messagebox.showinfo("Thành công", "Đã copy kết quả vào clipboard!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có kết quả để copy!")

    def save_result(self):
        """Lưu kết quả tóm tắt ra file"""
        if not self.current_summary:
            messagebox.showwarning("Cảnh báo", "Không có kết quả để lưu!")
            return

        # Tạo tên file mặc định với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"summary_{timestamp}.txt"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Lưu kết quả tóm tắt"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_summary)
                messagebox.showinfo(
                    "Thành công", f"Đã lưu kết quả vào:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file:\n{str(e)}")

    def display_result(self, result, success=True):
        """Hiển thị kết quả"""
        def update_ui():
            # Stop progress bar
            self.progress.stop()

            # Clear and show result
            self.result_text.delete(1.0, tk.END)

            if success:
                self.result_text.insert(1.0, f"📝 KẾT QUẢ TÓM TẮT:\n\n{result}")
                self.status_label.config(
                    text="Hoàn thành!", foreground="green")
                # Lưu kết quả và enable Copy/Save buttons
                self.current_summary = result
                self.copy_btn.config(state="normal")
                self.save_btn.config(state="normal")
            else:
                self.result_text.insert(1.0, f"❌ {result}")
                self.status_label.config(
                    text="Có lỗi xảy ra!", foreground="red")
                self.current_summary = ""
                self.copy_btn.config(state="disabled")
                self.save_btn.config(state="disabled")

            # Enable buttons
            self.select_btn.config(state="normal")
            self.summarize_btn.config(state="normal")

        self.root.after(0, update_ui)


def main():
    """Hàm main để chạy ứng dụng"""
    root = tk.Tk()
    app = AISummaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
