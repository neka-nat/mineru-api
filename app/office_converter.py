import os
from pathlib import Path
from typing import Literal

from gotenberg_client import GotenbergClient

OfficeExts = Literal[".docx", ".doc", ".odt", ".pptx", ".ppt", ".odp", ".xls", ".xlsx", ".ods"]


class OfficeConverter:
    def __init__(self, gotenberg_url: str | None = None, headers: dict[str, str] | None = None):
        if gotenberg_url is None:
            gotenberg_url = os.getenv("GOTENBERG_URL", "http://localhost:3500")
        self.gotenberg_url = gotenberg_url
        self.headers = headers

    def convert(self, office_file_path: Path | str, output_file_path: Path | str):
        if isinstance(office_file_path, str):
            office_file_path = Path(office_file_path)
        if isinstance(output_file_path, str):
            output_file_path = Path(output_file_path)
        with GotenbergClient(self.gotenberg_url) as client:
            if self.headers:
                client.add_headers(self.headers)
            with client.libre_office.to_pdf() as route:
                response = route.convert(office_file_path).run()
                output_file_path.write_bytes(response.content)

