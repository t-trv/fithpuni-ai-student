# 🤖 AI Summary Application

Ứng dụng đơn giản để học về AI - Tóm tắt văn bản sử dụng Ollama local models

## 📖 Giới thiệu

Đây là một ứng dụng Python đơn giản giúp bạn học về AI và cách sử dụng các model AI local thông qua Ollama. Ứng dụng có thể đọc và tóm tắt nội dung từ các file:
- 📄 `.txt` (Text files)
- 📕 `.pdf` (PDF documents)  
- 📘 `.docx` (Word documents)

## ✨ Tính năng

- ✅ Giao diện đồ họa đơn giản, dễ sử dụng
- ✅ Hỗ trợ nhiều định dạng file (.txt, .pdf, .docx)
- ✅ Chọn model AI từ Ollama local
- ✅ 2 chế độ tóm tắt:
  - Tóm tắt thường (paragraph)
  - Điểm chính (bullet points)
- ✅ Xử lý đa luồng (không bị đơ giao diện)

## 📋 Yêu cầu

### 1. Ollama
Bạn cần cài đặt Ollama và tải xuống các model. Bạn đã có sẵn các model:
- `tinyllama:latest`
- `llama3.2:1b` (được dùng mặc định)
- `gpt-oss:20b`
- `mistral:latest`
- `gemma3:4b`

**Kiểm tra Ollama đang chạy:**
```powershell
ollama list
```

Nếu chưa chạy, khởi động Ollama service trước khi dùng app.

### 2. Python
- Python 3.8 trở lên
- tkinter (thường có sẵn với Python)

## 🚀 Cài đặt

### Bước 1: Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

Các thư viện sẽ được cài:
- `ollama` - SDK để giao tiếp với Ollama
- `PyPDF2` - Đọc file PDF
- `python-docx` - Đọc file Word

### Bước 2: Đảm bảo Ollama đang chạy

Mở terminal mới và chạy:
```powershell
ollama serve
```

Hoặc Ollama có thể tự động chạy dưới dạng service.

## 🎮 Cách sử dụng

### Chạy ứng dụng:

```powershell
python main.py
```

### Các bước sử dụng:

1. **Chọn file**: Click nút "📁 Chọn File" và chọn file .txt, .pdf, hoặc .docx
2. **Chọn model**: Chọn model AI bạn muốn dùng từ dropdown (mặc định: llama3.2:1b)
3. **Chọn kiểu tóm tắt**: 
   - "Tóm tắt thường" - Tóm tắt dạng đoạn văn
   - "Điểm chính" - Liệt kê các ý chính
4. **Tóm tắt**: Click nút "✨ Tóm tắt" và đợi kết quả

## 📂 Cấu trúc project

```
AI_Summary/
│
├── main.py              # File chính - Giao diện GUI
├── ai_summarizer.py     # Module xử lý AI với Ollama
├── file_reader.py       # Module đọc các loại file
├── requirements.txt     # Dependencies
└── README.md           # Hướng dẫn này
```

## 🧠 Giải thích code cho người mới

### 1. `file_reader.py`
Module này chứa class `FileReader` với các phương thức:
- `read_txt()` - Đọc file text đơn giản
- `read_pdf()` - Dùng PyPDF2 để extract text từ PDF
- `read_docx()` - Dùng python-docx để đọc Word document
- `read_file()` - Tự động chọn phương thức đúng dựa trên extension

### 2. `ai_summarizer.py`
Module này chứa class `AISummarizer`:
- Kết nối với Ollama API
- `summarize()` - Tóm tắt văn bản dạng paragraph
- `summarize_with_bullet_points()` - Tóm tắt dạng bullet points
- Sử dụng prompt engineering để hướng dẫn AI tóm tắt

**Cách AI hoạt động:**
- Gửi văn bản + prompt (câu yêu cầu) đến model
- Model AI xử lý và trả về kết quả
- Tất cả chạy trên máy local của bạn qua Ollama

### 3. `main.py`
File chính chứa GUI application:
- Sử dụng `tkinter` để tạo giao diện
- `threading` để chạy AI không làm đơ giao diện
- Kết nối tất cả components lại với nhau

## 💡 Tips cho người mới học AI

### Model nào nên dùng?

