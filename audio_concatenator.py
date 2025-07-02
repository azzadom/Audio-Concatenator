import os
import argparse
from pydub import AudioSegment
from pathlib import Path
import math

def get_audio_files(folder_path, supported_formats=None):
    """
    Gets all audio files from the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing audio files
        supported_formats (list): List of supported audio formats
    
    Returns:
        list: Sorted list of audio file paths
    """
    if supported_formats is None:
        supported_formats = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']
    
    audio_files = []
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"The folder {folder_path} does not exist")
    
    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in supported_formats:
            audio_files.append(str(file))
    
    # Sort files by name
    audio_files.sort()
    return audio_files

def concatenate_audio_files(file_list, output_path):
    """
    Concatenates a list of audio files into a single file.
    
    Args:
        file_list (list): List of paths to the audio files to concatenate
        output_path (str): Path to the output file
    """
    if not file_list:
        print("No files to concatenate")
        return
    
    print(f"Concatenating {len(file_list)} files:")
    for file in file_list:
        print(f"  - {os.path.basename(file)}")
    
    # Load the first audio file
    combined = AudioSegment.from_file(file_list[0])
    
    # Concatenate the remaining files
    for audio_file in file_list[1:]:
        try:
            audio = AudioSegment.from_file(audio_file)
            combined += audio
        except Exception as e:
            print(f"Error loading {audio_file}: {e}")
            continue
    
    # Export the combined file
    try:
        combined.export(output_path, format="mp3")
        print(f"File saved: {output_path}")
    except Exception as e:
        print(f"Error saving {output_path}: {e}")

def concatenate_audio_groups(folder_path, group_size, output_folder=None):
    """
    Concatenates audio files in groups of the specified size.
    
    Args:
        folder_path (str): Path to the folder containing audio files
        group_size (int): Number of files to concatenate per group
        output_folder (str): Output folder (optional)
    """
    # Get all audio files
    audio_files = get_audio_files(folder_path)
    
    if not audio_files:
        print("No audio files found in the specified folder")
        return
    
    print(f"Found {len(audio_files)} audio files")
    print(f"Creating groups of {group_size} files")
    
    # Calculate the number of groups
    num_groups = math.ceil(len(audio_files) / group_size)
    print(f"{num_groups} concatenated files will be created")
    
    # Set the output folder
    if output_folder is None:
        output_folder = os.path.join(folder_path, "concatenated")
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Concatenate files into groups
    for i in range(num_groups):
        start_idx = i * group_size
        end_idx = min(start_idx + group_size, len(audio_files))
        
        # Get the files for this group
        group_files = audio_files[start_idx:end_idx]
        
        # Output file name
        output_filename = f"concatenated_group_{i+1:02d}.mp3"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"\n--- Group {i+1}/{num_groups} ---")
        concatenate_audio_files(group_files, output_path)

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate audio files in groups of the specified size"
    )
    parser.add_argument(
        "folder_path",
        help="Path to the folder containing audio files"
    )
    parser.add_argument(
        "group_size",
        type=int,
        help="Number of audio files to concatenate per group"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output folder (default: 'concatenated' folder inside the input folder)"
    )
    
    args = parser.parse_args()
    
    try:
        concatenate_audio_groups(args.folder_path, args.group_size, args.output)
        print("\nConcatenation completed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
