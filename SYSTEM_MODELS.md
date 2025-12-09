# 📊 MÔ HÌNH QUAN HỆ VÀ CLASS DIAGRAM - AI SUMMARY PROJECT

## I. CLASS DIAGRAM

### **1. Class FileReader**

```
┌────────────────────────────────────┐
│         FileReader                 │
├────────────────────────────────────┤
│ Attributes:                        │
│  (không có attributes)             │
├────────────────────────────────────┤
│ Methods:                           │
│  + read_txt(file_path: str)       │
│    → str                           │
│  + read_pdf(file_path: str)       │
│    → str                           │
│  + read_docx(file_path: str)      │
│    → str                           │
│  + read_file(file_path: str)      │
│    → str                           │
└────────────────────────────────────┘
```

**Chi tiết:**

| Phương thức | Tham số | Kiểu trả về | Mục đích |
|-----------|--------|-----------|---------|
| `read_txt()` | file_path: str | str | Đọc file text đơn giản |
| `read_pdf()` | file_path: str | str | Đọc PDF sử dụng PyPDF2 |
| `read_docx()` | file_path: str | str | Đọc Word document |
| `read_file()` | file_path: str | str | Dispatcher - tự động chọn method |

**Cách thức hoạt động:**
```
read_file(file_path)
    ├─ Kiểm tra extension
    ├─ .txt → read_txt()
    ├─ .pdf → read_pdf()
    ├─ .docx → read_docx()
    └─ Invalid → raise Exception
```

---

### **2. Class AISummarizer**

```
┌──────────────────────────────────────────┐
│          AISummarizer                    │
├──────────────────────────────────────────┤
│ Attributes:                              │
│  - model_name: str                       │
│  - available_models: List[str]           │
├──────────────────────────────────────────┤
│ Methods:                                 │
│  + __init__(model_name: str)            │
│  + set_model(model_name: str) → None    │
│  + get_available_models() → List[str]   │
│  + summarize(text: str,                 │
│              max_length: int) → str     │
│  + summarize_with_bullet_points(        │
│      text: str) → str                   │
└──────────────────────────────────────────┘
```

**Chi tiết Attributes:**

| Attribute | Kiểu | Giá trị mặc định | Mô tả |
|-----------|------|-----------------|-------|
| `model_name` | str | "llama3.2:1b" | Mô hình hiện tại |
| `available_models` | List[str] | ['tinyllama:latest', 'llama3.2:1b', 'gpt-oss:20b', 'mistral:latest', 'gemma3:4b'] | Danh sách mô hình |

**Chi tiết Methods:**

| Phương thức | Tham số | Kiểu trả về | Mục đích |
|-----------|--------|-----------|---------|
| `__init__()` | model_name: str = "llama3.2:1b" | None | Khởi tạo summarizer |
| `set_model()` | model_name: str | None | Thay đổi mô hình |
| `get_available_models()` | - | List[str] | Lấy danh sách mô hình |
| `summarize()` | text: str, max_length: int = 5000 | str | Tóm tắt thường |
| `summarize_with_bullet_points()` | text: str | str | Tóm tắt bullet points |

**Quy trình Summarize:**
```
summarize(text, max_length)
    ├─ Tạo prompt
    │  ├─ Đặt vai trò: "trợ lý AI chuyên tóm tắt"
    │  ├─ Đặt yêu cầu: độ dài (max_length)
    │  ├─ Đặt format: paragraph
    │  └─ Nhúng văn bản
    ├─ Gọi Ollama API
    │  └─ ollama.chat(model, messages)
    ├─ Nhận response
    ├─ Xử lý kết quả (strip)
    └─ Trả về tóm tắt
```

---

### **3. Class AISummaryApp**

