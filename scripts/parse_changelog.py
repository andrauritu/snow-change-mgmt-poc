
from sn_client import set_output

# for now i will just output N/A for all scope fields but normally we would take it from changelog
backend_scope = "N/A"
data_scope = "N/A"
frontend_scope = "N/A"

set_output("backend_scope", backend_scope)
set_output("data_scope", data_scope)
set_output("frontend_scope", frontend_scope)
