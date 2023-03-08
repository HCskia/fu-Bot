import os
from collections import defaultdict
#=====
import time
import datetime
from math import floor
import re
#=====
from src.plugins.maimai.music import *
from src.plugins.tools import *
#=====
import nonebot
import aiohttp
import math
#=====
from nonebot import on_regex, on_keyword
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Bot,Message,GROUP,GroupMessageEvent,PrivateMessageEvent
from nonebot.log import logger
# 变量
#picPath = "src/plugins/maimai/pic"
processPath = "src/plugins/maimai/pic/Process"
dataPath = r"src\static\datas"
indexToLevel = {'0': "Basic", '1': "Advanced", '2': "Expert", '3': "Master", '4': "Re:MASTER"}
baseNameToFile = {'d': "UI_GAM_Rank_D.png",
                      'c': "UI_GAM_Rank_C.png",
                      'b': "UI_GAM_Rank_B.png",
                      'bb': "UI_GAM_Rank_BB.png",
                      'bbb': "UI_GAM_Rank_BBB.png",
                      'a': "UI_GAM_Rank_A.png",
                      'aa': "UI_GAM_Rank_AA.png",
                      'aaa': "UI_GAM_Rank_AAA.png",
                      's': "UI_GAM_Rank_S.png",
                      'sp': "UI_GAM_Rank_Sp.png",
                      'ss': "UI_GAM_Rank_SS.png",
                      'ssp': "UI_GAM_Rank_SSp.png",
                      'sss': "UI_GAM_Rank_SSS.png",
                      'sssp': "UI_GAM_Rank_SSSp.png"}
maimaiVersion = ['真','超','檄','橙','晓','桃','樱','紫','堇','白','雪','辉','舞','熊','华','爽','煌']
VersionTrans = {    '真': "maimai",##maimai PLUS
                    "超": "maimai GreeN",
                    "檄": "maimai GreeN PLUS",
                    "橙": "maimai ORANGE",
                    "晓": "maimai ORANGE PLUS",
                    "桃": "maimai PiNK",
                    "樱": "maimai PiNK PLUS",
                    "紫": "maimai MURASAKi",
                    "堇": "maimai MURASAKi PLUS",
                    "白": "maimai MiLK",
                    "雪": "MiLK PLUS",
                    "辉": "maimai FiNALE",
                    "熊": "maimai でらっくす",
                    "华": "maimai でらっくす",
                    "爽": "maimai でらっくす Splash",
                    '煌': 'maimai でらっくす Splash PLUS',
                    '宙': 'maimai でらっくす Universe',
                    '星': 'maimai でらっくす Universe PLUS'
                    }
