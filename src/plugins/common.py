import concurrent
import datetime
import string
import textwrap
import aiohttp
import requests
from bs4 import BeautifulSoup
# ===
from nonebot.matcher import matchers
from nonebot.rule import *
from nonebot.adapters.onebot.v11 import *
from nonebot.utils import *
from nonebot import *
import nonebot
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
# === 前置导入 ====
from src.plugins.tools import *


# == 帮助功能
help = on_command("fu help", aliases={"fu 帮助"})
@help.handle()
async def help_main(matchers: help, event: GroupMessageEvent):
    msg = """您好，这里是小fu,以下是功能列表：
fu help ： 返回指令帮助
fu help mai ： 查看maimai功能的帮助内容
xxxxx吃啥 ： 发送"建议xxxxx吃(一个随机食物)"(可自定义)
请fufu吃<食物> ： 将一个食物文本添加到(吃啥)功能中


ph<id> ： 随机返回一张此迫害id的图片
ph<id> <[附带一张迫害图片]> ： 添加图片到可迫害的id中
ph add <id> ： 添加一个可迫害的id (id数量大于一个时为别名，用英文逗号分割)
ph list : 查询ph列表
ph rank ： 获取迫害排行榜(根据迫害图片数量)
"""
    await help.finish(Message(msg))

maiHelp = on_command("fu help mai")
@maiHelp.handle()
async def maiHelp_main(matchers: maiHelp, event: GroupMessageEvent):
    msg = """您好，这里是小fu,以下是舞萌功能列表：
今日fu ： 获取今日运势
b40/b50 ： 生成b40或b50图片
<难度等级>分数列表 <页数[可选]> ： 生成分数列表图片 页数为0时返回全部数据
定数算分 <定数> <完成度> ： 返回根据在该定数下达成相应完成度的rating值
分算定数 <rating值> ： 返回可以达成该分数的相应定数与完成度
随个<dx/sd[可选]><绿/黄/红/紫/白[可选]><难度> ： 随歌
<绿/黄/红/紫/白[可选]>id<歌曲id> ： 查询谱面信息
搜曲<歌曲标题的一部分> ： 搜索相应的歌曲
<版本简称>代完成表 ： 生成根据等级排列的该代谱面完成表
<版本简称><将/极/舞舞/神>进度 ： 返回该成就达成进度
添加别名 <歌曲id> <别名> ： 添加此id的歌曲别名
删除别名 <歌曲id> <别名> ： 删除在id中的歌曲的这个别名
<别名>是什么歌 ： 通过别名搜索歌曲
dx店铺 <地区> <参数[可选]> ： 返回该地区的舞萌DX机台铺货参数
"""
    await maiHelp.finish(Message(msg))


# == 戳一戳
async def pokeCheck(event: PokeNotifyEvent) -> bool:
    return event.sub_type == "poke"
async def pokeBotCheck(event: PokeNotifyEvent) -> bool:
    return event.target_id == event.self_id
pokeRule = Rule(pokeCheck,pokeBotCheck)
poke = on_notice(pokeRule)
@poke.handle()
async def poke_main(matchers: poke, event: PokeNotifyEvent):
    await poke.finish(Message(
        f"""[CQ:image,file=base64://{str(image_to_base64_gif(f"{getRandomFile(r'src/static/images/poke')}"), encoding='utf-8')}]"""))


# == 新群成员员加入、群成退出
async def groupMemQuitCheck(event: GroupDecreaseNoticeEvent) -> bool:
    return event.sub_type == "leave"
groupMemQuitRule = Rule(groupMemQuitCheck)
groupMemLeave = on_notice(groupMemQuitRule)
@groupMemLeave.handle()
async def groupMemLeave_main(matchers: groupMemLeave, event: GroupDecreaseNoticeEvent):
    await groupMemLeave.finish(Message(f"大佬(@{event.user_id})好像离开了呢....."))

async def groupMemJoinCheck(event: GroupIncreaseNoticeEvent) -> bool:
    return event.notice_type == "group_increase"
groupMemJoinRule = Rule(groupMemJoinCheck)
groupMemJoin = on_notice(groupMemJoinRule)
@groupMemJoin.handle()
async def groupMemJoin_main(matchers: groupMemJoin, event: GroupIncreaseNoticeEvent):
    await groupMemJoin.finish(Message(f"欢迎新椰叶 " + f"[CQ:at,qq={event.user_id}]" + "!!!!!\n" + f"""[CQ:image,file=base64://{str(image_to_base64_gif(f"{getRandomFile(r'src/static/images/welcome')}"), encoding='utf-8')}]"""))


