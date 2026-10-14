import os
import json
import logging
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from dotenv import load_dotenv
from prompt import extract_invoice_json

load_dotenv()

pdf_path=os.getenv("PDF_PATH")
output_txt_path=os.getenv("OUTPUT_TXT_PATH")
output_json_path=os.getenv("OUTPUT_JSON_PATH")

#logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("ocr_errors.log", encoding="utf-8"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)


#logging

try:
    if not pdf_path or not output_txt_path:
        raise ValueError("Error : PDF_PATH or OUTPUT_TXT_PATH not found in .env file")

    reader = PdfReader(pdf_path)

    full_text=[]

    for index, page in enumerate(reader.pages):
        try:
            text=page.extract_text()
        except Exception:
            logger.exception(
                "text extraction failed on page %s", index)
            continue
        if text:
            full_text.append(f"---Page{index+1}---\n"+ text)

    if not full_text:
        raise ValueError("No extractable text foun in the pdf")

    with open(output_txt_path,"w",encoding="utf-8") as txt_file:
        txt_file.write("\n\n".join(full_text))

    print(f"Sucessfully extracted text to {output_txt_path}")


    output_dir=os.path.dirname(output_txt_path)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok= True)


    with open(output_txt_path,"r",encoding="utf-8") as txt_file:
        invoice_text= txt_file.read()

    invoice_data = extract_invoice_json(invoice_text)

    json_dir = os.path.dirname(output_json_path)
    if json_dir:
        os.makedirs(json_dir,exist_ok=True)

    with open(output_json_path,"w",encoding="utf-8") as json_file:
        json.dump(
            invoice_data,
            json_file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Successfully extracted invoice JSON to {output_json_path}")

except FileNotFoundError:
    logger.exception("input PDF file not found")
    raise
except PdfReadError:
    logger.exception("PDF cannot be read")
    raise

except Exception:
    logger.exception("Unexpected PDF processing failure")
    raise


