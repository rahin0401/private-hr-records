import subprocess

print("=" * 50)
print("Reset Development Environment")
print("=" * 50)

print("Purging Celery queue...")

subprocess.run(
    "celery -A config purge -f",
    shell=True,
)

print("Flushing Redis cache...")

subprocess.run(
    r'"C:\Program Files\Memurai\memurai-cli.exe" FLUSHALL',
    shell=True,
)

print("\nReset completed.")
