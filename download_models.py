from modelscope import snapshot_download

mineru_patterns = [
    "models/Layout/LayoutLMv3/*",
    "models/Layout/YOLO/*",
    "models/MFD/YOLO/*",
    "models/MFR/unimernet_small/*",
    "models/TabRec/TableMaster/*",
    "models/TabRec/StructEqTable/*",
]
model_dir = snapshot_download(
    "opendatalab/PDF-Extract-Kit",
    local_dir="/root/PDF-Extract-Kit",
    allow_patterns=mineru_patterns,
)
layoutreader_model_dir = snapshot_download(
    "ppaanngggg/layoutreader", local_dir="/root/layoutreader"
)
