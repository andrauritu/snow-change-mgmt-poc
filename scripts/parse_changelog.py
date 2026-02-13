import os

#for now i will just output N/A for all scope fields but normally we would take it from changelog
backend_scope = "N/A"
data_scope = "N/A"
frontend_scope = "N/A"

version = os.environ.get("VERSION", "unknown")

github_output = os.environ.get("GITHUB_OUTPUT")
if github_output:
    with open(github_output, "a") as f:
        f.write(f"backend_scope={backend_scope}\n")
        f.write(f"data_scope={data_scope}\n")
        f.write(f"frontend_scope={frontend_scope}\n")