plateToVersion = {
    '初': 'maimai',
    '真': 'maimai PLUS',
    '超': 'maimai GreeN',
    '檄': 'maimai GreeN PLUS',
    '橙': 'maimai ORANGE',
    '暁': 'maimai ORANGE PLUS',
    '晓': 'maimai ORANGE PLUS',
    '桃': 'maimai PiNK',
    '櫻': 'maimai PiNK PLUS',
    '樱': 'maimai PiNK PLUS',
    '紫': 'maimai MURASAKi',
    '菫': 'maimai MURASAKi PLUS',
    '堇': 'maimai MURASAKi PLUS',
    '白': 'maimai MiLK',
    '雪': 'MiLK PLUS',
    '輝': 'maimai FiNALE',
    '辉': 'maimai FiNALE',
    '熊': 'maimai でらっくす',
    # '華': 'maimai でらっくす PLUS',
    '華': 'maimai でらっくす',
    # '华': 'maimai でらっくす PLUS',
    '华': 'maimai でらっくす',
    '爽': 'maimai でらっくす Splash',
    '煌': 'maimai でらっくす Splash,',
    '宙': 'maimai でらっくす Universe',
    '星': 'maimai でらっくす Universe PLUS'
}
allPlateToVersion = {
    '初': 'maimai',
    '真': 'maimai PLUS',
    '超': 'maimai GreeN',
    '檄': 'maimai GreeN PLUS',
    '橙': 'maimai ORANGE',
    '暁': 'maimai ORANGE PLUS',
    '晓': 'maimai ORANGE PLUS',
    '桃': 'maimai PiNK',
    '櫻': 'maimai PiNK PLUS',
    '樱': 'maimai PiNK PLUS',
    '紫': 'maimai MURASAKi',
    '菫': 'maimai MURASAKi PLUS',
    '堇': 'maimai MURASAKi PLUS',
    '白': 'maimai MiLK',
    '雪': 'MiLK PLUS',
    '輝': 'maimai FiNALE',
    '辉': 'maimai FiNALE',
    '熊': 'maimai でらっくす',
    # '華': 'maimai でらっくす PLUS',
    '華': 'maimai でらっくす',
    # '华': 'maimai でらっくす PLUS',
    '华': 'maimai でらっくす',
    '爽': 'maimai でらっくす Splash',
    '煌': 'maimai でらっくす Splash PLUS',
    '宙': 'maimai でらっくす Universe',
    '星': 'maimai でらっくす Universe PLUS'
}
allVersion = list(set(version for version in list(allPlateToVersion.values())[:]))
#=====
def hash(qq: int):
    days = int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
        time.strftime("%m", time.localtime(time.time()))) + 77
    return (days * qq) >> 8



def achieveToRank(achievements):
    if achievements > 100.5:
        return 'sssp'
    elif achievements > 100:
        return 'sss'
    elif achievements > 99.5:
        return 'ssp'
    elif achievements > 99:
        return 'ss'
    elif achievements > 98:
        return 'sp'
    elif achievements > 97:
        return 's'
    elif achievements > 94:
        return 'aaa'
    elif achievements > 90:
        return 'aa'
    elif achievements > 80:
        return 'a'
    elif achievements > 75:
        return 'bbb'
    elif achievements > 70:
        return 'bb'
    elif achievements > 60:
        return 'b'
    elif achievements > 50:
        return 'c'
    else:
        return 'd'



def getSongCover(songId):
    try:
        cover = Image.open(rf"src\static\images\maimai\covers\{songId}.jpg")
    except FileNotFoundError:
        try:
            coverDownload = requests.get(f"https://www.diving-fish.com/covers/{songId}.jpg")
            with open(rf"src\static\images\maimai\covers\{songId}.jpg", 'wb+')as f:
                f.write(coverDownload.content)
                f.close()
            logger.info(f"[maimaiDX]歌曲{songId}封面下载成功！")
            cover = Image.open(rf"src\static\images\maimai\covers\{songId}.jpg")
        except:
            try:
                os.remove(rf"src\static\images\maimai\covers\{songId}.jpg")
            except:
                pass
            logger.info(f"[maimaiDX]歌曲{songId}暂无封面")
            cover = None
    return cover



def song_txt2(music: Music):
    return f"""{music.id}. {music.title}\n歌曲难度：{music.ds}"""


def song_txt(music: Music):
    return Message(f"{music.id}. {music.title}\n"+f"""[CQ:image,file=base64://{str(image_to_base64(getSongCover(music.id)), encoding='utf-8')}]"""+f"{str(music.ds).replace(', ','/')}")



def inner_level_q(ds1, ds2=None):
    result_set = []
    diff_label = ['Bas', 'Adv', 'Exp', 'Mst', 'ReM']
    if ds2 is not None:
        music_data = total_list.filter(ds=(ds1, ds2))
    else:
        music_data = total_list.filter(ds=ds1)
    for music in music_data:
        for i in music.diff:
            result_set.append((music['id'], music['title'], music['ds'][i], diff_label[i], music['level'][i]))
    return result_set

