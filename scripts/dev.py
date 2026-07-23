import os
import subprocess
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"

# Change this if your RabbitMQ sbin folder is different
RABBITMQ_SBIN = Path(r"C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin")

processes = []


def run(title, command, cwd=None):
    print(f"Starting {title}...")

    p = subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )

    processes.append((title, p))


def rabbitmq_running():
    try:
        result = subprocess.run(
            "rabbitmqctl.bat status",
            cwd=RABBITMQ_SBIN,
            shell=True,
            capture_output=True,
            text=True,
        )

        return result.returncode == 0

    except Exception:
        return False


def start_rabbitmq():

    if rabbitmq_running():
        print("RabbitMQ already running.")
        return

    print("Starting RabbitMQ...")

    subprocess.Popen(
        "rabbitmq-server.bat",
        cwd=RABBITMQ_SBIN,
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )

    print("Waiting for RabbitMQ...")
    time.sleep(10)


def shutdown(sig=None, frame=None):

    print("\nStopping all processes...")

    for name, p in processes:
        try:
            p.terminate()
        except Exception:
            pass

    print("Done.")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)

print("=" * 50)
print(" HR Project Development Environment")
print("=" * 50)

start_rabbitmq()

run(
    "Django",
    "python manage.py runserver",
    cwd=BACKEND,
)

run(
    "Celery Worker",
    "celery -A config worker -P solo -l info",
    cwd=BACKEND,
)

run(
    "Celery Beat",
    "celery -A config beat -l info",
    cwd=BACKEND,
)

run(
    "React",
    "npm run dev",
    cwd=FRONTEND,
)

print("\nEverything started.")
print("Press CTRL+C to stop everything.")

while True:
    time.sleep(1)