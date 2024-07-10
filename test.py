import os
import time
import subprocess
import requests

# 配置
STREAM_URL = "udp://192.168.1.3:1234"
OUTPUT_DIR = "C:\\Users\\17719\\Downloads"
RECORD_DURATION = "00:01:00"  # 录制时长
CHECK_INTERVAL = 10  # 检查间隔（秒）
MAX_RETRIES = 5  # 最大重试次数
FFMPEG_PATH = "D:\\work\\ffmpeg\\bin\\ffmpeg.exe"  # FFmpeg的完整路径

def save_stream(url, output_file, duration):
    ffmpeg_command = [
        FFMPEG_PATH,
        "-i", url,
        "-t", duration,
        "-c", "copy",
        output_file
    ]
    subprocess.run(ffmpeg_command)

def main():
    while True:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"output_{timestamp}.mp4")
        retry_count = 0

        while retry_count < MAX_RETRIES:
            print(f"Attempting to save stream to {output_file}, try {retry_count + 1} of {MAX_RETRIES}")
            result = subprocess.run([FFMPEG_PATH, "-i", STREAM_URL, "-t", RECORD_DURATION, "-c", "copy", output_file], stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(f"Stream saved successfully to {output_file}")
                break
            else:
                print(f"Error saving stream: {result.stderr.decode()}")
                retry_count += 1
                time.sleep(CHECK_INTERVAL)

        if retry_count == MAX_RETRIES:
            print(f"Failed to save stream after {MAX_RETRIES} attempts")

        print(f"Waiting {CHECK_INTERVAL} seconds before next check...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