```
┌──────────────────────────────────────────┐
│         AISummaryApp                     │
├──────────────────────────────────────────┤
│ Attributes:                              │
│  - root: tk.Tk                          │
│  - file_reader: FileReader              │
│  - ai_summarizer: AISummarizer          │
│  - current_file: str                    │
│  - current_summary: str                 │
│  - original_content: str                │
│  - original_word_count: int             │
│  - summary_word_count: int              │
│  - summary_thread: Thread               │
│  - stop_event: Event                    │
│  - [UI Components] (buttons, labels,   │
│    text areas, dropdowns)               │
├──────────────────────────────────────────┤
│ Methods:                                 │
│  + __init__(root: tk.Tk)               │
│  + create_widgets() → None              │
│  + select_file() → None                 │
│  + on_model_change(event) → None       │
│  + summarize_file() → None              │
│  + perform_summarization() → None       │
│  + update_progress(message: str)        │
│    → None                               │
│  + clear_results() → None               │
│  + word_count(text: str) → int          │
└──────────────────────────────────────────┘
```

**Chi tiết Attributes:**

| Attribute | Kiểu | Mục đích |
|-----------|------|---------|
| `root` | tk.Tk | Cửa sổ chính |
| `file_reader` | FileReader | Đọc file |
| `ai_summarizer` | AISummarizer | Tóm tắt AI |
| `current_file` | str | File hiện tại |
| `current_summary` | str | Kết quả tóm tắt |
| `original_content` | str | Nội dung gốc |
| `original_word_count` | int | Số từ gốc |
| `summary_word_count` | int | Số từ tóm tắt |
| `summary_thread` | Thread | Thread xử lý |
| `stop_event` | Event | Dừng xử lý |

**Chi tiết Methods:**

| Phương thức | Tham số | Kiểu trả về | Mục đích |
|-----------|--------|-----------|---------|
| `__init__()` | root: tk.Tk | None | Khởi tạo app |
| `create_widgets()` | - | None | Tạo UI elements |
| `select_file()` | - | None | Chọn file dialog |
| `on_model_change()` | event | None | Xử lý thay đổi model |
| `summarize_file()` | - | None | Bắt đầu tóm tắt |
| `perform_summarization()` | - | None | Thực hiện tóm tắt (thread) |
| `update_progress()` | message: str | None | Cập nhật progress |
| `clear_results()` | - | None | Xóa kết quả |
| `word_count()` | text: str | int | Đếm từ |

---

## II. MỐI QUAN HỆ GIỮA CÁC CLASS

```
┌──────────────────┐
│  AISummaryApp    │
│   (Main UI)      │
└────────┬─────────┘
         │
         ├─── uses ───> ┌──────────────────┐
         │              │   FileReader     │
         │              │  (Read Files)    │
         │              └──────────────────┘
         │
         └─── uses ───> ┌──────────────────┐
                        │  AISummarizer    │
                        │  (AI Processing) │
                        └──────────────────┘
                              │
                              ├─── calls ──> Ollama API
                              │
                              └─── uses ──> LLM Models
                                   (llama3.2, mistral, etc)
```

**Mô tả chi tiết:**

1. **AISummaryApp** → **FileReader**
   - Sử dụng để đọc nội dung file
   - Gọi: `file_reader.read_file(file_path)`
   - Nhận: Nội dung text

2. **AISummaryApp** → **AISummarizer**
   - Sử dụng để tóm tắt nội dung
   - Gọi: `ai_summarizer.summarize(content)` hoặc `ai_summarizer.summarize_with_bullet_points(content)`
   - Nhận: Tóm tắt text

3. **AISummarizer** → **Ollama API**
   - Gọi mô hình LLM qua HTTP API
   - Endpoint: `http://localhost:11434/api/chat`
   - Gửi: Prompt + Messages
   - Nhận: Response từ mô hình

---

## III. USE CASE DIAGRAM

```
┌─────────────────────────────────────────────────────┐
│                    System Boundary                  │
│                  AI Summary App                     │
│                                                     │
│  ┌──────────────────────────────────────────┐     │
│  │  Open File                                │     │
│  │  (Select .txt/.pdf/.docx)                 │     │
│  └────────────┬─────────────────────────────┘     │
│               │                                    │
│  ┌────────────▼─────────────────────────────┐     │
│  │  Read File Content                       │     │
│  │  (Extract text from file)                │     │
│  └────────────┬─────────────────────────────┘     │
│               │                                    │
│  ┌────────────▼─────────────────────────────┐     │
│  │  Select Model & Options                  │     │
│  │  (Choose LLM, summarization type)        │     │
│  └────────────┬─────────────────────────────┘     │
│               │                                    │
│  ┌────────────▼─────────────────────────────┐     │
│  │  Summarize Content                       │     │
│  │  (Process with AI)                       │     │
│  │                                          │     │
│  │  ├─ Paragraph Summarization              │     │
│  │  └─ Bullet Points Summarization          │     │
│  └────────────┬─────────────────────────────┘     │
│               │                                    │
│  ┌────────────▼─────────────────────────────┐     │
│  │  Display Results                         │     │
│  │  - Summary text                          │     │
│  │  - Statistics (compression ratio, etc)   │     │
│  └─────────────────────────────────────────┘     │
│                                                     │
│  External Systems:                                 │
│  - Ollama (LLM Processing)                        │
│  - File System (File Access)                      │
└─────────────────────────────────────────────────────┘
```

