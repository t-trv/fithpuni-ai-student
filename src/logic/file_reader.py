"""
Module đọc nội dung từ các loại file khác nhau (.txt, .pdf, .docx)
"""

import PyPDF2
from docx import Document


class FileReader:
    """Class xử lý đọc nội dung từ các loại file"""

    @staticmethod
    def read_txt(file_path):
        """
        Đọc file .txt

        Args:
            file_path (str): Đường dẫn đến file .txt

        Returns:
            str: Nội dung của file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            raise Exception(f"Lỗi khi đọc file TXT: {str(e)}")

    @staticmethod
    def read_pdf(file_path):
        """
        Đọc file .pdf

        Args:
            file_path (str): Đường dẫn đến file .pdf

        Returns:
            str: Nội dung của file
        """
        try:
            content = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                # Đọc từng trang
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    content += page.extract_text() + "\n"

            return content
        except Exception as e:
            raise Exception(f"Lỗi khi đọc file PDF: {str(e)}")

    @staticmethod
    def read_docx(file_path):
        """
        Đọc file .docx

        Args:
            file_path (str): Đường dẫn đến file .docx

        Returns:
            str: Nội dung của file
        """
        try:
            doc = Document(file_path)
            content = ""

            # Đọc từng paragraph
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"

            return content
        except Exception as e:
            raise Exception(f"Lỗi khi đọc file DOCX: {str(e)}")

    @staticmethod
    def read_file(file_path):
        """
        Đọc file dựa trên extension

        Args:
            file_path (str): Đường dẫn đến file

        Returns:
            str: Nội dung của file
        """
        file_path_lower = file_path.lower()

        if file_path_lower.endswith('.txt'):
            return FileReader.read_txt(file_path)
        elif file_path_lower.endswith('.pdf'):
            return FileReader.read_pdf(file_path)
        elif file_path_lower.endswith('.docx'):
            return FileReader.read_docx(file_path)
        else:
            raise Exception(
                "Định dạng file không được hỗ trợ. Chỉ hỗ trợ .txt, .pdf, .docx")
