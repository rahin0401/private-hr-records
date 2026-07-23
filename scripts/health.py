import subprocess

print("=" * 60)
print("HR Project Health Check")
print("=" * 60)


def check(title, command):

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"[ OK ] {title}")
    else:
        print(f"[FAIL] {title}")


check(
    "RabbitMQ",
    r'"C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin\rabbitmqctl.bat" status',
)

check(
    "Redis (Memurai)",
    r'"C:\Program Files\Memurai\memurai-cli.exe" ping',
)

check(
    "Node",
    "node -v",
)

check(
    "Python",
    "python --version",
)

check(
    "Celery",
    "celery --version",
)

check(
    "Git",
    "git --version",
)

print("=" * 60)
print("Health check completed.")