# == 群成员被踢出
async def groupMemBeKikedCheck(event: GroupDecreaseNoticeEvent) -> bool:
    return event.sub_type == "kick"
groupMemBeKikedRule = Rule(groupMemBeKikedCheck)
groupMemBeKiked = on_notice(groupMemBeKikedRule)
@groupMemBeKiked.handle()
async def groupMemBeKiked_main(matchers: groupMemBeKiked, event: GroupDecreaseNoticeEvent):
    await groupMemBeKiked.finish(Message(f"恭喜(@{event.user_id})获得一张飞机票~"))


# == 复读
noKeyWordFunctions = on_regex(".*", permission=GROUP)
@noKeyWordFunctions.handle()
async def noKeyWordFunctions_main(matchers: noKeyWordFunctions, event: GroupMessageEvent):
    msgString = unescape(str(event.message))
    for keyWord in ['BV', 'b23.tv']:
        if keyWord in msgString:
            await bilibiliFunc(msgString, nonebot.get_bot(self_id=str(event.self_id)), event.group_id)
            break
    if "CQ" in str(event.message):
        await noKeyWordFunctions.finish()
    fdGroupData = readJson(r"src\static\datas\fudu.json")
    isFuduGroupInFile = False
    for tData in fdGroupData:
        if event.group_id == tData['groupId']:
            isFuduGroupInFile = True
        if str(event.message) != tData['msg']:
            tData['msg'] = str(event.message)
            tData['times'] = 1
            break
        tData['times'] += 1
        if tData['times'] > 3:
            await noKeyWordFunctions.finish()
        elif tData['times'] == 3:
            await noKeyWordFunctions.send(Message(str(event.message)))
    if not isFuduGroupInFile:
        fdGroupData.append({"groupId": event.group_id, "msg": str(event.message), "times": 1})
    writeJson(r"src\static\datas\fudu.json", fdGroupData)
    await noKeyWordFunctions.finish()


