import os
import math
import random

import requests
from nonebot.log import logger
from typing import Optional, Dict, List
import aiohttp
from PIL import Image, ImageDraw, ImageFont

scoreRank = 'D C B BB BBB A AA AAA S S+ SS SS+ SSS SSS+'.split(' ')
combo = ' FC FC+ AP AP+'.split(' ')
diffs = 'Basic Advanced Expert Master Re:Master'.split(' ')
rankPlate = {0:"UI_Rank_00.png",
             250:"UI_Rank_01.png",
             500:"UI_Rank_02.png",
             750:"UI_Rank_03.png",
             1000:"UI_Rank_04.png",
             1200:"UI_Rank_05.png",
             1400:"UI_Rank_06.png",
             1500:"UI_Rank_07.png",
             1600:"UI_Rank_08.png",
             1700:"UI_Rank_09.png",
             1800:"UI_Rank_10.png",
             1850:"UI_Rank_11.png",
             1900:"UI_Rank_12.png",
             1950:"UI_Rank_13.png",
             2000:"UI_Rank_14.png",
             2010:"UI_Rank_15.png",
             2020:"UI_Rank_16.png",
             2030:"UI_Rank_17.png",
             2040:"UI_Rank_18.png",
             2050:"UI_Rank_19.png",
             2060:"UI_Rank_20.png",
             2070:"UI_Rank_21.png",
             2080:"UI_Rank_22.png",
             2090:"UI_Rank_23.png",
             2100:"UI_Rank_24.png"}


def drawBaseImg(sd,dx,B35Rating,B15Rating,rankRating,userData,userName,plate,icon):
    BaseImg = Image.new('RGB', (2500, 1550), color=(0, 162, 232)).convert("RGBA")
    decoCenter = Image.open(rf"src\static\images\maimai\Style-Universe\deco_center.png")  # 1693*621
    BaseImg.paste(decoCenter, (0, 0), decoCenter)
    BaseImg.paste(decoCenter, (1693, 200), decoCenter)
    BaseImg.paste(decoCenter, (0, 621), decoCenter)
    BaseImg.paste(decoCenter, (1693, 821), decoCenter)
    dotsTop = Image.open(rf"src\static\images\maimai\Style-Universe\dots_top.png")
    dotsTop = dotsTop.resize((912, 215))
    BaseImg.paste(dotsTop, (0, 0), dotsTop)
    BaseImg.paste(dotsTop, (912, 0), dotsTop)
    BaseImg.paste(dotsTop, (1824, 0), dotsTop)
    dotsUnder = Image.open(rf"src\static\images\maimai\Style-Universe\dots_under.png")
    dotsUnder = dotsUnder.resize((912, 215))
    BaseImg.paste(dotsUnder, (0, 1335), dotsUnder)
    BaseImg.paste(dotsUnder, (912, 1335), dotsUnder)
    BaseImg.paste(dotsUnder, (1824, 1335), dotsUnder)
    cornerRight = Image.open(rf"src\static\images\maimai\Style-Universe\corner_right.png")
    cornerRight = cornerRight.resize((215, 215))
    BaseImg.paste(cornerRight, (2285, 1085), cornerRight)
    cornerLeft = Image.open(rf"src\static\images\maimai\Style-Universe\corner_left.png")
    cornerLeft = cornerLeft.resize((215,215))
    BaseImg.paste(cornerLeft, (0,0),cornerLeft)
    underLine = Image.open(rf"src\static\images\maimai\Style-Universe\bg.png")#864*157
    BaseImg.paste(underLine, (0, 1396), underLine)
    BaseImg.paste(underLine, (864, 1396), underLine)
    BaseImg.paste(underLine, (1728, 1396), underLine)

    UserImg = drawUserImg(userData,B35Rating,B15Rating,rankRating,userName,icon,plate)
    BaseImg.paste(UserImg, (0, 30), UserImg)

    dxLogo = Image.open(rf"src\static\images\maimai\Logo_2022.png")
    dxLogo = dxLogo.resize((308, 178))
    BaseImg.paste(dxLogo, (10, 5), dxLogo)

    rankScores = [0,0]
    baseLine = 280
    stIconImg = Image.open(rf"src\static\images\maimai\UI_GRS_Base_Achievment_00.png")
    BaseImg.paste(stIconImg, (120, baseLine-40), stIconImg)

    count = 0
    for line in sd:
        count += 1
        singleImg = drawSignleImg(line,count)
        x = 150 + 400*(int((count-1)%5))+40*int((count-1)%5)
        y = baseLine + int((count-1)/5)*100 + int((count-1)/5)*10
        BaseImg.paste(singleImg,(int(x),int(y)),singleImg)
        rankScores[0] += int(line['ra'])
    rankScoresDraw = ImageDraw.Draw(BaseImg)
    rankScoresDraw.text((330, baseLine-35), f"B35:{rankScores[0]}", font=ImageFont.truetype(r'src\static\Material\STHUPO.TTF', 20),fill=(255, 255, 255))

    baseLine = baseLine + 800 + 60
    dxIconImg = Image.open(rf"src\static\images\maimai\UI_GRS_Base_Achievment_01.png")
    BaseImg.paste(dxIconImg, (120, baseLine - 40), dxIconImg)
    count = 0
    for line in dx:
        count += 1
        singleImg = drawSignleImg(line, count)
        x = 150 + 400 * (int((count - 1) % 5)) + 40 * int((count - 1) % 5)
        y = baseLine + int((count - 1) / 5) * 100 + int((count - 1) / 5) * 10
        BaseImg.paste(singleImg, (int(x), int(y)), singleImg)
        rankScores[1] += int(line['ra'])
    rankScoresDraw = ImageDraw.Draw(BaseImg)
    rankScoresDraw.text((330, baseLine - 35), f"B15:{rankScores[1]}",font=ImageFont.truetype(r'src\static\Material\STHUPO.TTF', 20), fill=(255, 255, 255))

    designDraw = ImageDraw.Draw(BaseImg)
    designDraw.text((1145, 1520), f"Generated by fuBot",font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 20), fill=(0, 0, 0))

    return BaseImg



