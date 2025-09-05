import os
import asyncio
from pathlib import Path
from markitdown import MarkItDown
from app.tools.base import CustomBaseTool

class PDFConverterTool(CustomBaseTool):
    name: str = "pdf_to_markdown_converter"
    description: str = (
        "Use this tool to convert a PDF file (like a CV) to Markdown format text. "
        "Input must be the absolute path to the PDF."
    )

    def _convert_pdf_sync(self, pdf_path: str) -> str:
        if not os.path.exists(pdf_path):
            return f"❌ Error: PDF file not found at '{pdf_path}'"
        try:
            result = MarkItDown().convert(pdf_path)
            markdown = getattr(result, "text_content", None) or str(result)
            return markdown.strip() or "⚠️ No text was extracted from the PDF."
        except Exception as e:
            return f"❌ Error during PDF to Markdown conversion: {e}"

    def _run(self, pdf_path: str) -> str:
        return self._convert_pdf_sync(pdf_path)

    async def _arun(self, pdf_path: str) -> str:
        return await asyncio.to_thread(self._convert_pdf_sync, pdf_path)
