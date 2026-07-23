import os
import subprocess

SERVICES = [
    "python.exe",
    "node.exe",
    "celery.exe",
]

print("=" * 50)
print("Stopping Development Environment")
print("=" * 50)

for process in SERVICES:
    subprocess.run(
        f'taskkill /F /IM "{process}"',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

print("Stopped Django")
print("Stopped React")
print("Stopped Celery")

choice = input("Stop RabbitMQ too? (y/n): ").lower()

if choice == "y":
    subprocess.run(
        r'"C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin\rabbitmqctl.bat" stop',
        shell=True,
    )

print("\nDone.")