---

## IV. DATA FLOW DIAGRAM (DFD)

### **Level 0 (Context Diagram)**
```
┌──────────────┐                    ┌──────────────┐
│              │                    │              │
│    User      │◄──────────────────►│   AI Summary │
│              │    Input/Output    │   Application│
└──────────────┘                    └──────┬───────┘
                                           │
                        ┌──────────────────┼──────────────────┐
                        │                  │                  │
                   ┌────▼─────┐       ┌────▼─────┐       ┌────▼─────┐
                   │   File    │       │  Ollama  │       │  Model   │
                   │  System   │       │   API    │       │  Models  │
                   └───────────┘       └──────────┘       └──────────┘
```

### **Level 1 (Main Processes)**
```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       │ (1) Select File
       ▼
┌──────────────────────┐
│  1.0 File Selection  │─────┐
└──────┬───────────────┘     │
       │                      │
       │ (2) File Path        │
       ▼                      │
┌──────────────────────┐      │
│  2.0 Read File       │      │ File
│                      │      │ System
│  - read_txt()        │      │
│  - read_pdf()        │      │
│  - read_docx()       │      │
└──────┬───────────────┘      │
       │                      │
       │ (3) File Content     │
       ▼                      │
┌──────────────────────┐      │
│ 3.0 Process Content  │      │
│                      │      │
│ - Count words        │      │
│ - Store original     │      │
└──────┬───────────────┘      │
       │                      │
       │ (4) Content + Config │
       ▼                      │
┌──────────────────────┐      │
│  4.0 Summarize       │──────┤──────────┐
│                      │      │          │
│ - Create prompt      │      │ Ollama   │
│ - Call Ollama        │      │ API      │
│ - Receive summary    │      │          │
└──────┬───────────────┘      │          │
       │                      │          │
       │ (5) Summary Result   │          │
       ▼                      │          │
┌──────────────────────┐      │          │
│ 5.0 Display Results  │      │     ┌────▼──────┐
│                      │      │     │   Models  │
│ - Show summary       │      │     │           │
│ - Show statistics    │      │     │-llama3.2  │
│ - Allow export       │      │     │-mistral   │
└──────┬───────────────┘      │     │-tinyllama │
       │                      │     └───────────┘
       ▼                      │
   ┌────────┐                 │
   │ Output │─────────────────┘
   └────────┘
```

---

## V. SEQUENCE DIAGRAM

### **Scenario: User tóm tắt một file**

```
User          App              FileReader      AISummarizer      Ollama
 │             │                   │                │               │
 │─ Click "Select File" ──────────►│               │               │
 │             │                   │               │               │
 │             │─ File Dialog ─────┘               │               │
 │◄────────────────── File Path ───────────────────│               │
 │             │                   │               │               │
 │─ Choose Model & Type ──────────►│               │               │
 │             │                   │               │               │
 │─ Click "Summarize" ────────────►│               │               │
 │             │                   │               │               │
 │             │─ read_file() ────►│               │               │
 │             │◄──── Content ─────│               │               │
 │             │                   │               │               │
 │             │─ summarize() ─────┼──────────────►│               │
 │             │                   │               │               │
 │             │                   │   create_prompt()             │
 │             │                   │               │               │
 │             │                   │─── chat() ────┼──────────────►│
 │             │                   │               │               │
 │             │                   │               │ process      │
 │             │                   │               │ & generate   │
 │             │                   │               │               │
 │             │                   │               │◄─ response ──│
 │             │◄────── Summary ────┼───────────────┤               │
 │             │                   │               │               │
 │◄────────────────── Display ─────┘               │               │
 │             │                   │               │               │
```

