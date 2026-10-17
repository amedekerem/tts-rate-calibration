import asyncio
import edge_tts
from mutagen.mp3 import MP3

VOICE = "en-US-AriaNeural"
TEXT = "Hello! This is a test of the Edge TTS rate calibration setup."
OUTPUT_FILE = "output.mp3"


async def main() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

    audio = MP3(OUTPUT_FILE)
    print(f"Saved {OUTPUT_FILE} using voice '{VOICE}' (Duration: {audio.info.length:.2f}s)")


if __name__ == "__main__":
    asyncio.run(main())