def drawUserImg(data,B35Rating,B15Rating,rankRating,userName,icon,plate):
    numToNum = {    '0': "UI_NUM_Drating_0.png",
                    '1': "UI_NUM_Drating_1.png",
                    '2': "UI_NUM_Drating_2.png",
                    '3': "UI_NUM_Drating_3.png",
                    '4': "UI_NUM_Drating_4.png",
                    '5': "UI_NUM_Drating_5.png",
                    '6': "UI_NUM_Drating_6.png",
                    '7': "UI_NUM_Drating_7.png",
                    '8': "UI_NUM_Drating_8.png",
                    '9': "UI_NUM_Drating_9.png"}
    UserImg = Image.new('RGBA', (2500, 200))

    plateImg = Image.open(plate)
    plateImg = plateImg.resize((720,116))
    UserImg.paste(plateImg, (830, 8), plateImg)

    iconImg = Image.open(icon)
    iconImg = iconImg.resize((100,100))
    UserImg.paste(iconImg,(835,15),iconImg)

    ratingPlate = ""
    totalRating = int(B35Rating)+int(B15Rating)
    if totalRating > 8499:
        ratingPlate = "UI_CMN_DXRating_10.png"
    elif totalRating > 7999:
        ratingPlate = "UI_CMN_DXRating_09.png"
    elif totalRating > 6999:
        ratingPlate = "UI_CMN_DXRating_08.png"
    elif totalRating > 5999:
        ratingPlate = "UI_CMN_DXRating_07.png"
    elif totalRating > 4999:
        ratingPlate = "UI_CMN_DXRating_06.png"
    elif totalRating > 3999:
        ratingPlate = "UI_CMN_DXRating_05.png"
    elif totalRating > 2999:
        ratingPlate = "UI_CMN_DXRating_04.png"
    elif totalRating > 1999:
        ratingPlate = "UI_CMN_DXRating_03.png"
    elif totalRating > 999:
        ratingPlate = "UI_CMN_DXRating_02.png"
    else:
        ratingPlate = "UI_CMN_DXRating_01.png"
    ratingPlateImg = Image.open(rf"src\static\images\maimai\Rating\{ratingPlate}").resize((174,36))
    UserImg.paste(ratingPlateImg, (940, 16), ratingPlateImg)

    numImg = Image.open(rf"src\static\images\maimai\Num\{numToNum[f'{int(totalRating / 1 % 10)}']}").resize((21,23))
    UserImg.paste(numImg, (1085, 21), numImg)

    numImg = Image.open(rf"src\static\images\maimai\Num\{numToNum[f'{int(totalRating / 10 % 10)}']}").resize((21, 23))
    UserImg.paste(numImg, (1067, 21), numImg)

    numImg = Image.open(rf"src\static\images\maimai\Num\{numToNum[f'{int(totalRating / 100 % 10)}']}").resize((21, 23))
    UserImg.paste(numImg, (1049, 21), numImg)

    numImg = Image.open(rf"src\static\images\maimai\Num\{numToNum[f'{int(totalRating / 1000 % 10)}']}").resize((21, 23))
    UserImg.paste(numImg, (1031, 21), numImg)

    if int(totalRating / 10000 % 10) != 0:
        numImg = Image.open(rf"src\static\images\maimai\Num\{numToNum[f'{int(totalRating / 10000 % 10)}']}").resize((21, 23))
        UserImg.paste(numImg, (1012, 21), numImg)

    rankImg = Image.open(rf"src\static\images\maimai\Ranks\{rankPlate[int(rankRating)]}").resize((74, 34))
    UserImg.paste(rankImg, (1114, 15), rankImg)


    UserIdImg = Image.new('RGBA', (227, 45), color=(255, 255, 255))
    UserIdDraw = ImageDraw.Draw(UserIdImg)
    UserIdDraw.text((7, 6), f"{userName}", font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 25),fill=(0, 0, 0))
    UserImg.paste(UserIdImg, (940, 50), UserIdImg)

    totalRatingImg = Image.open(r"src\static\images\maimai\Shougou\UI_CMN_Shougou_Rainbow.png")#421*92  227*50
    totalRatingDraw = ImageDraw.Draw(totalRatingImg)
    totalRatingDraw.text((20, 5), f"B35：{B35Rating} + B15：{B15Rating}", font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 11),fill=(0, 0, 0))
    UserImg.paste(totalRatingImg, (940, 92), totalRatingImg)

    return UserImg



