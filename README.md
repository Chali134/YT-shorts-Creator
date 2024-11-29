
# YouTube Shorts Maker

A Python-based application with a graphical user interface (GUI) built using Pygame that helps users split videos into custom-length clips, ideal for YouTube Shorts. The app features an interactive slider for selecting clip durations and a dynamic progress window to monitor processing.

---

## Features

- **Custom Clip Duration**: Set clip duration dynamically using a slider (10 to 300 seconds).
- **User-Friendly Interface**: A sleek black-and-white GUI built with Pygame.
- **Progress Window**: A dedicated window displays a progress bar and percentage completion during video processing.
- **Automatic Output**: Clips are saved in an `yt_shorts_output` folder.

---

## Installation

### Prerequisites

1. **Python 3.7+**
   Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/).

2. **FFmpeg**
   FFmpeg is required for video processing.
   - Install FFmpeg:
     ```bash
     winget install ffmpeg
     ```
   - Verify installation:
     ```bash
     ffmpeg -version
     ```

3. **Python Dependencies**
   Install required Python libraries:
   ```bash
   pip install pygame
   ```

---

## Usage

1. Clone or download this repository.
2. Run the `yt_shorts_maker.py` script:
   ```bash
   python yt_shorts_maker.py
   ```
3. Follow the instructions on the GUI:
   - **Browse Video**: Click the button to select a video file.
   - **Set Clip Duration**: Use the slider to set the desired clip duration (10 to 300 seconds).
   - **Create Clips**: Click the button to process the video. A progress window will appear showing the processing status.
4. The clips will be saved in a folder named `yt_shorts_output` in the same directory as the script.

---

## How It Works

1. **Video Selection**: Browse and select a video file using the GUI.
2. **Clip Duration Selection**: Adjust the slider to choose the clip duration.
3. **Processing**:
   - The video is split into clips of the selected duration.
   - The progress window updates dynamically, showing the completion percentage.
4. **Output**: Clips are saved in `yt_shorts_output` with filenames like `short_1.mp4`, `short_2.mp4`, etc.

---

## Screenshots

### Main Screen
- **Browse Video** button.
- **Clip Duration Slider** for setting clip lengths.
- **Create Clips** button.

### Progress Window
- Shows progress bar and percentage completion during processing.

---

## Requirements

- Python 3.7+
- FFmpeg
- Pygame

---

## Contributing

Feel free to fork this repository and make improvements. Contributions are welcome! 

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or suggestions, feel free to reach out:
- **Name**: Ali Sajjad
- **Email**: ali_sajjad134@outlook.com
- **GitHub**: [Chali134](https://github.com/Chali134)

