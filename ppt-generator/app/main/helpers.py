import os
from typing import Dict, Any, Tuple

def validate_request(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validasi input JSON dari request API."""
    if not data:
        return False, "Request body tidak boleh kosong"
    if "company" not in data or not data["company"]:
        return False, "Field 'company' wajib diisi"
    if "slideCount" in data:
        try:
            slide_count = int(data["slideCount"])
            if slide_count <= 0:
                return False, "slideCount harus lebih dari 0"
        except ValueError:
            return False, "slideCount harus angka"
    return True, ""


def create_output_dir(dirname: str) -> str:
    """Bikin folder output kalau belum ada."""
    path = os.path.join(os.getcwd(), dirname)
    os.makedirs(path, exist_ok=True)
    return path
