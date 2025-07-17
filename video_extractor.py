import subprocess
import json

def extract_video_metadata_with_exiftool(file_path):
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
            "creation_time": (
                metadata.get("CreateDate") or
                metadata.get("MediaCreateDate") or
                metadata.get("TrackCreateDate") or
                metadata.get("DateTimeOriginal")
            ),
            "location": {
                "latitude": metadata.get("GPSLatitude"),
                "longitude": metadata.get("GPSLongitude")
            } if metadata.get("GPSLatitude") and metadata.get("GPSLongitude") else None
        }

        return extracted

    except subprocess.CalledProcessError as e:
        print("ExifTool error:", e.stderr.decode())
        return None
    except (IndexError, json.JSONDecodeError) as e:
        print("Parsing error:", str(e))
        return None

# Example usage
video_file = "IMG_3128.MOV"
metadata = extract_video_metadata_with_exiftool(video_file)
print(json.dumps(metadata, indent=4))