def drawSignleImg(data,count):
    fcNameToFile = {'fc': "UI_MSS_MBase_Icon_FC.png",
                    'fcp': "UI_MSS_MBase_Icon_FCp.png",
                    'ap': "UI_MSS_MBase_Icon_AP.png",
                    'app': "UI_MSS_MBase_Icon_APp.png"}
    fsNameToFile = {'fs': "UI_MSS_MBase_Icon_FS_S.png",
                    'fsp': "UI_MSS_MBase_Icon_FSD_S.png",
                    'fsd': "UI_MSS_MBase_Icon_FSDp_S.png",
                    'fsdp': "UI_MSS_MBase_Icon_FSp_S.png"}
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
    rankIcon = {'Basic': "diff_basic.png",
                'Advanced': "diff_advanced.png",
                'Expert': "diff_expert.png",
                'Master': "diff_master.png",
                'Re:MASTER': "diff_remaster.png"}
    levelToColor = {'Basic': (153, 255, 102),
                    'Advanced': (255, 242, 102),
                    'Expert': (255, 55, 55),
                    'Master': (191, 55, 255),
                    'Re:MASTER': (238, 202, 255)}
    coverFront = ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 10)
    singleBaseImg = Image.new('RGB', (400, 100), color=(7, 86, 156)).convert("RGBA")

    underImg = Image.new('RGB', (400, 20), color=(255, 255, 255))
    underTextDraw = ImageDraw.Draw(underImg)
    underTextDraw.text((109, 0), f"#{count}", font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 16),fill=(0, 0, 0))
    raImg = Image.open(r"src\static\images\maimai\rating.png").resize((48,9))
    underImg.paste(raImg,(150,0),raImg)
    underTextDraw.text((165, 7), f"{data['ds']}",font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 10), fill=(0, 0, 0))
    underTextDraw.text((200, 0), f">{computeRa(data['ds'],data['achievements'])}", font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 16),fill=(0, 0, 0))
    dxScoreImg = Image.open(r"src\static\images\maimai\deluxscore.png").resize((72,17))
    underImg.paste(dxScoreImg,(270,2),dxScoreImg)
    underTextDraw.text((337, 0), f"{data['dxScore']}",font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 16), fill=(29, 164, 0))

    singleBaseImg.paste(underImg, (0, 80))


    try:
        cover = Image.open(rf"src\static\images\maimai\covers\{data['song_id']}.jpg")
        cover = cover.resize((90, 90))
    except FileNotFoundError:
        try:
            coverDownload = requests.get(f"https://www.diving-fish.com/covers/{data['id']}.jpg")
            with open(rf"src\static\images\maimai\covers\{data['song_id']}.jpg", 'wb+')as f:
                f.write(coverDownload.content)
                f.close()
            logger.info(f"[maimaiDX]歌曲{data['song_id']}封面下载成功！")
            cover = Image.open(f"src\static\images\maimai\covers\{data['song_id']}.jpg")
            cover = cover.resize((90, 90))
        except:
            try:
                os.remove(f"src\static\images\maimai\covers\{data['song_id']}.jpg")
            except:
                pass
            logger.info(f"[maimaiDX]歌曲{data['song_id']}暂无封面")
            cover = Image.new('RGB', (90, 90), color=(255, 255, 255))
            tempDraw = ImageDraw.Draw(cover)
            tempDraw.text(((50 - (coverFront.getsize(f"{data['title']}")[0] / 2)), 40), f"{data['title']}",font=coverFront, fill=(0, 0, 0))

    coverBg = Image.new('RGB', (100, 100), color=levelToColor[f"{data['level_label']}"])
    coverBg.paste(cover, (5, 5))
    cover = coverBg
    rankImg = Image.open(rf"""src\static\images\maimai\Diff\{rankIcon[f"{data['level_label']}"]}""")
    dxImg = Image.open(r"src\static\images\maimai\UI_CMN_Name_DX.png")
    dxImg = dxImg.resize((30, 21))
    singleBaseImg.paste(cover,(0, 0))
    singleBaseImg.paste(rankImg, (100, 1), rankImg)
    if data['type'] == "DX":
        singleBaseImg.paste(dxImg, (60, 69), dxImg)
    processImg = Image.open(rf"""src\static\images\maimai\Process\{baseNameToFile[f"{data['rate']}"]}""")
    singleBaseImg.paste(processImg, (290, 30), processImg)
    textDraw = ImageDraw.Draw(singleBaseImg)
    textDraw.text((245, 15), f"id:{data['song_id']}",font=ImageFont.truetype(r'src\static\Material\STHUPO.TTF', 12), fill=(255, 255, 255))
    title = data['title']
    if _coloumWidth(title) > 15:
        title = _changeColumnWidth(title, 14) + '...'
    textDraw.text((107,27), f"{title}", font=ImageFont.truetype(r'src\static\Material\msyhbd.ttc', 20), fill=(255, 255, 255))
    textDraw.text((103, 50), f"{data['achievements']}%", font=ImageFont.truetype(r'src\static\Material\STHUPO.TTF', 30), fill=(255, 255, 255))
    blanIconImg = Image.open(r"src\static\images\maimai\Fc\UI_MSS_MBase_Icon_Blank.png")
    blanIconImg = blanIconImg.resize((28,28))
    singleBaseImg.paste(blanIconImg, (337, 3), blanIconImg)
    singleBaseImg.paste(blanIconImg, (306, 3), blanIconImg)

    if data['fc'] != "":
        fcIconImg = Image.open(rf"""src\static\images\maimai\Fc\{fcNameToFile[f"{data['fc']}"]}""")
        fcIconImg = fcIconImg.resize((28,28))
        singleBaseImg.paste(fcIconImg, (337, 3), fcIconImg)
    if data['fs'] != "":
        fsIconImg = Image.open(rf"""src\static\images\maimai\Fc\{fsNameToFile[f"{data['fs']}"]}""")
        fsIconImg = fsIconImg.resize((28, 28))
        singleBaseImg.paste(fsIconImg, (306, 3), fsIconImg)

    return singleBaseImg