def computeRaB40(ds: float, achievement:float) -> int:
    baseRa = 14.0
    if achievement >= 50 and achievement < 60:
        baseRa = 5.0
    elif achievement < 70:
        baseRa = 6.0
    elif achievement < 75:
        baseRa = 7.0
    elif achievement < 80:
        baseRa = 7.5
    elif achievement < 90:
        baseRa = 8.0
    elif achievement < 94:
        baseRa = 9.0
    elif achievement < 97:
        baseRa = 9.4
    elif achievement < 98:
        baseRa = 10.0
    elif achievement < 99:
        baseRa = 11.0
    elif achievement < 99.5:
        baseRa = 12.0
    elif achievement < 99.99:
        baseRa = 13.0
    elif achievement < 100:
        baseRa = 13.25
    elif achievement < 100.5:
        baseRa = 13.5
    return math.floor(ds * (min(100.5, achievement) / 100) * baseRa)


def computeRaB50(ds: float, achievement:float) -> int:
    baseRa = 22.4
    if achievement < 50:
        baseRa = 7.0
    elif achievement < 60:
        baseRa = 8.0
    elif achievement < 70:
        baseRa = 9.6
    elif achievement < 75:
        baseRa = 11.2
    elif achievement < 80:
        baseRa = 12.0
    elif achievement < 90:
        baseRa = 13.6
    elif achievement < 94:
        baseRa = 15.2
    elif achievement < 97:
        baseRa = 16.8
    elif achievement < 98:
        baseRa = 20.0
    elif achievement < 99:
        baseRa = 20.3
    elif achievement < 99.5:
        baseRa = 20.8
    elif achievement < 100:
        baseRa = 21.1
    elif achievement < 100.5:
        baseRa = 21.6
    return math.floor(ds * (min(100.5, achievement) / 100) * baseRa)


def generateProcessImg(levelData,maxLen,prefix):
    processNameToFile = {'clear': "music_icon_clear.png",
                         's': "UI_GAM_Rank_S.png",
                         'sp': "UI_GAM_Rank_Sp.png",
                         'ss': "UI_GAM_Rank_SS.png",
                         'ssp': "UI_GAM_Rank_SSp.png",
                         'sss': "UI_GAM_Rank_SSS.png",
                         'sssp': "UI_GAM_Rank_SSSp.png",
                         'fc': "UI_MSS_MBase_Icon_FC.png",
                         'fcp': "UI_MSS_MBase_Icon_FCp.png",
                         'ap': "UI_MSS_MBase_Icon_AP.png",
                         'app': "UI_MSS_MBase_Icon_APp.png",
                         'fs': "UI_MSS_MBase_Icon_FS.png",
                         'fsp': "UI_MSS_MBase_Icon_FSp.png",
                         'fsd': "UI_MSS_MBase_Icon_FSD.png",
                         'fsdp': "UI_MSS_MBase_Icon_FSDp.png"}
    elm = ['clear','s','sp','ss','ssp','sss','sssp','fc','fcp','ap','app','fs','fsp','fsd','fsdp']
    timg = Image.new("RGB",(500,500),(255,255,255))
    font = ImageFont.truetype(r'src\static\Material\msyh.ttc', 24)
    tdraw = ImageDraw.Draw(timg)
    tdraw.text(((250-font.getsize(prefix)[0]/2), 0), prefix, font=font, fill=(0, 0, 0))

    top = 40
    count = 0
    for i in elm:
        iconImg = Image.open(f"{processPath}/{processNameToFile[f'{i}']}")
        timg.paste(iconImg,(20+(count*220),top),iconImg)
        text=f"""  ：{levelData[f'{i}']}/{maxLen}"""
        if int(levelData[f'{i}']) ==  maxLen:
            color = (255,0,0)
        else:
            color = (0, 0, 0)
        tdraw.text((100+(count*210),top+10), text, font=font, fill=color)

        count = count + 1
        if count == 2:
            top = top + 55
            count = 0
    #timg.show()
    return timg



