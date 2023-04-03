# fu-Bot
基于[nonebot](https://github.com/nonebot/nonebot2)和[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)的QQ娱乐机器人，具有聊天娱乐与**舞萌DX**游戏信息查询等相关功能。

**GitHub**：[fu-Bot](https://github.com/HCskia/fu-Bot)

## 1. 前置
### 安装Python
此项目基于**Python 3.9.12**，建议使用**版本大于或等于 3.8 或者小于 4.0 的Python**添加到环境变量中使用。

Python下载：https://www.python.org/

### 前置资源
在开始使用此项目之前，请先下载项目资源文件并解压到项目 src 文件夹中：
>下载链接：[度盘](https://pan.baidu.com/s/15iwz6LQDP3hYEYBM2go5vw?pwd=skia)  [Google云](https://drive.google.com/file/d/1OFWI6JyIatXVuhZtrehApgzV1EVDbZ-n/view?usp=share_link)
>
>声明：此资源文件仅供学习参考交流使用，严禁用于商业用途，下载后请于24小时内删除。

## 2. 项目使用
可以直接将项目文件下载到本地使用 [Download ZIP](https://github.com/HCskia/fu-Bot/archive/refs/heads/main.zip)或者使用git来进行项目版本管理。

请安装 requirement.txt 中的插件：
>pip install -r requirement.txt

### 下载 go-cqhttp
在 https://github.com/Mrs4s/go-cqhttp/releases 下载 go-cqhttp 的最新版本， 然后解压出 go-cqhttp.exe 即可。


将解压出的 go-cqhttp.exe 文件放到任意文件夹内（路径名最好不含中文）之后，在同目录下新建一个.bat文件写入以下内容
```
go-cqhttp.exe faststart
```

双击.bat文件启动 go-cqhttp，并选择 **反向Websocket通信** ，第一次运行后会生成 **congfig.yml** 文件，打开此文件并且修改配置：
```
account: 
  uin: # 你的bot QQ账号
  password: '' # 你的bot QQ密码

message:
  post-format: array

servers:
  - ws-reverse:
      universal: ws://127.0.0.1:10219/onebot/v11/ws
```

## 3. 功能

**普通功能**:

Command | Function
--- | ---
fu help | 返回指令帮助
<[戳一戳]> | 发送戳一戳相关图片(可自定义)
<[当有新群成员]> | 发送欢迎相关图片和信息(可自定义)
<[复读]> | 当某一个群聊中信息重复四次以上时复读一次
<[每日新闻]> | 每天早上8点自动发送每日要闻
xxxxx吃啥 | 发送"建议xxxxx吃(一个随机食物)"(可自定义)
请fufu吃xxxxx | 给吃啥功能添加食物
ph add <id> | 添加一个可迫害的id (id数量大于一个时为别名，用英文逗号分割)
ph<id> <[附带一张迫害图片]> | 添加图片到可迫害的id中
ph<id> | 随机返回一张此迫害id的图片
ph list | 查询ph列表
ph rank | 获取迫害排行榜(根据迫害图片数量)
<[B站分享]> | 解析群聊中的b站分享信息

**舞萌功能**：
Command | Function
--- | ---
今日fu | 获取今日运势
b40/b50 | 生成b40或b50图片
<难度等级>分数列表 <页数[可选]> | 生成分数列表图片 页数为0时返回全部数据
定数算分 <定数> <完成度> | 返回根据在该定数下达成相应完成度的rating值
随个<dx/sd[可选]><绿/黄/红/紫/白[可选]><难度> | 随歌
搜曲<歌曲标题的一部分> | 搜索相应的歌曲
<绿/黄/红/紫/白[可选]>id<歌曲id> | 查询谱面信息
谱面分数线 <绿/黄/红/紫/白><歌曲id> <完成度> | 查询谱面在该完成度下所需容错率
分算定数 <rating值> | 返回可以达成该分数的相应定数与完成度
添加别名 <歌曲id> <别名> | 添加此id的歌曲别名
删除别名 <歌曲id> <别名> | 删除在id中的歌曲的这个别名
<别名>是什么歌 | 通过别名搜索歌曲
<难度>天梯图 | 获取该难度的谱面定数天梯图
<版本简称>代完成表 | 生成根据等级排列的该代谱面完成表
dx店铺 <地区> <参数[可选]> | 返回该地区的舞萌DX机台铺货参数

**其他功能**：
Command | Function
--- | ---
chu店铺 <地区> <参数[可选]> | 返回该地区的中二节奏机台铺货参数

## 更多
eat.json文件：
```
{"eat": [],"blackword":[]}
```
 "eat" 中存放的是 [食物] , "blackword" 中存放的是 [黑名单词语]
当用户使用请小fufu吃的功能时，如果输入的食物字符串与黑名单词语中的字符串相同，同时bot也有管理员权限，该用户会被禁言1~10分钟（随机），这两个地方的内容可以自行定义添加。

todayFu.json文件：
```
{"今日运势":["name":"","good","","bad":""],"今日游戏":[""],"移动端地点":[""],"maimai黄金位":[""]}
```
 通过修改此文件，可自定义今日运势中的信息。

 musicAliases.json文件：
 ```
 [{"id": 8, "title": "True Love Song", "alias": ["true love song", "真爱歌", "G弦上的咏叹调", "巴赫", "老八", "既实惠还管饱"]}]
 ```
 通过修改此文件，可直接自定义乐曲别名。

pohai文件夹：
pohai文件夹的子文件夹用为存储迫害对象的迫害图片，子文件夹的命名方式为“id,alias,alias2”(不带引号，用英文逗号分隔)，其中alias为别名。
>例如 static/images/pohai/hc,hcskia
>
>phhc 等于 phhcskia

poke文件夹：
poke文件夹用于存储戳一戳表情包，可以自行添加自己想要的戳一戳表情包。

welcome文件夹：
welcome文件夹用于存储欢迎新成员时的图像，可以自行添加自己想要图片文件。

## 更新
**2023-3-8** 发布
  
**2023-4-3** B站解析修复

## 感谢

**nonebot：**[GitHub](https://github.com/nonebot/nonebot2)

**go-cqhttp：**[GitHub](https://github.com/Mrs4s/go-cqhttp)

**Diving-Fish(mai歌曲信息数据)：**[GitHub](https://github.com/Diving-Fish)，[查分器](https://www.diving-fish.com/maimaidx/prober/)

# License

MIT

您可以自由使用本项目的代码用于商业或非商业的用途，但必须附带 MIT 授权协议。