**Chi tiết từng bước:**

```
1. User nhấn "Select File"
   → Mở file dialog
   → User chọn file .txt/.pdf/.docx

2. App nhận file path
   → Hiển thị tên file

3. User chọn:
   - Model: llama3.2, mistral, etc
   - Type: paragraph hoặc bullet points

4. User nhấn "Summarize"
   → App gọi FileReader.read_file(path)
   → Nhận content từ file

5. App gọi AISummarizer.summarize(content)
   → Tạo prompt chuyên biệt
   → Gọi Ollama API

6. Ollama xử lý:
   → Load model
   → Tokenize input
   → Process through transformer
   → Generate summary token by token

7. Ollama trả response
   → App nhận summary

8. App xử lý:
   → Strip whitespace
   → Count words
   → Calculate compression ratio
   → Display kết quả

9. UI cập nhật
   → Hiển thị summary
   → Hiển thị statistics
```

---

## VI. STATE DIAGRAM

### **App State Machine**

```
                 ┌─────────────────┐
                 │   INIT STATE    │
                 │  (App started)  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  IDLE STATE     │
                 │ (Ready for file)│◄───┐
                 └────────┬────────┘    │
                          │            │
         ┌────────────────┴────────────────────┐
         │                                     │
         ▼ (File selected)                     │ (Clear clicked)
    ┌─────────────────┐                      │
    │FILE_SELECTED    │                      │
    │(File loaded)    │                      │
    └────────┬────────┘                      │
             │                               │
             ▼ (Summarize clicked)           │
    ┌─────────────────┐                      │
    │PROCESSING STATE │                      │
    │(AI working)     │                      │
    └────────┬────────┘                      │
             │                               │
      ┌──────┴──────┐                        │
      ▼             ▼                        │
  Success      Error                        │
      │             │                        │
      │             ▼                        │
      │      ┌──────────────┐                │
      │      │ERROR STATE   │────────────────┘
      │      │(Show error)  │
      │      └──────────────┘
      │
      ▼
┌─────────────────────┐
│ RESULT_DISPLAYED    │
│ (Summary shown)     │
└────────┬────────────┘
         │
         └────────────────┤
                          │
                    (Clear/New file)
                          │
                          ▼
                    IDLE STATE
```

---

## VII. ENTITY-RELATIONSHIP DIAGRAM (ER)

### **Data Model**

```
┌──────────────────────────────────┐
│         ProcessedFile            │
├──────────────────────────────────┤
│ PK  file_id: UUID                │
│     file_name: String            │
│     file_path: String            │
│     file_type: Enum              │
│     file_size: Integer           │
│     original_word_count: Integer │
│     upload_timestamp: Datetime   │
│     content_hash: String         │
└────────────┬─────────────────────┘
             │
             │ 1..N
             │
             ▼
┌──────────────────────────────────┐
│       SummaryResult              │
├──────────────────────────────────┤
│ PK  summary_id: UUID             │
│ FK  file_id: UUID                │
│     original_content: Text       │
│     summary_text: Text           │
│     summary_type: Enum           │
│     model_used: String           │
│     summary_word_count: Integer  │
│     compression_ratio: Float     │
│     processing_time: Float       │
│     created_timestamp: Datetime  │
│     quality_score: Float         │
└────────────┬─────────────────────┘
             │
             │ 1..1
             │
             ▼
┌──────────────────────────────────┐
│      ModelConfiguration          │
├──────────────────────────────────┤
│ PK  config_id: UUID              │
│ FK  summary_id: UUID             │
│     model_name: String           │
│     model_version: String        │
│     max_length: Integer          │
│     temperature: Float           │
│     top_p: Float                 │
│     prompt_template: Text        │
│     language: String             │
└──────────────────────────────────┘
```

**Ý nghĩa quan hệ:**
- 1 File có thể được tóm tắt nhiều lần (1..N)
- Mỗi Summary Result có 1 Model Configuration (1..1)

---

## VIII. OBJECT DIAGRAM (INSTANCE EXAMPLE)

