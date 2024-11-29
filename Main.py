import pygame
import os
import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
PROGRESS_WIDTH, PROGRESS_HEIGHT = 500, 200
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
HOVER_GRAY = (80, 80, 80)
GREEN = (0, 255, 0)
FONT = pygame.font.Font(None, 36)


def draw_text(text, x, y, color, center=False, font_size=36, screen=None):
    """Draws text on a Pygame screen."""
    if screen is None:
        screen = pygame.display.get_surface()
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y) if center else None)
    if center:
        screen.blit(text_surface, text_rect)
    else:
        screen.blit(text_surface, (x, y))


def draw_button(text, x, y, width, height, color, hover_color, text_color, action=None):
    """Draws a button and handles hover/click effects."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, x + width // 2, y + height // 2, text_color, center=True)


def draw_slider(value, min_val, max_val, x, y, width):
    """Draws a slider to adjust the clip duration."""
    pygame.draw.line(screen, WHITE, (x, y), (x + width, y), 4)
    slider_x = x + ((value - min_val) / (max_val - min_val)) * width
    pygame.draw.circle(screen, WHITE, (int(slider_x), y), 10)
    return value


def browse_video_file():
    """Opens a file dialog to browse for a video file."""
    Tk().withdraw()  # Hides the root Tkinter window
    file_path = askopenfilename(
        title="Select a video file",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv *.flv *.webm *.wmv *.m4v")]
    )
    if file_path:
        file_path = file_path.replace("\\", "/")  # Normalize file path
    return file_path


def get_video_duration(input_file):
    """Retrieve the duration of the video in seconds using FFmpeg."""
    try:
        ffmpeg_path = "ffmpeg"  # Ensure ffmpeg is available in PATH
        command = [ffmpeg_path, "-i", input_file]
        result = subprocess.run(
            command,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        for line in result.stderr.split("\n"):
            if "Duration" in line:
                duration = line.split(",")[0].split("Duration:")[1].strip()
                hours, minutes, seconds = map(float, duration.split(":"))
                return int(hours * 3600 + minutes * 60 + seconds)
    except Exception as e:
        print(f"Error getting video duration: {e}")
    return None


def split_video_ffmpeg(input_file, output_folder, clip_duration, progress_screen):
    """Splits a video into user-selected duration clips."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_duration = get_video_duration(input_file)
    if total_duration is None:
        return "Unable to determine video duration."

    total_clips = (total_duration + clip_duration - 1) // clip_duration
    progress = 0

    for i in range(total_clips):
        start_time = i * clip_duration
        output_file = os.path.join(output_folder, f"short_{i + 1}.mp4")
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i", input_file,
                    "-ss", str(start_time),
                    "-t", str(clip_duration),
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    output_file,
                    "-y"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except Exception as e:
            print(f"Error splitting clip {i + 1}: {e}")
            return "Error during splitting process."

        # Update progress bar
        progress = int(((i + 1) / total_clips) * 100)
        progress_screen.fill(BLACK)
        draw_text("Processing Clips...", PROGRESS_WIDTH // 2, 50, WHITE, center=True, screen=progress_screen)
        pygame.draw.rect(progress_screen, GRAY, (50, 100, 400, 30))
        pygame.draw.rect(progress_screen, GREEN, (50, 100, 4 * progress, 30))
        draw_text(f"{progress}% Complete", PROGRESS_WIDTH // 2, 150, WHITE, center=True, screen=progress_screen)
        pygame.display.update()

    return "Successfully created clips!"


def show_progress_window(input_file, output_folder, clip_duration):
    """Creates a progress window to show the progress bar."""
    progress_screen = pygame.display.set_mode((PROGRESS_WIDTH, PROGRESS_HEIGHT))
    pygame.display.set_caption("Processing...")
    result_message = split_video_ffmpeg(input_file, output_folder, clip_duration, progress_screen)
    progress_screen.fill(BLACK)
    draw_text(result_message, PROGRESS_WIDTH // 2, PROGRESS_HEIGHT // 2, WHITE, center=True, screen=progress_screen)
    pygame.display.update()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing
    pygame.quit()


def main():
    """Main function to run the Pygame UI."""
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("YouTube Shorts Maker")

    running = True
    selected_video = None
    message = ""
    clip_duration = 60  # Default duration for clips (in seconds)

    def browse_action():
        nonlocal selected_video, message
        selected_video = browse_video_file()
        if selected_video:
            message = f"Selected: {os.path.basename(selected_video)}"

    def split_action():
        nonlocal selected_video, message
        if selected_video:
            output_folder = "yt_shorts_output"
            show_progress_window(selected_video, output_folder, clip_duration)
        else:
            message = "Please select a video first."

    while running:
        screen.fill(BLACK)

        # Title
        draw_text("YouTube Shorts Maker", SCREEN_WIDTH // 2, 50, WHITE, center=True, font_size=48)

        # Slider for clip duration
        draw_text(f"Clip Duration: {clip_duration} sec", SCREEN_WIDTH // 2, 200, WHITE, center=True)
        pygame.draw.line(screen, WHITE, (200, 300), (700, 300), 4)
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and 200 <= mouse[0] <= 700 and 290 <= mouse[1] <= 310:
            clip_duration = int(10 + ((mouse[0] - 200) / 500) * (300 - 10))
        slider_x = 200 + ((clip_duration - 10) / (300 - 10)) * 500
        pygame.draw.circle(screen, WHITE, (int(slider_x), 300), 10)

        # Buttons
        draw_button("Browse Video", 300, 350, 200, 50, GRAY, HOVER_GRAY, WHITE, browse_action)
        draw_button("Create Clips", 300, 450, 200, 50, GRAY, HOVER_GRAY, WHITE, split_action)

        # Display message
        draw_text(message, SCREEN_WIDTH // 2, 550, WHITE, center=True, font_size=28)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
