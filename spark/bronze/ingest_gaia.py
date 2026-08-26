import subprocess
import sys

# Local Gaia files mounted inside the NameNode container
LOCAL_GAIA_DIR = "/data/batch/gaia"

# HDFS Bronze destination
HDFS_DIR = "/bronze/source=gaia/year=2026/month=08"

SUCCESS_MARKER = f"{HDFS_DIR}/_SUCCESS"


def hdfs_command(command):
    """Execute an HDFS command inside the NameNode container."""
    full_command = [
        "docker",
        "exec",
        "namenode",
        "hdfs",
        "dfs"
    ] + command

    return subprocess.run(
        full_command,
        text=True,
        capture_output=True
    )


print("======================================")
print("🌌 GAIA → BRONZE")
print("======================================")

# -------------------------------------------------
# 1. Check _SUCCESS
# -------------------------------------------------

check_success = hdfs_command([
    "-test",
    "-e",
    SUCCESS_MARKER
])

if check_success.returncode == 0:
    print("✅ Batch already ingested.")
    print("✅ _SUCCESS exists.")
    sys.exit(0)


# -------------------------------------------------
# 2. Create Bronze directory
# -------------------------------------------------

print("📁 Creating HDFS Bronze directory...")

result = hdfs_command([
    "-mkdir",
    "-p",
    HDFS_DIR
])

if result.returncode != 0:
    print("❌ Error creating HDFS directory:")
    print(result.stderr)
    sys.exit(1)


# -------------------------------------------------
# 3. Upload raw Gaia files
# -------------------------------------------------

print("📦 Uploading raw Gaia files...")

upload_command = [
    "docker",
    "exec",
    "namenode",
    "sh",
    "-c",
    f"hdfs dfs -put -f "
    f"{LOCAL_GAIA_DIR}/*.csv.gz "
    f"{HDFS_DIR}/"
]

upload = subprocess.run(upload_command)

if upload.returncode != 0:
    print("❌ Gaia upload failed.")
    sys.exit(1)


# -------------------------------------------------
# 4. Create _SUCCESS marker
# -------------------------------------------------

print("✅ Creating _SUCCESS marker...")

success = hdfs_command([
    "-touchz",
    SUCCESS_MARKER
])

if success.returncode != 0:
    print("❌ Could not create _SUCCESS")
    print(success.stderr)
    sys.exit(1)


print()
print("======================================")
print("✅ GAIA BRONZE INGESTION COMPLETE")
print(f"📁 HDFS: {HDFS_DIR}")
print("✅ Raw .csv.gz files preserved")
print("✅ _SUCCESS created")
print("======================================")