def getLevelProcess(Data):
    clear = s = sp = ss = ssp = sss = sssp = fc = fcp = ap = app = fs = fsp = fsd = fsdp = 0
    for tData in Data:
        achievements = float(tData['achievements'])
        fullcombo = str(tData['fc'])
        fullsync = str(tData['fs'])
        if achievements >= 80:
            clear = clear + 1
        if achievements >= 97:
            s = s + 1
        if achievements >= 98:
            sp = sp + 1
        if achievements >= 99:
            ss = ss + 1
        if achievements >= 99.5:
            ssp = ssp + 1
        if achievements >= 100:
            sss = sss + 1
        if achievements >= 100.5:
            sssp = sssp + 1
        if fullcombo == 'fc':
            fc = fc + 1
        elif fullcombo == 'fcp':
            fc = fc + 1
            fcp = fcp + 1
        elif fullcombo == 'ap':
            fc = fc + 1
            fcp = fcp + 1
            ap = ap + 1
        elif fullcombo == 'app':
            fc = fc + 1
            fcp = fcp + 1
            ap = ap + 1
            app = app + 1
        if fullsync == 'fs':
            fs = fs + 1
        elif fullsync == 'fsp':
            fs = fs + 1
            fsp = fsp + 1
        elif fullsync == 'fsd':
            fs = fs + 1
            fsp = fsp + 1
            fsd = fsd + 1
        elif fullsync == 'fsdp':
            fs = fs + 1
            fsp = fsp + 1
            fsd = fsd + 1
            fsdp = fsdp + 1
    levelData = {'clear': clear, 's': s, 'sp': sp, 'ss': ss, 'ssp': ssp, 'sss': sss, 'sssp': sssp, 'fc': fc, 'fcp': fcp,'ap': ap, 'app': app, 'fs': fs, 'fsp': fsp, 'fsd': fsd, 'fsdp': fsdp}
    return levelData



def getLevelLen(level):
    len = 0
    musicDatas = requests.get(f'{music_data}').json()
    for data in musicDatas:
        if level in data['level']:
            for tlevel in data['level']:
                if tlevel == level:
                    len = len + 1
    return len



def getPages(len, page):
    maxPage = math.ceil(len / 40)
    if page == '0':
        return "ALL"
    if len <= 40:
        fPage = "1"
    elif int(page) > int(maxPage):
        return "ALL"
    else:
        fPage = f"{page}/ {maxPage}"
    return fPage



def get40Data(Data, page):
    if len(Data) <= 40:
        pass
    elif page == '0':
        pass
    elif int(page) > int(math.ceil(len(Data) / 40)):
        pass
    elif page == '1':
        Data = Data[0:41]
    elif page == '2':
        if len(Data) <= 2 * 40:
            Data = Data[1 * 40 + 1:len(Data)]
        else:
            Data = Data[1 * 40 + 1:2 * 40 + 1]
    elif page == '3':
        if len(Data) <= 3 * 40:
            Data = Data[2 * 40 + 1:len(Data)]
        else:
            Data = Data[2 * 40 + 1:3 * 40 + 1]
    elif page == '4':
        if len(Data) <= 4 * 40:
            Data = Data[3 * 40 + 1:len(Data)]
        else:
            Data = Data[3 * 40 + 1:4 * 40 + 1]
    elif page == '5':
        if len(Data) <= 5 * 40:
            Data = Data[4 * 40 + 1:len(Data)]
        else:
            Data = Data[4 * 40 + 1:5 * 40 + 1]
    elif page == '6':
        if len(Data) <= 6 * 40:
            Data = Data[5 * 40 + 1:len(Data)]
        else:
            Data = Data[5 * 40 + 1:6 * 40 + 1]
    return Data



