import os
from docxtpl import DocxTemplate

template_path = os.environ.get("TEMPLATE_PATH", "templates/Service_Validation_And_Testing_TEMPLATE.docx")
output_path = os.environ.get("OUTPUT_PATH", "Service_Validation_And_Testing_DRAFT.docx")
chg_number = os.environ["CHG_NUMBER"]
chg_description = os.environ.get("CHG_DESCRIPTION", "Standard Change")
backend_scope = os.environ.get("BACKEND_SCOPE", "N/A")
data_scope = os.environ.get("DATA_SCOPE", "N/A")
frontend_scope = os.environ.get("FRONTEND_SCOPE", "N/A")

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

