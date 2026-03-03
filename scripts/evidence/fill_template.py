import os
import sys
from docxtpl import DocxTemplate
from evidence.constants import *

def main():
    try:
        template_path = os.environ.get("TEMPLATE_PATH", DEFAULT_TEMPLATE_PATH)
        output_path = os.environ.get("OUTPUT_PATH", DEFAULT_OUTPUT_PATH)
        chg_number = os.environ["CHG_NUMBER"]
        chg_description = os.environ.get("CHG_DESCRIPTION", DEFAULT_CHG_DESCRIPTION)
        backend_scope = os.environ.get("BACKEND_SCOPE", DEFAULT_SCOPE)
        data_scope = os.environ.get("DATA_SCOPE", DEFAULT_SCOPE)
        frontend_scope = os.environ.get("FRONTEND_SCOPE", DEFAULT_SCOPE)

        context = {
            "chg_number": chg_number,
            "chg_description": chg_description,
            "backend_scope": backend_scope,
            "data_scope": data_scope,
            "frontend_scope": frontend_scope,
        }

        doc = DocxTemplate(template_path)
        doc.render(context)
        doc.save(output_path)
        print(f"Generated: {output_path}")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