def generateVersionImg(tData, prefix, page):
    fcNameToFile = {'fc': "UI_MSS_MBase_Icon_FC.png",
                    'fcp': "UI_MSS_MBase_Icon_FCp.png",
                    'ap': "UI_MSS_MBase_Icon_AP.png",
                    'app': "UI_MSS_MBase_Icon_APp.png"}
    font = ImageFont.truetype(r'src\static\Material\msyh.ttc', 24)
    max_width = 0
    for text in tData:
        w, h = font.getsize(str(text['title']) + str(text['level_label']) + str(text['achievements']) + str(text['song_id']) + str(text['fc']) + str(text['ds']) + " (       ) ")
        max_width = max(max_width, w + 95)
    tImg = Image.new('RGB', (max_width, len(tData) * 75 + 150), color=(255, 255, 255))
    draw = ImageDraw.Draw(tImg)
    draw.text(((max_width / 2) - (font.getsize(prefix)[0] / 2), 0), prefix, font=font, fill=(0, 0, 0))



def generateScoreListImg(tData, prefix, page):
    fcNameToFile = {'fc': "UI_MSS_MBase_Icon_FC.png",
                    'fcp': "UI_MSS_MBase_Icon_FCp.png",
                    'ap': "UI_MSS_MBase_Icon_AP.png",
                    'app': "UI_MSS_MBase_Icon_APp.png"}
    LevelToindex = {'Basic': 0, 'Advanced': 1, 'Expert': 2, 'Master': 3, 'Re:MASTER': 4}
    font = ImageFont.truetype(r'src\static\Material\msyh.ttc', 24)
    rows = len(tData)
    max_width = 0
    for text in tData:
        w, h = font.getsize(str(text['title']) + str(text['level_label']) + str(text['achievements']) + str(text['id']) + str(text['fc']) + " (           ) ")
        max_width = max(max_width, w + 95)
    tImg = Image.new('RGB', (max_width, rows*75+150), color=(255, 255, 255))
    draw = ImageDraw.Draw(tImg)
    draw.text(((max_width/2)-(font.getsize(prefix)[0]/2), 0), prefix, font=font, fill=(0, 0, 0))
    i = 1
    for dataLine in tData:
        musicId = dataLine['id']
        musicDs = float(total_list.by_id(str(musicId))['ds'][LevelToindex[dataLine['level_label']]])
        try:
            cover = Image.open(rf"src\static\images\maimai\covers\{musicId}.jpg")
        except FileNotFoundError:
            logger.info("[maimaiDX分数列表]没有该曲目封面！正在下载ID:" + str(musicId))
            try:
                coverDownload = requests.get(f"https://www.diving-fish.com/covers/{musicId}.jpg")
                with open(rf"src\static\images\maimai\covers\{musicId}.jpg", 'wb+')as f:
                    f.write(coverDownload.content)
                cover = Image.open(rf"src\static\images\maimai\covers\{musicId}.jpg")
            except:
                logger.info(f"[maimaiDX分数列表]歌曲{musicId}暂无封面")
                os.remove(rf"src\static\images\maimai\covers\{musicId}.jpg")
                cover = Image.new('RGB', (160, 160), color=(255, 255, 255))
                tempDraw = ImageDraw.Draw(cover)
                tempDraw.text(((80 - (font.getsize("暂无封面")[0] / 2)), 70), f"暂无封面", font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 20), fill=(0, 0, 0))
        tImg.paste(cover.resize((73, 73)), (10,75 * i))
        draw.text((85, 75 * i + 30), f"{dataLine['achievements']}%         B40:{computeRaB40(musicDs,dataLine['achievements'])}/{computeRaB40(musicDs,100.50)}     B50:{computeRaB50(musicDs,dataLine['achievements'])}/{computeRaB50(musicDs,100.50)}", font=font, fill=(0, 0, 0))
        draw.text((85, 75 * i), f"{musicId}.{dataLine['title']} | {dataLine['level_label']} | {musicDs} | [{dataLine['type']}]",font=font, fill=(0, 0, 0))
        try:
            fcImg = Image.open(rf"""src\static\images\maimai\Fc\{fcNameToFile[f"{dataLine['fc']}"]}""").convert('RGBA')
            fcImg = fcImg.resize((25, 25))
            tImg.paste(fcImg, (215, 75 * i + 35), fcImg)
        except:
            pass
        i += 1
    draw.text(((max_width / 2) - (font.getsize(f"Page {page}\n")[0] / 2), 75 * i + 14), f"Page {page}\n", font=font, fill=(0, 0, 0))
    draw.text(((max_width / 2) - (font.getsize("Generate BY fuBot")[0] / 2), 75 * i + 38), f"Generate BY fuBot", font=font, fill=(0, 0, 0))
    return tImg