- **`tinyllama:latest`** - Nhỏ nhất, nhanh nhất, kết quả đơn giản
- **`llama3.2:1b`** - Nhỏ, nhanh, kết quả tốt (khuyên dùng để bắt đầu)
- **`mistral:latest`** - Cân bằng tốc độ và chất lượng
- **`gemma3:4b`** - Model lớn hơn, kết quả tốt hơn nhưng chậm hơn
- **`gpt-oss:20b`** - Lớn nhất, chất lượng cao nhất nhưng chậm nhất

### Prompt Engineering là gì?

Trong file `ai_summarizer.py`, bạn sẽ thấy biến `prompt`. Đây là cách bạn "nói chuyện" với AI:

```python
prompt = f"""Bạn là một trợ lý AI chuyên tóm tắt văn bản. 
Hãy đọc văn bản dưới đây và tạo một bản tóm tắt ngắn gọn...
"""
```

Bạn có thể thử thay đổi prompt để có kết quả khác nhau!

### Cách AI làm việc:

1. **Input**: Bạn cung cấp văn bản + yêu cầu (prompt)
2. **Processing**: AI model xử lý bằng neural network
3. **Output**: AI tạo ra văn bản mới (bản tóm tắt)

Tất cả chạy **local trên máy bạn**, không gửi data lên internet!

## 🔧 Tùy chỉnh và mở rộng

### Thay đổi độ dài tóm tắt:

Trong `ai_summarizer.py`, dòng 51:
```python
def summarize(self, text, max_length=500):  # Thay đổi 500 thành số khác
```

### Thêm model mới:

Nếu bạn tải model mới từ Ollama:
```powershell
ollama pull llama2
```

Thêm vào list trong `ai_summarizer.py`:
```python
self.available_models = [
    "tinyllama:latest",
    "llama3.2:1b", 
    # ...
    "llama2:latest"  # Thêm model mới
]
```

### Thêm định dạng file mới:

Bạn có thể thêm hỗ trợ cho `.html`, `.md`, etc. bằng cách:
1. Tìm thư viện Python để đọc file đó
2. Thêm method mới vào `FileReader`
3. Update `read_file()` method

## ❓ Troubleshooting

### Lỗi "Cannot connect to Ollama"
- Đảm bảo Ollama đang chạy: `ollama serve`
- Kiểm tra Ollama đang lắng nghe trên port 11434

### Lỗi khi đọc PDF
- Một số PDF có mã hóa đặc biệt hoặc chỉ là hình ảnh (scanned)
- Thử với file PDF khác hoặc dùng OCR

### AI tóm tắt không tốt
- Thử model lớn hơn (mistral, gemma3)
- Điều chỉnh prompt trong `ai_summarizer.py`
- Đảm bảo văn bản input rõ ràng, không bị lỗi font

### Ứng dụng chạy chậm
- Model lớn sẽ chậm hơn, thử model nhỏ hơn
- Kiểm tra CPU/RAM usage
- File quá lớn có thể mất nhiều thời gian

## 📚 Học thêm về AI

### Khái niệm cơ bản:
- **LLM (Large Language Model)**: Model AI được train trên lượng lớn text
- **Local AI**: Chạy AI trên máy local, không cần internet/API key
- **Ollama**: Tool giúp chạy LLM local dễ dàng
- **Inference**: Quá trình AI xử lý input và tạo output

### Resources:
- [Ollama Documentation](https://ollama.ai/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- Python AI tutorials trên YouTube

## 🎯 Bài tập mở rộng

Sau khi hiểu code, bạn có thể thử:

1. ✏️ Thêm nút "Copy" để copy kết quả vào clipboard
2. 💾 Thêm nút "Save" để lưu tóm tắt ra file
3. 🌍 Thêm option để dịch sang ngôn ngữ khác
4. 📊 Hiển thị số từ gốc vs số từ tóm tắt
5. ⚙️ Thêm thanh slider để điều chỉnh độ dài tóm tắt
6. 📝 Thêm tab mới cho "Ask Questions" về văn bản
7. 🎨 Tùy chỉnh theme/màu sắc của UI

## 📝 License

Project này mở để học tập. Bạn có thể tự do sử dụng và chỉnh sửa!

## 🤝 Đóng góp

Nếu bạn có ý tưởng cải thiện, hãy:
1. Fork project
2. Tạo feature branch
3. Commit changes
4. Tạo Pull Request

---

**Chúc bạn học vui vẻ và khám phá thế giới AI! 🚀**

Nếu có câu hỏi, đừng ngại hỏi trong Issues!
