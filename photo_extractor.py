import subprocess
import json

def extract_metadata_with_exiftool(file_path):
    try:
        result = subprocess.run(
            ["exiftool", "-json", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        metadata = json.loads(result.stdout)[0]

        extracted = {
            "filename": metadata.get("FileName"),
            "creation_time": metadata.get("CreateDate") or metadata.get("DateTimeOriginal"),
            "location": {
                "latitude": metadata.get("GPSLatitude"),
                "longitude": metadata.get("GPSLongitude")
            } if metadata.get("GPSLatitude") and metadata.get("GPSLongitude") else None
        }

        return extracted

    except subprocess.CalledProcessError as e:
        print("ExifTool error:", e.stderr.decode())
        return None

# Example usage
photo_file = "IMG_3127.HEIC"
metadata = extract_metadata_with_exiftool(photo_file)
print(json.dumps(metadata, indent=4))