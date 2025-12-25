# context.py
# System awareness for JARVIS (Windows compatible)

import platform
import socket
from datetime import datetime
import time
import sys


def get_system_context() -> str:
    """
    Collects system information and returns
    a formatted context string for the LLM.
    """

    now = datetime.now()
    formatted_time = now.strftime("%A, %d %B %Y, %I:%M %p")

    timezone = time.tzname[0]
    hostname = socket.gethostname()

    os_name = platform.system()
    os_version = platform.release()
    python_version = platform.python_version()

    context = f"""
SYSTEM STATUS:
- Date & Time : {formatted_time} ({timezone})
- Hostname    : {hostname}
- OS          : {os_name} {os_version}
- Python      : {python_version}

NOTE:
This information is factual and provided by the operating system.
"""

    return context.strip()
