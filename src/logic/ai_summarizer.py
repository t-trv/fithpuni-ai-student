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

    def summarize(self, text, max_length=500):
        """
        Tóm tắt văn bản sử dụng Ollama

        Args:
            text (str): Văn bản cần tóm tắt
            max_length (int): Độ dài tóm tắt mong muốn (mặc định: 500 từ)

        Returns:
            str: Văn bản đã được tóm tắt
        """
        try:
            word_count = len(text.split())

            # Điều chỉnh độ dài target dựa trên văn bản gốc
            if word_count < 200:
                target_length = word_count
            elif word_count < 500:
                target_length = min(200, word_count // 2)
            elif word_count < 1000:
                target_length = min(300, word_count // 3)
            else:
                target_length = min(max_length, word_count // 4)

            prompt = f"""Bạn là một chuyên gia soạn thảo văn bản. Nhiệm vụ của bạn là viết bản tóm tắt CHUYÊN NGHIỆP từ văn bản cho sẵn.

QUY TẮC NGHIÊM NGẶT:
1. Viết bản tóm tắt khoảng {target_length} từ, đủ dài để nắm bắt ý chính
2. Viết theo định dạng đoạn văn MẠCH LẠC, không dùng danh sách bullet points
3. KHÔNG VIẾT bất kỳ câu nào mang tính mô tả về bản tóm tắt (ví dụ: "Bản tóm tắt này...", "Tóm lại...", "Như đã nêu trên...")
4. KHÔNG THÊM lời kết thúc như "Bản tóm tắt có..." hoặc bất kỳ dòng mô tả nào về độ dài, chất lượng
5. Chỉ viết nội dung tóm tắt thuần túy, đi thẳng vào vấn đề
6. Dùng tiếng Việt, viết tự nhiên như đang viết văn

VĂN BẢN GỐC:
{text}

BẢN TÓM TẮT:"""

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
            prompt = f"""Bạn là một chuyên gia tóm tắt văn bản. Nhiệm vụ của bạn là trích xuất các ý chính quan trọng nhất từ văn bản.

QUY TẮC NGHIÊM NGẶT:
1. Liệt kê TỪ 5 ĐẾN 10 điểm chính quan trọng nhất
2. Mỗi điểm viết NGẮN GỌN (1-2 dòng), dùng dấu • ở đầu
3. KHÔNG có tiêu đề như "Các điểm chính:", "Tóm tắt:", hay bất kỳ lời mở đầu nào
4. BẮT ĐẦU NGAY bằng bullet point đầu tiên
5. Ưu tiên: quyết định, mục tiêu, lợi ích, chi phí, thông tin quan trọng
6. Dùng tiếng Việt

VĂN BẢN:
{text}"""

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
