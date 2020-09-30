from abc import ABC, abstractmethod
from fileinput import FileInput
import uuid
from werkzeug.utils import secure_filename


class Storage(ABC):
    @abstractmethod
    def save_file(self, file: FileInput) -> str:
        pass

    def get_secure_filename(self, filename: str):
        return secure_filename(f"{uuid.uuid4().hex}_{filename}")
