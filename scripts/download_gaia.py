import os
import requests

BASE_URL = "https://cdn.gea.esac.esa.int/Gaia/gdr3/gaia_source/"
LIST_URL = BASE_URL + "_MD5SUM.txt"

OUTPUT_DIR = "data/batch/gaia"

TARGET_GB = 5
TARGET_BYTES = TARGET_GB * 1024**3

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🌌 Gaia DR3 downloader")
print(f"🎯 Target: {TARGET_GB} GB")

# --------------------------------------------------
# Get official Gaia file list
# --------------------------------------------------

print("📡 Getting official Gaia file list...")

response = requests.get(LIST_URL, timeout=60)
response.raise_for_status()

files = []

for line in response.text.splitlines():
    parts = line.strip().split()

    if len(parts) >= 2:
        filename = parts[-1]

        if filename.startswith("GaiaSource_") and filename.endswith(".csv.gz"):
            files.append(filename)

print(f"✅ Found {len(files)} Gaia files")

if not files:
    raise RuntimeError("No Gaia files found in _MD5SUM.txt")

# --------------------------------------------------
# Calculate already downloaded size
# --------------------------------------------------

current_size = 0

for filename in os.listdir(OUTPUT_DIR):
    path = os.path.join(OUTPUT_DIR, filename)

    if os.path.isfile(path):
        current_size += os.path.getsize(path)

print(f"💾 Already downloaded: {current_size / 1024**3:.2f} GB")

# --------------------------------------------------
# Download until we reach 5 GB
# --------------------------------------------------

for index, filename in enumerate(files, start=1):

    if current_size >= TARGET_BYTES:
        break

    output_path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(output_path):
        continue

    url = BASE_URL + filename

    print(f"\n⬇️ [{index}/{len(files)}] {filename}")

    try:

        with requests.get(url, stream=True, timeout=120) as r:

            r.raise_for_status()

            total = int(r.headers.get("content-length", 0))
            downloaded = 0

            with open(output_path, "wb") as f:

                for chunk in r.iter_content(chunk_size=1024 * 1024):

                    if not chunk:
                        continue

                    f.write(chunk)
                    downloaded += len(chunk)

                    if total > 0:
                        percent = downloaded / total * 100

                        print(
                            f"\r   {percent:5.1f}% | "
                            f"{downloaded / 1024**2:.1f} MB",
                            end=""
                        )

        file_size = os.path.getsize(output_path)
        current_size += file_size

        print(
            f"\n✅ File completed | "
            f"Total dataset: {current_size / 1024**3:.2f} GB"
        )

    except Exception as e:

        print(f"\n❌ Error downloading {filename}: {e}")

        # Remove incomplete file
        if os.path.exists(output_path):
            os.remove(output_path)

# --------------------------------------------------
# Finished
# --------------------------------------------------

print("\n" + "=" * 50)
print("🚀 GAIA DOWNLOAD COMPLETE")
print(f"📦 Total size: {current_size / 1024**3:.2f} GB")
print(f"📁 Location: {OUTPUT_DIR}")
print("=" * 50)