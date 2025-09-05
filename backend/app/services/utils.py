from pathlib import Path
from fastapi import UploadFile

def save_uploaded_file(uploaded_file: UploadFile, upload_dir: Path) -> Path:
    file_path = upload_dir / uploaded_file.filename
    with file_path.open("wb") as buffer:
        buffer.write(uploaded_file.file.read())
    return file_path
