import os
import logging
from datetime import datetime


log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(os.getcwd(),"logs",log_file)

# Ensure the log directory exists
os.makedirs(log_path, exist_ok=True)
log_file_path=os.path.join(log_path, log_file)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s"
)
# ...existing code...