def generateVersionList(version,songData,PlayerData):
    levelDatas = "["
    indexToLevel = {'0': "Basic", '1': "Advanced", '2': "Expert", '3': "Master", '4': "Re:MASTER"}
    levelToColor = {'Basic': (153, 255, 102),
                    'Advanced': (255, 242, 102),
                    'Expert': (255, 55, 55),
                    'Master': (191, 55, 255),
                    'Re:MASTER': (238, 202, 255)}
    processNameToFile = {'fc': "UI_MSS_MBase_Icon_FC.png",
                         'fcp': "UI_MSS_MBase_Icon_FCp.png",
                         'ap': "UI_MSS_MBase_Icon_AP.png",
                         'app': "UI_MSS_MBase_Icon_APp.png",
                         'fs': "UI_MSS_MBase_Icon_FS.png",
                         'fsp': "UI_MSS_MBase_Icon_FSp.png",
                         'fsd': "UI_MSS_MBase_Icon_FSD.png",
                         'fsdp': "UI_MSS_MBase_Icon_FSDp.png"}
    temp = None
    for tdata in songData:
        for tds in sorted(tdata['ds'], reverse=False):
            thisLevel = indexToLevel[f"{tdata['ds'].index(tds)}"]
            if temp == tds:
                thisLevel = indexToLevel[f"{tdata['ds'].index(tds) + 1}"]
            temp = tds
            if version != "舞" and thisLevel == "Re:MASTER":
                continue
            if version == "舞":
                if thisLevel != "Re:MASTER":
                    continue
            if int(tds - 0.7) >= int(tds):
                levelDatas += f"""{{"id":"{tdata['id']}","level":"{int(tds)}+","title":"{str(tdata['title']).replace('"', "'")}","level_label":"{thisLevel}","type":"{tdata['type']}","bs":{float(tds)}}},"""
            else:
                levelDatas += f"""{{"id":"{tdata['id']}","level":"{int(tds)}","title":"{str(tdata['title']).replace('"', "'")}","level_label":"{thisLevel}","type":"{tdata['type']}","bs":{float(tds)}}},"""
    # logger.info(levelDatas)
    levelDatas += "]"
    levelDatas = levelDatas.replace(",]", "]")
    levelDatas = json.loads(levelDatas)
    levelDatas = sorted(levelDatas, key=lambda x: x['bs'], reverse=True)

    titleFront = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 10)
    idFront = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15)
    levelFront = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 30)
    lineWidth = 1
    lineHeight = 1
    tempBase = (levelDatas[0])['level']
    for data in levelDatas:
        lineWidth += 1
        if lineWidth == 8 or tempBase != data['level']:
            lineWidth = 1
            lineHeight += 1
            tempBase = data['level']
    tImg = Image.new('RGB', (920, 100 * lineHeight + 30), color=(255, 255, 255))
    DXimg = Image.open(rf"src\static\images\maimai\UI_CMN_Name_DX.png").resize((25, 13))
    lineWidth = 0
    lineHeight = 1
    rowsHeight = 1
    rows = 1
    tempBase = (levelDatas[0])['level']
    for data in levelDatas:
        lineWidth += 1
        if lineWidth == 8 or tempBase != data['level']:
            rows += 1
            rowsHeight += 1
            if tempBase != data['level']:
                baseText = Image.new('RGB', (120, 100 * (rowsHeight - 1)),
                                     color=(random.randint(179, 255), random.randint(0, 255), random.randint(0, 255)))
                baseTextDraw = ImageDraw.Draw(baseText)
                baseTextWidth = 60 - (levelFront.getsize(f"{tempBase}")[0]) / 2
                baseTextHeight = (100 * (rowsHeight - 1)) / 2 - 20
                baseTextDraw.text((baseTextWidth, baseTextHeight), f"{tempBase}", font=levelFront, fill=(0, 0, 0))
                tImg.paste(baseText, (0, (100 * (lineHeight - rowsHeight + 1))))
                rowsHeight = 1
                rows = 1
                tempBase = data['level']
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
                logger.info(f"[X代完成表]歌曲{data['id']}封面下载成功！")
                cover = Image.open(rf"src\static\images\maimai\covers\{data['id']}.jpg")
                cover = cover.resize((90, 90))
            except:
                os.remove(rf"src\static\images\maimai\covers\{data['id']}.jpg")
                logger.info(f"[X代完成表]歌曲{data['id']}暂无封面")
                cover = Image.new('RGB', (90, 90), color=(255, 255, 255))
                tempDraw = ImageDraw.Draw(cover)
                tempDraw.text(((50 - (titleFront.getsize(f"{data['title']}")[0] / 2)), 40), f"{data['title']}",font=titleFront, fill=(0, 0, 0))
        tempDraw = ImageDraw.Draw(cover)
        try:
            tempDraw.text((3, 3), text=f"{data['id']}", font=idFront,fill=(random.randint(0, 130), random.randint(200, 230), random.randint(200, 250)))
        except:
            pass
        coverBg = Image.new('RGB', (100, 100), color=levelToColor[f"{data['level_label']}"])
        if PlayerData is not None:
            for tData in PlayerData:
                if str(tData['id']) == str(data['id']) and indexToLevel[f"{tData['level_index']}"] == data['level_label']:
                    rankImg = Image.open(rf"""src\static\images\maimai\Rank\{baseNameToFile[f'{achieveToRank(tData["achievements"])}']}""")
                    rankImgW = rankImg.width
                    rankImgH = rankImg.height
                    cover.paste(rankImg,(int((90-rankImgW)/2),int((90-rankImgH)/2)),rankImg)

                    try:
                        fcImg = Image.open(rf"""src\static\images\maimai\Fc\{processNameToFile[f"{tData['fc']}"]}""").convert('RGBA')
                        fcImg = fcImg.resize((25, 25))
                        cover.paste(fcImg, (0,65), fcImg)
                    except:
                        pass

                    try:
                        fcImg = Image.open(rf"""src\static\images\maimai\Fc\{processNameToFile[f"{tData['fs']}"]}""").convert('RGBA')
                        fcImg = fcImg.resize((25, 25))
                        cover.paste(fcImg, (28,65), fcImg)
                    except:
                        pass

                    break
        coverBg.paste(cover, (5, 5))
        if data['type'] == "DX":
            coverBg.paste(DXimg, (70, 80))
        tImg.paste(coverBg, ((120 + 100 * (lineWidth - 1)), (100 * (lineHeight - 1))))
    baseText = Image.new('RGB', (120, 100 * rowsHeight),
                         color=(random.randint(179, 255), random.randint(0, 255), random.randint(0, 255)))
    baseTextDraw = ImageDraw.Draw(baseText)
    baseTextWidth = 60 - (levelFront.getsize(f"{tempBase}")[0]) / 2
    baseTextHeight = (100 * rowsHeight) / 2 - 20
    baseTextDraw.text((baseTextWidth, baseTextHeight), f"{tempBase}", font=levelFront, fill=(0, 0, 0))
    tImg.paste(baseText, (0, (100 * (lineHeight - rowsHeight))))
    responseTextDraw = ImageDraw.Draw(tImg)
    responseTextDraw.text((0, tImg.height - 20), f"Generate by fuBot",font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 15), fill=(0, 0, 0))
    return tImg