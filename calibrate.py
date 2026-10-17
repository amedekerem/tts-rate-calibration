import asyncio
import csv
from pathlib import Path
import edge_tts
from mutagen.mp3 import MP3

VOICE = "en-US-AriaNeural"
CSV_FILENAME = "edge-tts Speaking-Rate Calibration Passages.csv"


def find_csv_file() -> Path:
    local_path = Path(CSV_FILENAME)
    if local_path.exists():
        return local_path
    parent_path = Path(__file__).resolve().parent.parent / CSV_FILENAME
    if parent_path.exists():
        return parent_path
    raise FileNotFoundError(f"Could not find '{CSV_FILENAME}'")


async def main() -> None:
    csv_path = find_csv_file()
    wps_values: list[float] = []

    with csv_path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if not row:
                continue
            passage_id = row[0].strip()
            try:
                passage_text = row[1]
                mp3_filename = f"{passage_id}.mp3"

                communicate = edge_tts.Communicate(passage_text, VOICE)
                await communicate.save(mp3_filename)

                audio = MP3(mp3_filename)
                seconds = audio.info.length
                word_count = len(passage_text.split(" "))
                wps = word_count / seconds
                wps_values.append(wps)

                print(f"{passage_id}, {word_count}, {seconds:.2f}, {wps:.2f}")
            except Exception as e:
                print(f"{passage_id}: Error - {e}")

    if wps_values:
        avg_wps = sum(wps_values) / len(wps_values)
        print(f"Average words per second: {avg_wps:.2f}")
    else:
        print("Average words per second: N/A (no passages succeeded)")


if __name__ == "__main__":
    asyncio.run(main())
