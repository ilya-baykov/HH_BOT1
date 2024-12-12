from typing import Optional

import pdfplumber
from config.logger import logger


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
            logger.error(f"Ошибка при извлечении текста: {e}")
            return None
        return text
