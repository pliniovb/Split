import cv2
import os
import argparse

# Video processing function
def process_video(input_video_path, output_format):
    output_folder_path = './splits'
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    base_name = os.path.splitext(os.path.basename(input_video_path))[0]
    output_video_left_path = os.path.join(output_folder_path, f'{base_name}_left.{output_format}')
    output_video_right_path = os.path.join(output_folder_path, f'{base_name}_right.{output_format}')

    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print(f"ERROR - video not found: {input_video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') if output_format == 'mp4' else cv2.VideoWriter_fourcc(*'XVID')
    out_left = cv2.VideoWriter(output_video_left_path, fourcc, fps, (frame_width // 2, frame_height))
    out_right = cv2.VideoWriter(output_video_right_path, fourcc, fps, (frame_width // 2, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        left_half = frame[:, :frame_width // 2]
        right_half = frame[:, frame_width // 2:]

        out_left.write(left_half)
        out_right.write(right_half)

    cap.release()
    out_left.release()
    out_right.release()

    print(f"Split already done: {input_video_path}")

# Setting command line arguments
parser = argparse.ArgumentParser(description='Process videos in a folder by splitting them vertically in half.')
parser.add_argument('input_folder', type=str, help='Path to the input folder containing the videos.')
parser.add_argument('output_format', type=str, choices=['mp4', 'avi'], help='Video output format (mp4 or avi).')

args = parser.parse_args()

input_folder_path = args.input_folder
output_format = args.output_format

input_files = [f for f in os.listdir(input_folder_path) if f.endswith(('.mp4', '.avi', '.mov'))]

for input_file in input_files:
    input_video_path = os.path.join(input_folder_path, input_file)
    process_video(input_video_path, output_format)

print("All spliting completed.")