def _getCharWidth(o) -> int:
    widths = [
        (126, 1), (159, 0), (687, 1), (710, 0), (711, 1), (727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0),
        (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1), (8426, 0), (9000, 1), (9002, 2), (11021, 1),
        (12350, 2), (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1), (55203, 2), (63743, 1),
        (64106, 2), (65039, 1), (65059, 0), (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2),
        (120831, 1), (262141, 2), (1114109, 1),
    ]
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1



def _coloumWidth(s:str):
    res = 0
    for ch in s:
        res += _getCharWidth(ord(ch))
    return res



def _changeColumnWidth(str, len):
    res = 0
    sList = []
    for ch in str:
        res += _getCharWidth(ord(ch))
        if res <= len:
            sList.append(ch)
    return ''.join(sList)



def computeRa(ds: float, achievement:float) -> int:
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

def getRandomPlate():
    plateList = []
    for root, dirs, files in os.walk(r'src\static\images\maimai\plate'):
        for file in files:
            file = str(os.path.join(file))
            if 'UI_Plate' not in file:
                continue
            plateList.append(file)
    return rf"src\static\images\maimai\plate\{plateList[random.randint(0, len(plateList) - 1)]}"

def getRandomIcon():
    iocnList = []
    for root, dirs, files in os.walk(r'src\static\images\maimai\icon'):
        for file in files:
            file = str(os.path.join(file))
            if 'UI_Icon' not in file:
                continue
            iocnList.append(file)
    return rf"src\static\images\maimai\icon\{iocnList[random.randint(0, len(iocnList) - 1)]}"