# == b站解析
async def bilibiliFunc(msg, bot, groupId):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    timeout = aiohttp.ClientTimeout(total=15)
    if 'BV' in msg:
        msg = msg[msg.find("BV"):len(msg)]
        if '/' in msg:
            bvNum = msg.replace(msg[msg.find('/'):len(msg)], "")
        else:
            bvNum = msg
        videoUrl = f"https://www.bilibili.com/video/{bvNum}"
    elif 'b23.tv' in msg:
        msg = msg.replace(r'\/','/')
        if "哔哩哔哩HD" in msg:
            msg = msg[msg.find('jumpUrl'):len(msg)]
            msg = msg[0:msg.find('&#44')]
            msg = msg[0:msg.find(',')].replace("&#44", "").replace(",", '')
            videoUrl = "https://" + msg[msg.find('b23.tv'):msg.find('";')].replace('"', "")
        elif "QQ小程序" in msg:
            msg = msg[msg.find('qqdocurl'):len(msg)]
            msg = msg[0:msg.find('&#44')]
            msg = msg[0:msg.find(',')].replace("&#44", "").replace(",", '')
            videoUrl = "https://" + msg[msg.find('b23.tv'):msg.find('";')].replace('"', "")
        else:
            videoUrl = re.search("(?P<url>https?://[^\s]+)", msg).group("url")
        if "?" in videoUrl:
            videoUrl = videoUrl.replace(f'{videoUrl[videoUrl.find("?"):len(videoUrl)]}', "")
    else:
        return 0
    logger.info("[b站解析]videoUrl:"+videoUrl)
    try:
            async with aiohttp.request("GET", videoUrl, headers=head, timeout=timeout) as resp:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
            try:
                title = soup.find('h1', attrs={'class': "video-title"})['title']
            except:
                title = "标题获取失败"
            try:
                view = soup.find('span', attrs={'class': "view"})['title']
            except:
                view = "总播放数：获取失败"
            try:
                dm = soup.find('span', attrs={'class': "dm"})['title']
            except:
                dm = "历史累计弹幕数：获取失败"
            try:
                like = "点赞：" + str(soup.find('span', attrs={'class': 'like'}).get_text().replace(" ", '').replace('\n', ''))
            except:
                like = "点赞：获取失败"
            try:
                coin = "硬币：" + str(
                    soup.find('span', attrs={'class': 'coin'}).get_text().replace(" ", '').replace('\n', ''))
            except:
                coin = "硬币：获取失败"
            try:
                collect = "收藏：" + str(
                    soup.find('span', attrs={'class': 'collect'}).get_text().replace(" ", '').replace('\n', ''))
            except:
                collect = "收藏：获取失败"
            try:
                share = "分享：" + str(
                    soup.find('span', attrs={'class': 'share'}).get_text().replace(" ", '').replace('\n', ''))
            except:
                share = "分享：获取失败"
            try:
                up = "UP主：" + str(
                    soup.find('a', attrs={'class': 'username'}).get_text().replace(" ", '').replace('\n', ''))
            except:
                up = "UP主：获取失败"
            try:
                description = "简介：\n" + (str(soup.find('div', attrs={'id': 'v_desc'}).get_text())).replace("收起", "\n")
            except:
                description = "简介：NONE\n"
            try:
                img = str(soup.find('meta', attrs={'itemprop': 'image'})['content'])
                img = f"视频封面：\n[CQ:image,file=http:{img.replace('@100w_100h_1c.png', '')}]"
            except:
                img = "视频封面：获取失败"
            try:
                url = "链接：" + str(soup.find('meta', attrs={'itemprop': 'url'})['content'])
            except:
                url = "链接获取失败"
            fMsg = f"""{title}\n{up}\n{description}\n{view}\n{dm}\n{like}\n{coin}\n{collect}\n{share}\n{url}\n{img}"""
            await bot.send_group_msg(message=fMsg, group_id=groupId)
    except concurrent.futures._base.TimeoutError:
        await bot.send_group_msg(message=f"[b站分享解析]发生错误 原因：VideoUrl访问超时", group_id=groupId)
    except Exception as e:
        await bot.send_group_msg(message=f"[b站分享解析]发生错误 原因：{e}", group_id=groupId)
    return 0


# == 日常新闻
@scheduler.scheduled_job('cron', hour=21, minute=46)
async def dailyNews_main():
    fufu: Bot = nonebot.get_bot(self_id=nonebot.get_bot().self_id)
    newsData = str((requests.get("http://bjb.yunwj.top/php/qq.php")).text).replace("'", '"')
    newsData = json.loads(newsData)
    newsImgDownload = requests.get(newsData['tp'])
    with open(r"src\static\images\newsTemp.jpg", 'wb+')as f:
        f.write(newsImgDownload.content)
    newsText = str(newsData['wb']).split("【换行】")
    newsText2 = []
    for i in newsText:
        newsText2.append(textwrap.fill(i.replace('&#34',' '), width=22))
    text = ""
    for i in newsText2:
        text += f"{i}\n\n"
    bgImg = Image.new("RGB", (1920, 1080), (255, 255, 255))
    bgImgDr = ImageDraw.Draw(bgImg)
    font = ImageFont.truetype(r'src\static\Material\msyh.ttc', 13)
    font2 = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 13)
    imgSize = bgImgDr.multiline_textsize(text, font=font)
    newImg = bgImg.resize((imgSize[0] + 10, imgSize[1] + 10))
    newImgDr = ImageDraw.Draw(newImg)
    newImgDr.text((1, 1), text, font=font, fill="#000000")
    newsImg = Image.open(r"src\static\images\newsTemp.jpg").resize((300, 166))
    newsBaseImg = Image.new('RGB', (350, newImg.height + 191), color=(255, 255, 255))
    newsBaseImg.paste(newsImg, (25, 25))
    newsBaseImg.paste(newImg, (32, 230))
    newsBgDraw = ImageDraw.Draw(newsBaseImg)
    newsBgDraw.text((35, 200), f"To Day News", font=font2, fill=(237, 28, 36))
    newsBgDraw.text((250, 200), f"{datetime.datetime.now().strftime('%Y.%m.%d')}", font=font, fill=(195, 195, 195))
    newsBgDraw.text((35, 210), f"-----------------------------------------------", font=font2, fill=(205, 205, 205))
    for group in (await fufu.get_group_list()):
        await fufu.send_group_msg(message=f"""[CQ:image,file=base64://{str(image_to_base64(newsBaseImg), encoding='utf-8')}]""", group_id=group['group_id'])


