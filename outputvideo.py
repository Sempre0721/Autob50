from moviepy.editor import VideoFileClip, concatenate_videoclips

def main():
    clips = []
    for i in range(1, 51):
        output_path = f'b{i}_cut.mp4'  # 输出文件名为 b1_cut.mp4, b2_cut.mp4, ..., b50_cut.mp4
        processed_clip = VideoFileClip(output_path)
        clips.append(processed_clip)
    
    # 拼接所有剪辑后的视频
    final_clip = concatenate_videoclips(clips)
    
    # 输出最终的视频文件
    final_clip.write_videofile("final_output.mp4", codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    main()