async def generate(payload: Dict) -> (Optional[Image.Image], bool):
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
        if resp.status == 400:
            return None, 400, None
        if resp.status == 403:
            return None, 403, None
        obj = await resp.json()
        dx: List[Dict] = obj["charts"]["dx"]
        sd: List[Dict] = obj["charts"]["sd"]
        B35Rating = 0
        B15Rating = 0
        for t in sd:
            B35Rating += int(computeRa(t['ds'], t['achievements']))
        for t in dx:
            B15Rating += int(computeRa(t['ds'], t['achievements']))
        plate = None
        icon = None
        if obj['user_data'] == None:
            if (obj['plate'] == None) or (obj['plate'] == ''):
                plate = getRandomPlate()
            icon = getRandomIcon()

        achievePath = []
        for root, dirs, files in os.walk(r"src\static\images\maimai\plate\achievements"):
            for t in files:
                achievePath.append(str(t).replace('.png',''))
        platePath = []
        for root, dirs, files in os.walk(r"src\static\images\maimai\plate\raw"):
            for t in files:
                platePath.append(str(t).replace('.png','').replace("UI_Plate_",""))
        iconPath = []
        for root, dirs, files in os.walk(r"src\static\images\maimai\icon"):
            for t in files:
                iconPath.append(str(t).replace('.png', '').replace('UI_Icon_', ""))
        if plate == None:
            if obj['plate'] in achievePath:
                plate = rf"src\static\images\maimai\plate\achievements\{obj['plate']}.png"
            elif str(obj['user_data']['plateId']).zfill(6) in platePath:
                plate = rf"src\static\images\maimai\plate\raw\UI_Plate_{str(obj['user_data']['plateId']).zfill(6)}.png"
            else:
                plate = getRandomPlate()
            try:
                Image.open(plate)
            except:
                plate = getRandomPlate()
        if icon == None:
            if str(obj['user_data']['iconId']).zfill(6) in iconPath:
                icon = rf"src\static\images\maimai\icon\UI_Icon_{str(obj['user_data']['iconId']).zfill(6)}.png"
            else:
                icon = getRandomIcon()
        return drawBaseImg(sd,dx,B35Rating,B15Rating,int(obj['additional_rating']),obj["user_data"],obj["nickname"],plate,icon), 0, int(obj["rating"])