import os
from pathlib import Path
from uuid import uuid4

import magic_pdf.model as model_config
from fastapi import APIRouter, File, HTTPException, UploadFile
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
from pydantic import BaseModel

from .office_converter import OfficeConverter, OfficeExts

parse_router = APIRouter()

class ParseResponse(BaseModel):
    content: str


_tmp_dir = "/tmp/{uuid}"
_local_image_dir = "/tmp/{uuid}/images"
model_config.__use_inside_model__ = True
model_config.__model_mode__ = "full"


@parse_router.post("/parse", response_model=ParseResponse)
async def parse(file: UploadFile = File(...)):
    pdf_bytes = None
    uuid_str = str(uuid4())
    tmp_dir = _tmp_dir.format(uuid=uuid_str)
    local_image_dir = _local_image_dir.format(uuid=uuid_str)
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(local_image_dir, exist_ok=True)
    if file.filename.endswith(OfficeExts.__args__):
        contents = await file.read()
        input_file: Path = Path(tmp_dir) / file.filename
        input_file.write_bytes(contents)
        output_file: Path = Path(tmp_dir) / os.path.splitext(file.filename)[0] + ".pdf"
        office_converter = OfficeConverter()
        office_converter.convert(input_file, output_file)
        pdf_bytes = output_file.read_bytes()
    elif file.filename.endswith(".pdf"):
        pdf_bytes = await file.read()
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    image_writer = DiskReaderWriter(local_image_dir)
    jso_useful_key = {"_pdf_type": "", "model_list": []}
    pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer, is_debug=True)
    pipe.pipe_classify()
    pipe.pipe_analyze()
    pipe.pipe_parse()
    md_content = pipe.pipe_mk_markdown(local_image_dir, drop_mode="none")
    return ParseResponse(content=md_content)
