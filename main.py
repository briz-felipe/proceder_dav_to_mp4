import os
from pathlib import Path
import subprocess
import asyncio
from datetime import datetime
import cv2
import pandas as pd
import platform
import sys

async def check_and_install_ffmpeg():
    """Checks if ffmpeg is installed and installs it if not."""
    try:
        process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-version',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        await process.communicate()
        if process.returncode != 0:
            raise FileNotFoundError
        return True
    except FileNotFoundError:
        print("FFmpeg not found. Attempting to install...")
        
        try:
            if platform.system() == "Windows":
                # For Windows, we can use chocolatey or download manually
                print("Please install FFmpeg on Windows using one of these methods:")
                print("1. Using Chocolatey: 'choco install ffmpeg' (run as admin)")
                print("2. Download from https://ffmpeg.org/download.html")
            elif platform.system() == "Linux":
                # For Linux (Debian/Ubuntu)
                process = await asyncio.create_subprocess_shell(
                    'sudo apt-get install -y ffmpeg',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                if process.returncode == 0:
                    print("FFmpeg installed successfully")
                    return True
                else:
                    print("Failed to install FFmpeg:", stderr.decode())
            elif platform.system() == "Darwin":  # macOS
                process = await asyncio.create_subprocess_shell(
                    'brew install ffmpeg',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                if process.returncode == 0:
                    print("FFmpeg installed successfully")
                    return True
                else:
                    print("Failed to install FFmpeg:", stderr.decode())
        except Exception as e:
            print(f"Error installing FFmpeg: {str(e)}")
        
        print("FFmpeg installation failed. Please install it manually.")
        sys.exit(1)

async def validate_and_create_paths(input_path: str, output_path: str) -> tuple[Path, Path]:
    """Validates and converts input/output paths to Path objects, creating directories if needed."""
    input_path_obj = Path(input_path)
    output_path_obj = Path(output_path)
    
    if not input_path_obj.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_path}")
    
    if not input_path_obj.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_path}")
    
    # Create output directory if it doesn't exist
    output_path_obj.mkdir(parents=True, exist_ok=True)
    
    # Create img directory for thumbnails if it doesn't exist
    img_dir = output_path_obj.parent / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    
    return input_path_obj, output_path_obj

async def mp4_to_jpg(file_path: Path, output_dir: Path):
    """Extracts a frame from MP4 and saves as JPG in the specified directory."""
    vidcap = cv2.VideoCapture(str(file_path))
    success, image = vidcap.read()
    if not success:
        raise RuntimeError(f"Could not read video file: {file_path}")
    
    img_dir = output_dir.parent / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    path_str = str(img_dir / f"{file_path.stem}.jpg")
    cv2.imwrite(path_str, image)
    return path_str

async def mp4_duration(file_path: Path):
    """Calculates duration of MP4 file."""
    vidcap = cv2.VideoCapture(str(file_path))
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    return duration_str

async def convert_dav_to_mp4(input_file: Path, output_file: Path):
    """Converts a .dav video file to .mp4 using ffmpeg asynchronously."""
    try:
        command = [
            'ffmpeg',
            '-i', str(input_file),
            '-codec', 'copy',
            str(output_file)
        ]

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            file_size = os.path.getsize(output_file)
            file_size = f"{file_size / (1024 * 1024):.2f} MB"
            # path_jpg = await mp4_to_jpg(output_file, output_file.parent)
            duration = await mp4_duration(output_file)
            
            # Parse file name components
            parts = output_file.stem.split('-')
            if len(parts) >= 4:
                origem = parts[0]
                chanel = parts[1]
                camera = parts[2]
                final_gravacao = '-'.join(parts[3:])
            else:
                origem = "unknown"
                chanel = "unknown"
                camera = "unknown"
                final_gravacao = output_file.stem
                
            public_link = f"http://yourserver.com/{output_file}"
            return {
                "origem": origem,
                "chanel": chanel,
                "camera": camera,
                "final_gravacao": final_gravacao,
                "duration": duration,
                "file_size": file_size
            }
        else:
            print(f"Error converting {input_file}:")
            print(stderr.decode())
            return None

    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return None

async def dav_to_mp4(input_path: str, output_path: str):
    """Main function to convert DAV videos to MP4."""
    await check_and_install_ffmpeg()
    
    try:
        input_path_obj, output_path_obj = await validate_and_create_paths(input_path, output_path)
    except Exception as e:
        print(f"Error with paths: {str(e)}")
        return []
    
    print('\nStarting conversion...')
    startat = datetime.now()
    print(f"Start at: {startat.strftime('%X')}")
    
    dav_videos = [x for x in input_path_obj.iterdir() if x.suffix == '.dav']
    if not dav_videos:
        print("No .dav files found in input directory")
        return []
    
    tasks = [
        convert_dav_to_mp4(
            dav_video, 
            output_path_obj / f"{dav_video.stem}.mp4"
        ) 
        for dav_video in dav_videos
    ]
    
    response = await asyncio.gather(*tasks)
    response = [r for r in response if r is not None]  # Filter out failed conversions
    
    endat = datetime.now()
    print(f"End at: {endat.strftime('%X')}")
    print(f"Total time: {endat - startat}")
    print(f"Converted {len(response)} files")
    
    return response

if __name__ == "__main__":
    input_path = 'input_videos'
    output_path = 'output_videos'
    
    # Create directories if they don't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    response = asyncio.run(dav_to_mp4(
        input_path=input_path,
        output_path=output_path
    ))
    
    if response:
        df = pd.DataFrame(response)
        try:
            df['final_gravacao'] = pd.to_datetime(df['final_gravacao'], format='%Y-%m-%d-%H-%M-%S')
            df = df.sort_values(by=['camera', 'chanel', 'final_gravacao'])
            print(df)
            df.to_csv("output_videos.csv", index=False)
        except Exception as e:
            print(f"Error processing results: {str(e)}")
            df.to_csv("output_videos.csv", index=False)