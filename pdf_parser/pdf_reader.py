from typing import Optional

import pdfplumber


class PDFTextExtractor:
    """Класс для извлечения текста из PDF файла."""

    @staticmethod
    def get_text(pdf_path: str) -> Optional[str]:
        """Извлекает текст из PDF файла."""
        text = ''
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:  # Проверяем, что текст был извлечен
                        text += page_text + '\n'
        except Exception as e:
            print(f"Ошибка при извлечении текста: {e}")
            return None
        return text


# Пример использования

pdf_path = r"C:\Users\ilyab\PycharmProjects\HH_BOT_1\pdf_parser\Руководитель проекта, исполнительный директор.pdf"
extractor = PDFTextExtractor()
extracted_text = extractor.get_text(pdf_path)
print(extracted_text)