### **Ví dụ cụ thể**

```
┌─────────────────────────────────────┐
│ fileReader: FileReader              │
├─────────────────────────────────────┤
│ (static methods)                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ summarizer: AISummarizer            │
├─────────────────────────────────────┤
│ model_name = "llama3.2:1b"         │
│ available_models = [5 models]       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ app: AISummaryApp                   │
├─────────────────────────────────────┤
│ root = Tk window                    │
│ file_reader = fileReader            │
│ ai_summarizer = summarizer          │
│ current_file = "/path/file.pdf"    │
│ current_summary = "Long summary..." │
│ original_word_count = 12500         │
│ summary_word_count = 1200           │
└─────────────────────────────────────┘
```

---

## IX. COMPONENT DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│                   AI Summary Application                 │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │            UI Component Layer                    │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │   │
│  │  │ File     │  │ Model    │  │ Summary  │     │   │
│  │  │ Selection│  │ Selection│  │ Display  │     │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘     │   │
│  │       │             │             │            │   │
│  └───────┼─────────────┼─────────────┼────────────┘   │
│          │             │             │                │
│  ┌───────┴─────────────┴─────────────┴────────────┐   │
│  │      Business Logic Layer (main.py)           │   │
│  │                                                 │   │
│  │  ┌────────────────────────────────────────┐   │   │
│  │  │      AISummaryApp Controller           │   │   │
│  │  │ - Handle user input                    │   │   │
│  │  │ - Orchestrate workflows                │   │   │
│  │  │ - Manage threading                     │   │   │
│  │  └────────────────────────────────────────┘   │   │
│  └──────┬──────────────┬─────────────────────────┘   │
│         │              │                              │
│  ┌──────▼──┐   ┌──────▼────────────────────────┐   │
│  │ File I/O│   │  Processing Layer             │   │
│  │Component├──►├────────────────────────────────┤   │
│  │         │   │ - FileReader                  │   │
│  │ • Read  │   │ - AISummarizer                │   │
│  │   .txt  │   │ - Word counter                │   │
│  │ • Read  │   │ - Prompt builder              │   │
│  │   .pdf  │   └──────┬─────────────────────────┘   │
│  │ • Read  │          │                              │
│  │   .docx │   ┌──────▼──────────────────────────┐  │
│  └─────────┘   │   External Services            │  │
│                ├──────────────────────────────────┤  │
│                │ - Ollama API (LLM)            │  │
│                │ - Language Models             │  │
│                └──────────────────────────────────┘  │
│                                                       │
└─────────────────────────────────────────────────────────┘
```

---

## X. DEPLOYMENT DIAGRAM

```
┌─────────────────────────────────────────────────────┐
│                  User Machine                       │
│                  (Windows/Linux)                    │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │         AI Summary Application                │ │
│  │                                               │ │
│  │  ┌──────────┐  ┌────────────────────────┐   │ │
│  │  │   GUI    │  │  Application Logic     │   │ │
│  │  │(Tkinter) │  │                        │   │ │
│  │  └──────────┘  │ • file_reader.py      │   │ │
│  │                │ • ai_summarizer.py    │   │ │
│  │  ┌──────────┐  │ • main.py             │   │ │
│  │  │ Libraries│  │                        │   │ │
│  │  │          │  └────────┬───────────────┘   │ │
│  │  │ • PyPDF2 │           │                   │ │
│  │  │ • python-│           │                   │ │
│  │  │   docx   │           │                   │ │
│  │  │ • ollama │           │                   │ │
│  │  │   client │           │                   │ │
│  │  └──────────┘           │                   │ │
│  │                          │                   │ │
│  └──────────────────────────┼───────────────────┘ │
│                             │                      │
└─────────────────────────────┼──────────────────────┘
                              │
                    ┌─────────▼────────────┐
                    │   Local Network      │
                    └─────────┬────────────┘
                              │
                    ┌─────────▼────────────┐
                    │  Ollama Server       │
                    │  (localhost:11434)   │
                    │                      │
                    │  ┌────────────────┐  │
                    │  │ LLM Models     │  │
                    │  │                │  │
                    │  │ • llama3.2:1b  │  │
                    │  │ • mistral      │  │
                    │  │ • tinyllama    │  │
                    │  │ • gemma3       │  │
                    │  │ • gpt-oss      │  │
                    │  └────────────────┘  │
                    │                      │
                    │ GPU/CPU: Processing  │
                    │ RAM: Model Storage   │
                    │ Disk: Model Cache    │
                    │                      │
                    └──────────────────────┘