# == 吃啥
eatWhat = on_keyword(keywords={"吃啥"}, permission=GROUP)
@eatWhat.handle()
async def eatWhat_main(matchers:eatWhat, event: GroupMessageEvent):
    msg = str(event.message).replace("吃啥", "")
    eats = readJson(r'src\static\datas\eat.json')['eat']
    await eatWhat.finish(Message(f"""建议{msg}吃{eats[random.randint(0, len(eats) - 1)]}呢~"""))

tellFuToEat = on_keyword(keywords={"请fufu吃"}, permission=GROUP)
@tellFuToEat.handle()
async def tellFuToEat_main(matchers:tellFuToEat, event: GroupMessageEvent):
    fufu: Bot = nonebot.get_bot(self_id=str(event.self_id))
    msg = str(event.message).replace("请fufu吃", "")
    blackWord = readJson(r'src\static\datas\eat.json')['blackword']
    if msg in blackWord:
        try:
            await fufu.set_group_ban(user_id=event.user_id, duration=random.randint(60, 600),group_id=event.group_id)
        except ActionFailed:
            await tellFuToEat.finish(Message("欺负我没权限不能禁言是吧凸(艹皿艹 )"))
        await tellFuToEat.finish(Message("建议亲亲不要乱搞呢( ･´ω`･ )"))
    for word in blackWord:
        if word in msg:
            await fufu.set_group_ban(user_id=event.user_id, duration=random.randint(60, 600),group_id=event.group_id)
            await tellFuToEat.finish(Message("建议亲亲不要乱搞呢( ･´ω`･ )"))
    if msg != "":
        foods = readJson(r'src\static\datas\eat.json')['eat']
        if msg in foods:
            await tellFuToEat.finish("本fu已经吃过这个了捏")
        else:
            foods.append(msg)
            data = {'eat':foods,'blackword':blackWord}
            writeJson(r'src\static\datas\eat.json', data)
            await tellFuToEat.finish("蟹蟹！我记住哩！^_^")
    await tellFuToEat.finish()


