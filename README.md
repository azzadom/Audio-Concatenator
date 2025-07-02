# Audio Concatenator

A Python script to concatenate audio files into specified groups, generating longer audio files from a folder of shorter ones.

## Requirements

* Python 3.7+
* [ffmpeg](https://ffmpeg.org/) installed on the system (required for compatibility with many audio formats)
* Python dependencies listed in `requirements.txt`

## Installation

### 1. Create a virtual environment

On **Linux/macOS**:

```bash
python -m venv audio_env
source audio_env/bin/activate
```

On **Windows**:

```bash
python -m venv audio_env
audio_env\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Make sure ffmpeg is installed

* **macOS:**
  `brew install ffmpeg`
* **Ubuntu/Debian:**
  `sudo apt install ffmpeg`
* **Windows:**
  Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add `ffmpeg` to the PATH

## Usage

### Main script

To concatenate audio files from a folder in groups of 3:

```bash
python audio_concatenator.py "/path/to/audio/folder" 3
```

To specify a different output folder:

```bash
python audio_concatenator.py "/path/to/audio/folder" 3 -o "/path/to/output/folder"
```

* Replace `"/path/to/audio/folder"` with the actual path to your audio files folder.
* Replace `3` with the number of files to concatenate per group.
* The output will be saved in the `concatenated` folder inside the input folder unless another folder is specified with `-o`.

### Example usage from Python

You can also use the function directly in a Python script:

```python
from audio_concatenator import concatenate_audio_groups

folder_path = "/path/to/audio/folder"
group_size = 3
output_folder = "/path/to/output/folder"  # optional

concatenate_audio_groups(folder_path, group_size, output_folder)
```

## Output

The concatenated files will be named:

```
concatenated_group_01.mp3
concatenated_group_02.mp3
...
```

and will be saved in the selected output folder.

---

**Note**: The number of generated files will be equal to `ceil(total_files / group_size)`.
If you have 11 files and choose `3` as the group size, you will get 4 output files: 3+3+3+2.