```

---

## XI. PACKAGE DIAGRAM

```
┌─────────────────────────────────────────────────────┐
│           AI Summary Project Package                │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │         Presentation Package                 │  │
│  │              (main.py)                       │  │
│  │                                              │  │
│  │  ┌────────────────────────────────────────┐ │  │
│  │  │ AISummaryApp                           │ │  │
│  │  │ - Tkinter GUI Components               │ │  │
│  │  │ - Event Handlers                       │ │  │
│  │  │ - UI Logic                             │ │  │
│  │  └────────────────────────────────────────┘ │  │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│                 │ imports                          │
│                 ▼                                   │
│  ┌──────────────────────────────────────────────┐  │
│  │      Business Logic Package                 │  │
│  │                                              │  │
│  │  ┌────────────────────────────────────────┐ │  │
│  │  │ FileReader (file_reader.py)            │ │  │
│  │  │ - read_txt()                           │ │  │
│  │  │ - read_pdf()                           │ │  │
│  │  │ - read_docx()                          │ │  │
│  │  └────────────────────────────────────────┘ │  │
│  │                                              │  │
│  │  ┌────────────────────────────────────────┐ │  │
│  │  │ AISummarizer (ai_summarizer.py)        │ │  │
│  │  │ - summarize()                          │ │  │
│  │  │ - summarize_with_bullet_points()       │ │  │
│  │  │ - Model Management                     │ │  │
│  │  └────────────────────────────────────────┘ │  │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│                 │ imports                          │
│                 ▼                                   │
│  ┌──────────────────────────────────────────────┐  │
│  │    External Libraries Package                │  │
│  │                                              │  │
│  │  ┌────────────────────────────────────────┐ │  │
│  │  │ ollama - Ollama Python Client          │ │  │
│  │  │ PyPDF2 - PDF Processing                │ │  │
│  │  │ python-docx - DOCX Processing          │ │  │
│  │  │ tkinter - GUI Framework                │ │  │
│  │  │ threading - Multi-threading            │ │  │
│  │  └────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────┘  │
│                 │                                   │
│                 │ calls                            │
│                 ▼                                   │
│  ┌──────────────────────────────────────────────┐  │
│  │     Ollama External Service                  │  │
│  │                                              │  │
│  │  HTTP API: localhost:11434                  │  │
│  │  - /api/chat                                │  │
│  │  - /api/generate                            │  │
│  │  - /api/pull (model management)             │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## XII. BẢNG TÓM TẮT

### **Các Class Chính**

| Class | Mục đích | File | Methods |
|-------|---------|------|---------|
| **FileReader** | Đọc file | file_reader.py | read_txt, read_pdf, read_docx, read_file |
| **AISummarizer** | Tóm tắt AI | ai_summarizer.py | summarize, summarize_with_bullet_points, set_model, get_available_models |
| **AISummaryApp** | Giao diện | main.py | create_widgets, select_file, summarize_file, perform_summarization, update_progress |

### **Mối Quan Hệ**

| From | To | Loại | Mô tả |
|------|-----|------|-------|
| AISummaryApp | FileReader | Uses | Gọi để đọc file |
| AISummaryApp | AISummarizer | Uses | Gọi để tóm tắt |
| AISummarizer | Ollama API | Calls | Gửi request tóm tắt |
| FileReader | File System | Access | Đọc file từ disk |

### **Data Flow**

```
User Input
    ↓
Select File → Read File → Get Content
    ↓
Select Model & Type
    ↓
Create Prompt
    ↓
Send to Ollama
    ↓
Process (AI)
    ↓
Get Summary
    ↓
Display Results
```

---

Đây là mô hình hoàn chỉnh về class diagram, ER diagram, use case, sequence diagram, state diagram, component diagram, deployment diagram, và package diagram của hệ thống AI Summary.
