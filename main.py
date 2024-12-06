import asyncio
import sys
from bilibili_api import search, video, Credential, HEADERS
import httpx
import os
import json

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"

async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                #print(f'下载 {info} {process} / {length}')
                f.write(chunk)

async def download_video_by_bvid(bvid: str, credential: Credential, output_filename: str):
    # 实例化 Video 类
    v = video.Video(bvid=bvid, credential=credential)
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_flv_stream() == True:
        # FLV 流下载
        await download_url(streams[0].url, "flv_temp.flv", "FLV 音视频流")
        # 转换文件格式
        os.system(f'{FFMPEG_PATH} -i flv_temp.flv {output_filename}')
        # 删除临时文件
        os.remove("flv_temp.flv")
    else:
        # MP4 流下载
        await download_url(streams[0].url, "video_temp.m4s", "视频流")
        await download_url(streams[1].url, "audio_temp.m4s", "音频流")
        # 混流
        os.system(f'{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy {output_filename}')
        # 删除临时文件
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")

    print(f'已下载为：{output_filename}')

async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    
    # 读取 badapple.json 文件
    with open('badapple.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for index, item in enumerate(data, start=1):
        song = item['song']
        difficulty = "谱面确认"
        combo = item['combo']
        
        # 拼接搜索关键词
        keyword = f"{song} {difficulty} {combo}"
        print(f"开始搜索并下载视频: {keyword}")
        
        # 搜索视频
        results = await search.search_by_type(keyword, search_type=search.SearchObjectType.VIDEO, page=1)
        if not results['result']:
            print("没有找到相关视频")
            continue
        
        # 获取第一个视频的 BVID
        first_video_bvid = results['result'][0]['bvid']
        print(f"找到视频 BVID: {first_video_bvid}")
        
        # 下载视频并保存为指定文件名
        output_filename = f"b{index}.mp4"
        await download_video_by_bvid(first_video_bvid, credential, output_filename)

if __name__ == '__main__':
    # 重定向标准输出到日志文件
    with open('log.txt', 'w', encoding='utf-8') as log_file:
        sys.stdout = log_file
        asyncio.get_event_loop().run_until_complete(main())