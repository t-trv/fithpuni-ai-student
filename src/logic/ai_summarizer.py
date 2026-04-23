"""
Module xử lý AI Summarization sử dụng Ollama
"""

import ollama


class AISummarizer:
    """Class xử lý summarization với Ollama"""

    def __init__(self, model_name="llama3.2:1b"):
        """
        Khởi tạo AI Summarizer

        Args:
            model_name (str): Tên model Ollama (mặc định: llama3.2:1b)
        """
        self.model_name = model_name
        self.available_models = [
            "tinyllama:latest",
            "llama3.2:1b",
            "gpt-oss:20b",
            "mistral:latest",
            "gemma3:4b"
        ]

    def set_model(self, model_name):
        """
        Thay đổi model

        Args:
            model_name (str): Tên model mới
        """
        self.model_name = model_name

    def get_available_models(self):
        """
        Lấy danh sách các model có sẵn

        Returns:
            list: Danh sách tên model
        """
        return self.available_models

    def summarize(self, text, max_length=5000):
        """
        Tóm tắt văn bản sử dụng Ollama

        Args:
            text (str): Văn bản cần tóm tắt
            max_length (int): Độ dài tóm tắt tối đa (mặc định: 5000 từ)

        Returns:
            str: Văn bản đã được tóm tắt
        """
        try:
            # Tạo prompt cho AI
            prompt = f"""Bạn là một trợ lý AI chuyên tóm tắt văn bản. 
Hãy đọc văn bản dưới đây và tạo một bản tóm tắt, không quá {max_length} từ. 
Nhưng cũng đừng ngắn quá, ít nhất phải 500 từ trở lên trừ khi văn bản quá ngắn.
Đối với tóm tắt thường, ít nhất phải ít nhất phải dài hơn 20% so với văn bản gốc.
Đối với tóm tắt điểm chính (bullet points), hãy cung cấp từ 5 đến 10 điểm chính.
Tóm tắt bằng tiếng Việt nếu văn bản gốc là tiếng Việt, hoặc bằng tiếng Anh nếu văn bản gốc là tiếng Anh.
Chỉ trả về phần tóm tắt, không thêm lời giải thích.

Văn bản cần tóm tắt:
{text}

Tóm tắt:"""

            # Gọi Ollama API
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )

            # Lấy kết quả
            summary = response['message']['content']
            return summary.strip()

        except Exception as e:
            raise Exception(f"Lỗi khi tóm tắt với Ollama: {str(e)}")

    def summarize_with_bullet_points(self, text):
        """
        Tóm tắt văn bản dưới dạng các điểm chính (bullet points)

        Args:
            text (str): Văn bản cần tóm tắt

        Returns:
            str: Các điểm chính của văn bản
        """
        try:
            prompt = f"""Bạn là một trợ lý AI chuyên tóm tắt văn bản.
Hãy đọc văn bản dưới đây và liệt kê các ý chính dưới dạng bullet points (5-10 điểm).
Trả lời bằng tiếng Việt nếu văn bản gốc là tiếng Việt, hoặc bằng tiếng Anh nếu văn bản gốc là tiếng Anh.

Văn bản:
{text}

Các điểm chính:"""

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )

            summary = response['message']['content']
            return summary.strip()

        except Exception as e:
            raise Exception(f"Lỗi khi tóm tắt với Ollama: {str(e)}")
