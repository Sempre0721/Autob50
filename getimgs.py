import asyncio
import sys
import httpx
import os
import json
from bilibili_api import search, video, Credential, HEADERS

SESSDATA = "249cf650%2C1748866682%2C572c7%2Ac1CjCeM98Wmzw7yExxVC9Y0dE3CQcV4UTik5rB1E-l2RypGK2zJXhyNWaplshyoIr0_mkSVlBkamdiWTkwWDBFb2gtUGNWdUI3LU9tU1RUSHNIdzBtVmM0MTlac3ZtaUJHUkRXazgxTkIwaE9qWHlRZGI0S0RDNU5NeG9PYkN2bC1VSkhHS3BOWU93IIEC"
BILI_JCT = "94efcf02895b460325508a0567fbe8c8"
BUVID3 = ""

# 下载函数
async def download_url(url: str, out: str, info: str):
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                # print(f'下载 {info} {process} / {length}')
                f.write(chunk)

# 下载视频封面
async def download_video_cover_by_bvid(bvid: str, credential: Credential, output_filename: str):
    # 实例化 Video 类
    v = video.Video(bvid=bvid, credential=credential)
    # 获取视频信息
    info = await v.get_info()
    # 获取封面 URL
    cover_url = info['pic']
    # 下载封面
    await download_url(cover_url, output_filename, "封面")

async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    
    # 读取 badapple.json 文件
    with open('badapple.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for index, item in enumerate(data, start=1):
        song = item['song']
        
        # 拼接搜索关键词
        keyword = f"{song}"
        print(f"开始搜索并下载视频封面: {keyword}")
        
        # 搜索视频
        results = await search.search_by_type(keyword, search_type=search.SearchObjectType.VIDEO, page=1)
        if not results['result']:
            print("没有找到相关视频")
            continue
        
        # 获取第一个视频的 BVID
        first_video_bvid = results['result'][0]['bvid']
        print(f"找到视频 BVID: {first_video_bvid}")
        
        # 下载视频封面并保存为指定文件名
        output_filename = f"cover_{index}.jpg"
        await download_video_cover_by_bvid(first_video_bvid, credential, output_filename)

if __name__ == '__main__':
    # 重定向标准输出到日志文件
    with open('log.txt', 'w', encoding='utf-8') as log_file:
        sys.stdout = log_file
        asyncio.get_event_loop().run_until_complete(main())