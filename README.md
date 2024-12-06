# Autob50
##本项目用于辅助制作个人b50视频，可以大大减少视频制作的时间，并保留一定的个性化。  
###先提准备:  
1.b站的cookie，主要是SESSDATA 和 BILI_JCT，https://nemo2011.github.io/bilibili-api/#/get-credential。  
2.b50JSON文件，可以通过查分器导出，参考本项目中的badapple.json格式  
###使用流程:  
1.准备好b50的json后，在main.py里填入你的SESSDATA 和 BILI_JCT，安装必要的依赖库。  
运行main.py，将自动搜索并保存b1.mp4到b2.mp4视频  
2.运行cutvideo.py,将调用ffmpeg将这50个视频剪辑出35秒到55秒，并保存为b{i}_cut.mp4文件。  
3.运行createsrt文件，将自动生成四个字幕文件，分别是曲名，定数，成绩，感想（都是默认的好听好玩）  
4.运行outputvideo.py将视频拼接成一个完整视频，或直接导入剪辑软件，因为下载下来的视频不一定是我们想要的，有的需要手动替换  
5.在剪辑软件中排版配图（可以用getimgs.py下载）  
导入字幕文件，编辑感想，加上片头片尾，导出  
##恭喜你的私人b50视频新鲜出炉啦！  
