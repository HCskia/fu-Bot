from nonebot.matcher import matchers
from nonebot.rule import *
from nonebot.adapters.onebot.v11 import *
from nonebot.utils import *
from nonebot import *
import nonebot
from nonebot import require
# === 前置导入 ====
from src.plugins.tools import *
from src.plugins.maimai.music import *
from src.plugins.maimai.functions import *
from src.plugins.maimai.B40generator import generate as B40generate
from src.plugins.maimai.B50generator import generate as B50generate

todayFu = on_command(cmd="今日fu", permission=GROUP)
@todayFu.handle()
async def todayFu_main(matchers: todayFu, event: GroupMessageEvent):
    foods = readJson(r'src\static\datas\eat.json')['eat']
    toDayYunShi = readJson(r'src\static\datas\todayFu.json')['今日运势']
    toDayGames = readJson(r'src\static\datas\todayFu.json')['今日游戏']
    mobilePos = readJson(r'src\static\datas\todayFu.json')['移动端地点']
    positons = readJson(r'src\static\datas\todayFu.json')['maimai黄金位']
    h = hash(int(event.user_id))
    lucky_num = h % 100
    ys_value = []
    for i in range(len(toDayYunShi)-1):
        ys_value.append(h & len(toDayYunShi)-1)
        h >>= 1
    toDayFuBodyText = f"""今天是{time.strftime("20%y-%m-%d", time.localtime(time.time()))}\n{event.sender.nickname}  -> 今日：\n幸运点数：{lucky_num}\n"""
    if lucky_num == 0:
        toDayFuBodyText += "倒  霉  蛋！哈哈哈\n"
    elif lucky_num < 10:
        toDayFuBodyText += "时运不周，不过也不要气馁呀~有小fufu陪你呀\n"
    elif lucky_num < 30:
        toDayFuBodyText += "今天运气不是很好，但是也是美好的一天呀！\n"
    elif lucky_num < 70:
        toDayFuBodyText += "今天是平静祥和的一天呢~\n"
    elif lucky_num < 90:
        toDayFuBodyText += "今天你的运气不错耶~~\n"
    elif lucky_num < 100:
        toDayFuBodyText += "哇~今天是好运的一天哦！\n"
    elif lucky_num == 100:
        toDayFuBodyText += "我超！欧洲狗快给爷爬！\n"
    i = [0,0,0,0,0]
    for j in range(0,2):
        i[3] = 0
        while 1:
            #logger.info(i)
            if i[1] > len(ys_value)-1:
                i[1] = i[1] - (h%(len(ys_value)-1))
                continue
            elif i[0] == ys_value[i[1]]:
                i[1] += 1
                continue
            i[0] = ys_value[i[1]]
            i[3] += 1
            if i[3] == 2:
                if i[4] == i[0]:
                    i[3] = 1
                    continue
                break
        i[4] = i[0]
        if j < 1:
            toDayFuBodyText += f'宜 {toDayYunShi[i[0]]["name"]}:{toDayYunShi[i[0]]["good"]}\n'
        else:
            toDayFuBodyText += f'忌 {toDayYunShi[i[0]]["name"]}:{toDayYunShi[i[0]]["bad"]}\n'

    toDayFuBodyText += f'\n今日推荐：\n今日美食：{foods[h % len(foods)]}\n今日推荐音游：{toDayGames[h % (len(toDayGames) - 1)]}\n移动端最佳地点：{mobilePos[h % (len(mobilePos) - 1)]}\nmaimai黄金位：{positons[h & (len(positons) - 1)]}\n'
    toDayFuBaseImg = Image.new("RGB", (1920, 1080), (255, 255, 255))
    toDayFuBaseImgDraw = ImageDraw.Draw(toDayFuBaseImg)
    toDayFuBodyTextSize = toDayFuBaseImgDraw.multiline_textsize(toDayFuBodyText, font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15))

    toDayFuMaiText = "\n今日maimai金曲：\n"
    songs = h % len(total_list)
    music = total_list[songs]
    try:
        cover = Image.open(rf"src\static\images\maimai\covers\{music.id}.jpg").convert("RGBA")
    except:
        cover = Image.open(rf"src\static\images\maimai\covers\0.jpg")
    cover = cover.resize((200, 200))
    toDayFuMaiText += song_txt2(music)
    toDayFuMaiTextSize = toDayFuBaseImgDraw.multiline_textsize(toDayFuMaiText, font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15))

    toDayFuBaseImg = toDayFuBaseImg.resize((toDayFuBodyTextSize[0] + 10, toDayFuBodyTextSize[1] + toDayFuMaiTextSize[1] + 210))
    toDayFuBaseImgDraw = ImageDraw.Draw(toDayFuBaseImg)
    toDayFuBodyTextSize = toDayFuBaseImgDraw.multiline_textsize(toDayFuBodyText, font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15))

    toDayFuBaseImgDraw.text((1, 1), toDayFuBodyText, font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15), fill="#000000")
    toDayFuBaseImgDraw.text((1, toDayFuBodyTextSize[1]), str(toDayFuMaiText), font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15), fill="#000000")
    toDayFuBaseImg.paste(cover, (1, toDayFuBodyTextSize[1] + 80), cover)
    await todayFu.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(toDayFuBaseImg), encoding='utf-8')}]"""))


# == B40 | B50
generateB40 = on_command(cmd="b40", permission=GROUP)
@generateB40.handle()
async def generateB40_main(matchers: generateB40, event: GroupMessageEvent):
    msgGroup = str(event.get_message()).replace('b40', '').split()
    if len(msgGroup) >= 2 and msgGroup[0] == 'qq':
        payload = {'qq': str(msgGroup[1])}
    elif len(msgGroup) >= 1:
        payload = {'username': msgGroup[0]}  # payload -> QQ
    else:
        payload = {'qq': str(event.user_id)}
    try:
        B40Img, success, rating = await B40generate(payload)
    except aiohttp.client.ClientConnectorError:
        await generateB40.finish("[b40]发生错误：\n访问查分器服务器超时！")
        return 0
    except Exception as e:
        await generateB40.finish(f"[b40]发生错误：\n{e}")
        return 0
    if success == 400:
        await generateB40.finish("[b40]没有找到这位玩家呢，请确保此玩家的用户名和查分器中的用户名相同呀。\n如果还没绑定的话请到：https://www.diving-fish.com/maimaidx/prober/")
    elif success == 403:
        await generateB40.finish("[b40]这位玩家好像不让别人查他的分数呢~")
    else:
        await generateB40.finish(Message(f"[CQ:reply,id={event.message_id}]\n" + f"[b40][CQ:at,qq={event.user_id}]\n" + f"""[CQ:image,file=base64://{str(image_to_base64(B40Img), encoding='utf-8')}]"""))

generateB50 = on_command(cmd="b50", permission=GROUP)
@generateB50.handle()
async def generateB50_main(matchers: generateB50, event: GroupMessageEvent):
    msgGroup = str(event.get_message()).replace('b50', '').split()
    if len(msgGroup) >= 2 and msgGroup[0] == 'qq':
        payload = {'qq': str(msgGroup[1]), 'b50':  True}
    elif len(msgGroup) >= 1:
        payload = {'username': msgGroup[0], 'b50':  True}
    else:
        payload = {'qq': str(event.user_id), 'b50':  True}
    try:
        B50Img, success, rating = await B50generate(payload)
    except aiohttp.client.ClientConnectorError:
        await generateB40.finish("[b50]发生错误：\n访问查分器服务器超时！")
        return 0
    # except Exception as e:
    #     await generateB40.finish(f"[b50]发生错误：\n{e}")
    #     return 0
    if success == 400:
        await generateB40.finish("[b50]没有找到这位玩家呢，请确保此玩家的用户名和查分器中的用户名相同呀。\n如果还没绑定的话请到：https://www.diving-fish.com/maimaidx/prober/")
    elif success == 403:
        await generateB40.finish("[b50]这位玩家好像不让别人查他的分数呢~")
    else:
        await generateB40.finish(Message(f"[CQ:reply,id={event.message_id}]\n" + f"[b50][CQ:at,qq={event.user_id}]\n" + f"""[CQ:image,file=base64://{str(image_to_base64(B50Img), encoding='utf-8')}]"""))


# == 分数列表
scoreList = on_keyword(keywords={"分数列表"})
@scoreList.handle()
async def scoreList_main(matchers: scoreList, event: GroupMessageEvent):
    levelIndexToLabel = {0: "Basic", 1: "Advanced", 2: "Expert", 3: "Master", 4: "Re:MASTER"}
    parm = str(event.get_message()).replace("分数列表", "").split()
    level = None
    page = None
    if len(parm) == 1:
        level = parm[0]
    elif len(parm) == 2:
        level = parm[0]
        page = parm[1]
    else:
        await scoreList.finish(Message("[分数列表]参数错误！"))
    fuBot: Bot = nonebot.get_bots().get(str(event.self_id), None)
    payload = {'qq': event.user_id, 'version': allVersion}
    nickName = (await fuBot.get_stranger_info(user_id=event.user_id))['nickname']
    prefix = f"{nickName}的< {level} >分数列表：\n"
    if page == None:
        page = '1'
    try:
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/plate",json=payload) as resp:
            fData = []
            for line in sorted((await resp.json())['verlist'], key=lambda x: x['achievements'], reverse=True):
                line['level_label'] = levelIndexToLabel[line['level_index']]
                if line['level'] == level:
                    fData.append(line)
    except:
        await scoreList.finish("[分数列表]看起来您并没有绑定查分器到QQ捏，请到https://www.diving-fish.com/maimaidx/prober/绑定此QQ再使用功能哦。")
    try:
        fImg = generateScoreListImg(get40Data(fData, page), prefix, getPages(len(fData), page))
    except Exception as e:
        await scoreList.finish(f"[分数列表]发生错误：\n{e}")
        return 0
    await scoreList.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(fImg), encoding='utf-8')}]"""))


# == 定数算分
dsToRa = on_keyword(keywords={"定数算分"}, permission=GROUP)
@dsToRa.handle()
async def dsToRa_main(matchers: dsToRa, event: GroupMessageEvent):
    parm = str(event.get_message()).replace("定数算分", "").split()
    if not (len(parm) >= 2):
        await dsToRa.finish()
    await dsToRa.finish(f"[定数算分]定数{float(parm[0])}且分数为{float(parm[1])}的单曲ra为{computeRaB40(float(parm[0]), float(parm[1]))}左右")

# == 分算定数
raToDs = on_keyword(keywords={"分算定数"}, permission=GROUP)
@raToDs.handle()
async def raToDs_main(matchers: raToDs, event: GroupMessageEvent):
    parm = str(event.get_message()).replace("分算定数", "").split()
    if not (len(parm) >= 1):
        await raToDs.finish()
    ds = 1.0
    fmsg = "[分算定数] Generate by fuBot：\n"
    while (True):
        achievements = 97.0
        while (True):
            if achievements > 100.5:
                break
            rating = round(computeRaB40(ds, achievements), 1)
            if float(parm[0]) <= rating and rating <= (float(parm[0]) + 2):
                fmsg += (f"定数{round(ds, 1)},分数{round(achievements, 1)},单曲Ra  {floor(rating)}\n")
            achievements += 0.5
        ds += 0.1
        if ds > 15:
            break
    await raToDs.send(Message(f"""[CQ:image,file=base64://{str(image_to_base64(TextToImg(fmsg)), encoding='utf-8')}]"""))


# == 随歌
rollMusics = on_regex(r"^随个(?:dx|sd|标准)?[绿黄红紫白]?[0-9]+\+?", permission=GROUP)
@rollMusics.handle()
async def rollMusics_main(matchers: rollMusics, event: GroupMessageEvent):
    res = re.match("随个((?:dx|sd|标准))?([绿黄红紫白]?)([0-9]+\+?)", str(event.get_message()).lower())
    try:
        if res.groups()[0] == "dx":
            tp = ["DX"]
        elif res.groups()[0] == "sd" or res.groups()[0] == "标准":
            tp = ["SD"]
        else:
            tp = ["SD", "DX"]
        level = res.groups()[2]
        if res.groups()[1] == "":
            music_data = total_list.filter(level=level, type=tp)
        else:
            music_data = total_list.filter(level=level, diff=['绿黄红紫白'.index(res.groups()[1])], type=tp)
    except Exception as e:
        await rollMusics.finish(f"[随歌]发生错误：\n{e}")
        return 0
    await rollMusics.finish(Message(song_txt(music_data.random())))


# == 搜曲
searchMusic = on_regex(r"^搜曲.+", permission=GROUP)
@searchMusic.handle()
async def searchMusic_main(matchers: searchMusic, event: GroupMessageEvent):
    name = re.match("搜曲(.+)", str(event.get_message())).groups()[0].strip()
    if name == "":
        return
    res = total_list.filter(title_search=name)
    await searchMusic.finish(f"{music['id']}. {music['title']}\n" for music in res)


# == 查谱
searchNoteInfos = on_regex(r"^([绿黄红紫白]?)id([0-9]+)", permission=GROUP)
@searchNoteInfos.handle()
async def searchNoteInfos_main(matchers: searchNoteInfos, event: GroupMessageEvent):
    parms = re.match("([绿黄红紫白]?)id([0-9]+)", str(event.get_message())).groups()
    level_labels = ['绿', '黄', '红', '紫', '白']
    isCoverAvailable = True
    try:
        file = getSongCover(parms[1])
    except:
        file = None
        isCoverAvailable = False
    if parms[0] != "":
        try:
            level_index = level_labels.index(parms[0])
            level_name = ['Basic', 'Advanced', 'Expert', 'Master', 'Re: MASTER']
            musicId = parms[1]
            music = total_list.by_id(musicId)
            chart = music['charts'][level_index]
            ds = music['ds'][level_index]
            level = music['level'][level_index]
            if len(chart['notes']) == 4:
                msgText = f'''{level_name[level_index]} {level}({ds})\n——TAP: {chart['notes'][0]}\n——HOLD: {chart['notes'][1]}\n——SLIDE: {chart['notes'][2]}\n——BREAK: {chart['notes'][3]}\n——谱师: {chart['charter']}'''
            else:
                msgText = f'''{level_name[level_index]} {level}({ds})\n——TAP: {chart['notes'][0]}\n——HOLD: {chart['notes'][1]}\n——SLIDE: {chart['notes'][2]}\n——TOUCH: {chart['notes'][3]}\n——BREAK: {chart['notes'][4]}\n——谱师: {chart['charter']}'''
            if isCoverAvailable:
                msg = Message(f"[CQ:reply,id={event.message_id}]\n" + f"{music['id']}. {music['title']}\n" + f"""[CQ:image,file=base64://{str(image_to_base64(file), encoding='utf-8')}]""" + f'{msgText}')
            else:
                msg = Message(f"[CQ:reply,id={event.message_id}]\n" + f"{music['id']}. {music['title']}\n" + f"\n封面错误\n\n" + f'{msgText}')
        except Exception as e:
            await searchNoteInfos.finish(f"[查谱]发生错误：\n{e}")
            return 0
        await searchNoteInfos.finish(msg)
    else:
        musicId = parms[1]
        music = total_list.by_id(musicId)
        try:
            if isCoverAvailable:
                msg = Message(f"[CQ:reply,id={event.message_id}]\n" + f"{music['id']}. {music['title']}\n" + f"""[CQ:image,file=base64://{str(image_to_base64(file), encoding='utf-8')}]""" + f"艺术家: {music['basic_info']['artist']}\n分类: {music['basic_info']['genre']}\nBPM: {music['basic_info']['bpm']}\n版本: {music['basic_info']['from']}\n难度: {str(music['ds']).replace(', ', '/')}")
            else:
                msg = Message(f"[CQ:reply,id={event.message_id}]\n" + f"{music['id']}. {music['title']}\n" + f"\n封面错误\n\n" + f"艺术家: {music['basic_info']['artist']}\n分类: {music['basic_info']['genre']}\nBPM: {music['basic_info']['bpm']}\n版本: {music['basic_info']['from']}\n难度: {str(music['ds']).replace(', ', '/')}")
        except Exception as e:
            await searchNoteInfos.finish(f"[查谱]发生错误：\n{e}")
            return 0
        await searchNoteInfos.finish(msg)


# == 谱面分数线
noteScoreLine = on_keyword(keywords={'谱面分数线'}, permission=GROUP)
@noteScoreLine.handle()
async def noteScoreLine_main(matchers: noteScoreLine, event: GroupMessageEvent):
    parms = str(event.get_message()).replace('谱面分数线', "").split()
    if len(parms) == 1 and (parms[0] == '帮助' or parms[0] == 'help'):
        await noteScoreLine.finish("#谱面分数线 <难度+歌曲id> <分数线> ->\n例如：谱面分数线 紫799 100\n以下为 TAP GREAT 的对应表：\n    GREAT/GOOD/MISS\nTAP     1/2.5/5\nHOLD    2/5/10\nSLIDE   3/7.5/15\nTOUCH   1/2.5/5\nBREAK   5/12.5/25(外加200落)")
    elif len(parms) == 2:
        try:
            parms_s = re.match("([绿黄红紫白])(id)?([0-9]+)", parms[0]).groups()
            level_labels = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:MASTER']
            level_index = ['绿', '黄', '红', '紫', '白'].index(parms_s[0])
            chart_id = parms_s[2]
            line = float(parms[1])
            music = total_list.by_id(chart_id)
            chart: Dict[Any] = music['charts'][level_index]
            total_score = 500 * int(chart['notes'][0]) + int(chart['notes'][2]) * 1500 + int(chart['notes'][1]) * 1000 + (int(chart['notes'][3]) if len(chart['notes']) == 5 else 0) * 500 + int(chart['notes'][-1]) * 2500
            break_bonus = 0.01 / int(chart['notes'][-1])
            break_50_reduce = total_score * break_bonus / 4
            reduce = 101 - line
            if reduce <= 0 or reduce >= 101:
                raise ValueError
        except Exception as e:
            await noteScoreLine.finish(f"[谱面分数线]发生错误：\n{e}")
            return 0
        await noteScoreLine.finish(f'''->{music['title']} {level_labels[level_index]}\n——分数线 {line}% 最大 TAP GREAT 数为 {(total_score * reduce / 10000):.2f}(每个-{10000 / total_score:.4f}%)\n——BREAK 50落(一共{int(chart['notes'][-1])}个)等价于 {(break_50_reduce / 100):.3f} 个 TAP GREAT(-{break_50_reduce / total_score * 100:.4f}%)''')


# == 添加别名
addMusicAlias = on_keyword(keywords={"添加别名"}, permission=GROUP)
@addMusicAlias.handle()
async def addMusicAlias_main(matchers: addMusicAlias, event: GroupMessageEvent):
    if len(str(event.get_message()).split()) < 3:
        await addMusicAlias.finish()
    songData = str(event.get_message()).replace("添加别名", '').split()
    songID = songData[0]
    songAlias = songData[1]
    result = readJson(r"src\static\datas\musicAliases.json")
    for line in result:
        if songAlias in line['alias']:
            await addMusicAlias.finish("[添加别名]别名冲突！已经有别名相同的歌曲了。")
    ans = False
    for i in result:
        if songID == str(i['id']):
            i['alias'].append(songAlias)
            ans = True
            break
    if ans == False:
        music = total_list.by_id(songID)
        if music == None:
            await addMusicAlias.finish("[添加别名]没有查询到相应id的歌曲！")
        songID = music['id']
        songTitle = music['title']
        result.append({"id": songID, "title": f"{songTitle}", "alias": [f"{songAlias}"]})
    writeJson(r"src\static\datas\musicAliases.json", result)
    await addMusicAlias.finish("[添加别名]添加别名成功！")


# == 删除别名
delMusicAlias = on_keyword(keywords={"删除别名"}, permission=GROUP)
@delMusicAlias.handle()
async def delMusicAlias_main(matchers: delMusicAlias, event: GroupMessageEvent):
    if len(str(event.get_message()).split()) < 3:
        await delMusicAlias.finish()
    songData = str(event.get_message()).replace("删除别名",'').split()
    songID = songData[0]
    songAlias = songData[1]
    result = readJson(r"src\static\datas\musicAliases.json")
    ans = False
    for line in result:
        if songAlias in line['alias']:
            if songID == str(line['id']):
                alias = []
                for t in line['alias']:
                    if songAlias != t:
                        alias.append(t)
                line['alias'] = alias
                ans = True
                break
    if ans == True:
        writeJson(r"src\static\datas\musicAliases.json", result)
        await delMusicAlias.finish(Message("[删除别名]删除别名成功！"))
    else:
        await delMusicAlias.finish(Message("[删除别名]没有在id信息中找到这个别名！"))
    await delMusicAlias.finish(Message("[删除别名]没有查询到相应id的歌曲！"))


# == 别名查歌
aliasFindMusic = on_regex(r".+是什么歌", permission=GROUP)
@aliasFindMusic.handle()
async def aliasFindMusic_main(matchers: aliasFindMusic, event: GroupMessageEvent):
    name = re.match("(.+)是什么歌", str(event.get_message())).groups()[0].strip().lower()
    result = readJson(r"src\static\datas\musicAliases.json")
    for line in result:
        for tline in line['alias']:
            if name == tline:
                songID = str(line['id'])
                music = total_list.by_id(songID)
                await aliasFindMusic.finish(Message("[别名查歌]：\n" + song_txt(music) + "\n——该歌曲的全部别名：\n" + str(line['alias'])))
    await aliasFindMusic.finish("[别名查歌]没有查到相应歌曲！\n——可以用 '添加别名 <id> <别名> '来添加别名哦!")


# == 等级天梯图
ladderDiagram = on_regex(r"^[0-9]+\+?天梯图", permission=GROUP)
@ladderDiagram.handle()
async def ladderDiagram_main(matchers: ladderDiagram, event: GroupMessageEvent):
    level = re.match("([0-9]+\+?)天梯图", str(event.get_message())).groups()[0]
    try:
        musicDatas = requests.get(f'{music_data}').json()
    except requests.exceptions.ConnectionError:
        await ladderDiagram.finish(Message("[谱面等级天梯图]www.diving-fish.com服务器响应超时"))
        return 0
    levelDatas = "["
    indexToLevel = {'0': "Basic",'1': "Advanced",'2': "Expert",'3': "Master",'4': "Re:MASTER"}
    levelToColor = {'Basic': (153, 255, 102),
                    'Advanced': (255, 242, 102),
                    'Expert': (255, 55, 55),
                    'Master': (191, 55, 255),
                    'Re:MASTER': (238, 202, 255)}
    temp = None
    for data in musicDatas:
        if level in data['level']:
            thisLevel = level
            thisLevel = int(str(thisLevel).replace("+", ""))
            for tds in sorted(data['ds'], reverse=False):
                levelLabel = indexToLevel[f"{data['ds'].index(tds)}"]
                if temp == tds:
                    levelLabel = indexToLevel[f"{data['ds'].index(tds)+1}"]
                temp = tds
                if '+' in level:
                    if float(tds) >= (thisLevel + 0.7) and int(thisLevel) == int(tds):
                        levelDatas += f"""{{"id":"{data['id']}","level":"{level}","title":"{str(data['title']).replace('"', "'")}","level_label":"{levelLabel}","type":"{data['type']}","bs":{float(tds)}}},"""
                else:
                    if int(thisLevel) == int(tds):
                        if float(tds) >= (int(thisLevel)+0.7):
                            continue
                        if float(tds) >= thisLevel:
                            levelDatas += f"""{{"id":"{data['id']}","level":"{level}","title":"{str(data['title']).replace('"', "'")}","level_label":"{levelLabel}","type":"{data['type']}","bs":{float(tds)}}},"""
    levelDatas += "]"
    levelDatas = levelDatas.replace(",]","]")
    levelDatas = json.loads(levelDatas)
    levelDatas = sorted(levelDatas, key=lambda x:x['bs'], reverse=True)
    titleFront = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 10)
    idFront = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15)
    levelFront = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 30)
    lineWidth = 1
    lineHeight = 1
    tempBase = (levelDatas[0])['bs']
    for data in levelDatas:
        lineWidth += 1
        if lineWidth == 8 or tempBase!=data['bs']:
            lineWidth = 1
            lineHeight += 1
            tempBase = data['bs']
    tImg = Image.new('RGB', (920, 100*lineHeight), color=(255, 255, 255))
    DXimg = Image.open(r"src\static\images\maimai\UI_CMN_Name_DX.png").resize((25,13))
    lineWidth = 0
    lineHeight = 1
    rowsHeight = 1
    rows = 1
    tempBase = (levelDatas[0])['bs']
    for data in levelDatas:
        lineWidth += 1
        if lineWidth == 8 or tempBase != data['bs']:
            rows += 1
            rowsHeight += 1
            if tempBase != data['bs']:
                baseText = Image.new('RGB', (120, 100 * (rowsHeight - 1)), color=(random.randint(179,255), random.randint(0,255), random.randint(0,255)))
                baseTextDraw = ImageDraw.Draw(baseText)
                baseTextWidth = 60 - (levelFront.getsize(f"{tempBase}")[0]) / 2
                baseTextHeight = (100*(rowsHeight-1))/2 - 20
                baseTextDraw.text((baseTextWidth, baseTextHeight), f"{tempBase}", font=levelFront, fill=(0, 0, 0))
                tImg.paste(baseText, (0, (100 * (lineHeight - rowsHeight + 1))))
                rowsHeight = 1
                rows = 1
                tempBase = data['bs']
            lineWidth = 1
            lineHeight += 1
        try:
            cover = Image.open(rf"src\static\images\maimai\covers\{data['id']}.jpg")
            cover = cover.resize((90, 90))
        except FileNotFoundError:
            try:
                coverDownload = requests.get(f"https://www.diving-fish.com/covers/{data['id']}.jpg")
                with open(rf"src\static\images\maimai\covers\{data['id']}.jpg", 'wb+')as f:
                    f.write(coverDownload.content)
                    f.close()
                logger.info(f"[maimaiDX天梯图]歌曲{data['id']}封面下载成功！")
                cover = Image.open(rf"src\static\images\maimai\covers\{data['id']}.jpg")
                cover = cover.resize((90, 90))
            except:
                os.remove(rf"src\static\images\maimai\covers\{data['id']}.jpg")
                logger.info(f"[maimaiDX天梯图]歌曲{data['id']}暂无封面")
                cover = Image.new('RGB', (90, 90), color=(255, 255, 255))
                tempDraw = ImageDraw.Draw(cover)
                tempDraw.text(((50 - (titleFront.getsize(f"{data['title']}")[0] / 2)),40), f"{data['title']}", font=titleFront, fill=(0, 0, 0))
        tempDraw = ImageDraw.Draw(cover)
        try:
            tempDraw.text((3, 3), text=f"{data['id']}", font=idFront, fill=(random.randint(0, 130), random.randint(200, 230), random.randint(200, 250)))
        except:
            pass
        coverBg = Image.new('RGB', (100,100), color=levelToColor[f"{data['level_label']}"])
        coverBg.paste(cover, (5, 5))
        if data['type'] == "DX":
            coverBg.paste(DXimg, (70, 80))
        tImg.paste(coverBg, ((120+100*(lineWidth-1)), (100*(lineHeight-1))))
    baseText = Image.new('RGB', (120, 100 * rowsHeight), color=(random.randint(179,255), random.randint(0,255), random.randint(0,255)))
    baseTextDraw = ImageDraw.Draw(baseText)
    baseTextWidth =60-(levelFront.getsize(f"{tempBase}")[0])/2
    baseTextHeight = (100*rowsHeight)/2 - 20
    baseTextDraw.text((baseTextWidth,baseTextHeight), f"{tempBase}", font=levelFront, fill=(0, 0, 0))
    tImg.paste(baseText, (0, (100 * (lineHeight - rowsHeight))))
    responseTextDraw = ImageDraw.Draw(tImg)
    responseTextDraw.text((0,tImg.height-20), f"Generate by fuBot", font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15), fill=(0, 0, 0))
    await ladderDiagram.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(tImg), encoding='utf-8')}]"""))


# == x代完成表
SongVersion = on_regex(r".+代", permission=GROUP)
@SongVersion.handle()#['真','超','檄','橙','晓','桃','樱','紫','堇','白','雪','辉','舞','熊','华','爽','煌']
async def SongVersion_main(matchers: SongVersion, event: GroupMessageEvent):
    rawMsg = str(event.get_message())
    Verson = str(re.match("(.+)代", str(event.get_message())).groups()[0].strip().lower()).replace('代', "").replace("谱面表","").replace("完成表","")
    zVersion = ['maimai', 'maimai PLUS']
    if "谱面表" in rawMsg:
        playerData = None
        if Verson not in maimaiVersion:
            await SongVersion.finish()
        if Verson != '舞':
            versionTitle = plateToVersion[f'{Verson}']
        else:
            versionTitle = '舞'
        try:
            musicDatas = requests.get(f'{music_data}').json()
        except requests.exceptions.ConnectionError:
            await SongVersion.finish(Message("[X代完成表]www.diving-fish.com服务器响应超时"))
            return 0
        versionData = []
        for tdata in musicDatas:
            if Verson == '舞':
                if tdata['basic_info']['from'] in ['maimai','maimai PLUS','maimai GreeN','maimai GreeN PLUS','maimai ORANGE','maimai ORANGE PLUS','maimai PiNK','maimai PiNK PLUS','maimai MURASAKi','maimai MURASAKi PLUS','maimai MiLK','MiLK PLUS','maimai FiNALE']:
                    versionData.append(tdata)
            elif Verson == '真':
                if tdata['basic_info']['from'] in ['maimai','maimai PLUS']:
                    versionData.append(tdata)
            else:
                if tdata['basic_info']['from'] == versionTitle:
                    versionData.append(tdata)
        Img = generateVersionList(Verson,versionData,playerData)
        await SongVersion.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(Img), encoding='utf-8')}]"""))
    elif "完成表" in rawMsg:
        playerData = None
        if Verson not in maimaiVersion:
            await SongVersion.finish()
        if Verson == '真':
            payload = {'qq': event.user_id, 'version': zVersion}
        elif Verson != '舞':
            versionTitle = plateToVersion[f'{Verson}']
            payload = {'qq': event.user_id, 'version': [versionTitle]}
        else:
            tVersion = ['maimai', 'maimai PLUS', 'maimai GreeN', 'maimai GreeN PLUS', 'maimai ORANGE',
                        'maimai ORANGE PLUS', 'maimai PiNK', 'maimai PiNK PLUS', 'maimai MURASAKi',
                        'maimai MURASAKi PLUS', 'maimai MiLK', 'MiLK PLUS', 'maimai FiNALE']
            payload = {'qq': event.user_id, 'version': tVersion}
            versionTitle = '舞'
        try:
            musicDatas = requests.get(f'{music_data}').json()
        except requests.exceptions.ConnectionError:
            await scoreList.finish(Message("[X代完成表]www.diving-fish.com服务器响应超时"))
            return 0
        versionData = []
        for tdata in musicDatas:
            if Verson == '舞':
                if tdata['basic_info']['from'] in tVersion:
                    versionData.append(tdata)
            elif Verson == '真':
                if tdata['basic_info']['from'] in zVersion:
                    versionData.append(tdata)
            else:
                if tdata['basic_info']['from'] == versionTitle:
                    versionData.append(tdata)

        try:
            async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/plate",json=payload) as resp:
                playerData = []
                for line in sorted((await resp.json())['verlist'], key=lambda x: x['achievements'], reverse=True):
                    if Verson == '舞':
                        if line['level_index'] == 4:
                            playerData.append(line)
                        else:
                            continue
                    else:
                        playerData.append(line)
        except:
            await scoreList.finish(Message("[X代完成表]看起来您并没有绑定查分器到QQ\n请到https://www.diving-fish.com/maimaidx/prober/绑定此QQ再使用功能哦。"))
        Img = generateVersionList(Verson, versionData, playerData)
        await SongVersion.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(Img), encoding='utf-8')}]"""))
    else:
        await SongVersion.finish()


# == DX店铺
dxLocate = on_keyword(keywords={"dx店铺",'DX店铺'}, permission=GROUP)
@dxLocate.handle()
async def dxLocate_main(matchers: dxLocate, event: GroupMessageEvent):
    if len(str(event.get_message()).replace('dx店铺', '').replace('DX店铺', '').split()) < 1:
        await dxLocate.finish()
    locate = str(event.get_message()).replace('dx店铺', '').replace('DX店铺', '').split()
    locateDatas = requests.get('http://wc.wahlap.net/maidx/rest/location').json()
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
        await dxLocate.finish()
    if len(fDatas) == 0:
        await dxLocate.finish("[dx店铺]查询无果")
    msg = ""
    i = 1
    for line in fDatas:
        msg += f"""》》NO.{i}  {line['machineCount']}台  {line['arcadeName']}\n"""+f"""地址：{line['address']}"""+"\n"
        i += 1
    msg += "\n\nGenerate by fuBot"
    await dxLocate.finish(Message(f"""[CQ:image,file=base64://{str(image_to_base64(TextToImg(msg)), encoding='utf-8')}]"""))