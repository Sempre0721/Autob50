import json

def generate_subtitle_file(data, filename, key):
    with open(filename, 'w', encoding='utf-8') as file:
        start_time = 0
        for i, item in enumerate(data, start=1):
            end_time = start_time + 20
            start_str = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{int(start_time % 60):02d},{int((start_time % 1) * 1000):03d}"
            end_str = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{int(end_time % 60):02d},{int((end_time % 1) * 1000):03d}"
            line = f"{i}\n{start_str} --> {end_str}\n{item[key]}\n\n"
            file.write(line)
            start_time = end_time

def generate_fixed_subtitle(filename, text, duration_per_item, num_items):
    with open(filename, 'w', encoding='utf-8') as file:
        start_time = 0
        for i in range(1, num_items + 1):
            end_time = start_time + duration_per_item
            start_str = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{int(start_time % 60):02d},{int((start_time % 1) * 1000):03d}"
            end_str = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{int(end_time % 60):02d},{int((end_time % 1) * 1000):03d}"
            line = f"{i}\n{start_str} --> {end_str}\n{text}\n\n"
            file.write(line)
            start_time = end_time

def main():
    with open('badapple.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    generate_subtitle_file(data, 'song_subtitles.srt', 'song')
    generate_subtitle_file(data, 'accuracy_subtitles.srt', 'accuracy')
    generate_subtitle_file(data, 'combo_subtitles.srt', 'combo')
    generate_fixed_subtitle('comment_subtitles.srt', '感想:好听好玩', 20, len(data))

if __name__ == "__main__":
    main()