# == 迫害功能
phVoidWords = ['Phigros', 'phigros', 'Prophesy', 'prophesy'] #为了避免误触发，如果有需要屏蔽的词语，请再次添加
pohai = on_keyword(keywords={"ph"})
@pohai.handle()
async def pohai_main(matchers: pohai, event: GroupMessageEvent):
    func = str(event.message)
    for t in phVoidWords:
        if t in func:
            await pohai.finish()
    pohaiList = []
    for root, dirs, files in os.walk(r'src\static\images\pohai'):
        for file in dirs:
            pohaiList.append(str(file))
    if "CQ:image" in func.replace(" ", ''):
        func = func.split("[")
        id = str(func[0]).replace("迫害", "").replace("ph", "").replace("pohai", "")
        Url = func[1][func[1].find("url=") + 4:func[1].find("]")]

        isFindId = False
        for i in pohaiList:
            if id in i.split(','):
                id = i
                isFindId = True
        if isFindId == False:
            await pohai.finish(Message("[迫害]没有找到相应迫害人员"))

        fileList = []
        for root, dirs, files in os.walk(rf"src\static\images\pohai\{id}"):
            for file in files:
                fileList.append(str(os.path.join(file)))
        while (True):
            notInFile = True
            randomFileName = "".join(random.sample(string.ascii_letters + string.digits, 16))
            for tempFileName in fileList:
                tempFileName = str(tempFileName)
                if randomFileName in tempFileName:
                    notInFile = False
            if notInFile == True:
                break
        img = requests.get(f"{Url}")
        with open(rf"src\static\images\pohai\{id}\{randomFileName}.gif", 'wb+') as f:
            f.write(img.content)
            f.close()
        await pohai.finish(Message("[迫害]添加迫害成功~"))
    elif func == 'phlist':
        msg = "以下是迫害名单(符号.为别名衔接)：\n"
        for i in pohaiList:
            msg += f"{i.replace(',', '.')}、"
        await pohai.finish(Message(msg))
    elif "add" in func:
        func = func.replace("迫害", "").replace("ph", "").replace("pohai", "")
        id = func.replace("添加", "").replace("add", "").replace(" ", '')
        isFindId = False
        for i in pohaiList:
            if id in i:
                id = i
                isFindId = True
        if isFindId == True:
            await pohai.finish(Message("[迫害]已经存在相应迫害人员~"))
        os.makedirs(rf"src\static\images\pohai\{id}")
        await pohai.finish(Message("[迫害]添加迫害人员成功~"))
    elif "rank" in func:
        pohaiRankInfo = []
        for info in os.walk(r'src\static\images\pohai'):
            if info[0] == r"src\static\images\pohai":
                continue
            Id = info[0].replace("src/static/images/pohai\\", "")
            ImgAmount = len(info[2])
            pohaiRankInfo.append({f"id": Id, "amount": ImgAmount})
        sortedRankInfo = sorted(pohaiRankInfo, key=lambda x: x['amount'], reverse=True)
        Fmsg = "=>迫害排行榜\n"
        Time = 1
        for line in sortedRankInfo[0:10]:
            line["id"] = line["id"].replace("src\static\images\pohai\\", "")
            Fmsg += f' No.{Time} ({line["amount"]}张) :  {line["id"]}\n'
            Time += 1
        await pohai.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(TextToImg(Fmsg)), encoding='utf-8')}]"""))
    elif func == "sjph":
        while (True):
            id = pohaiList[random.randint(0, len(pohaiList) - 1)]
            pohaiImgList = []
            for root, dirs, files in os.walk(rf"src\static\images\pohai\{id}"):
                for file in files:
                    pohaiImgList.append(os.path.join(root, file))
            if pohaiImgList == []:
                continue
            else:
                break
        if len(pohaiImgList) == 1:
            pohaiImg = pohaiImgList[0]
        else:
            pohaiImg = pohaiImgList[random.randint(0, len(pohaiImgList) - 1)]
        await pohai.finish(
            Message(f"""[CQ:image,file=base64://{str(image_to_base64_gif(f"{pohaiImg}"), encoding='utf-8')}]"""))
    else:
        func = func.replace("迫害", "").replace("ph", "").replace("pohai", "")
        id = func.replace(" ", '')
        isFindId = False
        for i in pohaiList:
            if id in i.split(','):
                id = i
                isFindId = True
        if isFindId == False:
            await pohai.finish(Message("[迫害]没有找到相应迫害人员"))
        pohaiImgList = []
        for root, dirs, files in os.walk(rf"src\static\images\pohai\{id}"):
            for file in files:
                pohaiImgList.append(os.path.join(root, file))
        await pohai.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64_gif(f"{pohaiImgList[random.randint(0, len(pohaiImgList) - 1)]}"), encoding='utf-8')}]"""))
    await pohai.finish()


# == 中二店铺
chumLocate = on_keyword(keywords={"中二店铺"}, permission=GROUP)
@chumLocate.handle()
async def chumLocate_main(matchers: chumLocate, event: GroupMessageEvent):
    if len(str(event.get_message()).replace('中二店铺', '').replace('中二店铺', '').split()) < 1:
        await chumLocate.finish()
    locate = str(event.get_message()).replace('中二店铺', '').replace('中二店铺', '').split()
    locateDatas = requests.get('https://wc.wahlap.net/chunithm/rest/location').json()
    fDatas = []
    if len(locate) == 1:
        for line in locateDatas:
            if (locate[0] in line['address']) or (locate[0] in line['arcadeName']):
                fDatas.append(line)
    elif len(locate) == 2:
        tDatas = []
        for line in locateDatas:
            if (locate[0] in line['address']) or (locate[0] in line['arcadeName']):
                tDatas.append(line)
        for line in tDatas:
            if (locate[1] in line['address']) or (locate[1] in line['arcadeName']):
                fDatas.append(line)
        #logger.info(fDatas)
    else:
        await chumLocate.finish()
    if len(fDatas) == 0:
        await chumLocate.finish("[中二店铺]查询无果")
    msg = ""
    i = 1
    for line in fDatas:
        msg += f"""》》NO.{i}  {line['machineCount']}台  {line['arcadeName']}\n"""+f"""地址：{line['address']}"""+"\n"
        i += 1
    msg += "\n\nGenerate by fuBot"
    await chumLocate.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(TextToImg(msg)), encoding='utf-8')}]"""))
