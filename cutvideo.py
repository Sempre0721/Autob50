from moviepy.editor import VideoFileClip, afx

def process_video(video_path, output_path):
    # 加载视频文件
    clip = VideoFileClip(video_path)
    
    # 剪辑视频的第35秒到第55秒
    sub_clip = clip.subclip(35, 55)
    
    # 在开头和结尾添加音频淡入淡出效果
    audio_fade_in = sub_clip.audio.fx(afx.audio_fadein, 1)
    audio_fade_out = audio_fade_in.fx(afx.audio_fadeout, 1)
    sub_clip = sub_clip.set_audio(audio_fade_out)
    
    # 保存剪辑后的视频
    sub_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

def main():
    for i in range(1, 51):
        video_path = f'b{i}.mp4' 
        output_path = f'b{i}_cut.mp4'  
        process_video(video_path, output_path)

if __name__ == "__main__":
    main()
