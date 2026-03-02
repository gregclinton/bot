from pathlib import Path

# if we add a storage volume in runpod, it shows up as /workspace
# otherwise, in development, we'll just fall back to /tmp

root = Path("/workspace" if Path("/workspace").exists() else "/tmp")
