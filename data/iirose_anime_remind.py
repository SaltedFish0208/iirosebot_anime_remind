import requests
import datetime

from loguru import logger
from API.api_message import at_user
from API.api_iirose import APIIirose  # 大部分接口都在这里
from globals.globals import GlobalVal  # 一些全局变量 now_room_id 是机器人当前所在的房间标识，websocket是ws链接，请勿更改其他参数防止出bug，也不要去监听ws，websockets库只允许一个接收流
from API.api_get_config import get_master_id  # 用于获取配置文件中主人的唯一标识
from API.decorator.command import on_command, MessageType  # 注册指令装饰器和消息类型Enmu

API = APIIirose()  # 吧class定义到变量就不会要求输入self了（虽然我都带了装饰器没有要self的 直接用APIIirose也不是不可以 习惯了

bangumiapi = "https://api.bgm.tv/calendar"
weekdays = {
    "1":"星期一",
    "2":"星期二",
    "3":"星期三",
    "4":"星期四",
    "5":"星期五",
    "6":"星期六",
    "7":"星期日",
    "星期一":"1",
    "星期二":"2",
    "星期三":"3",
    "星期四":"4",
    "星期五":"5",
    "星期六":"6",
    "星期日":"7"
}

@on_command('>今日番剧', False, command_type=[MessageType.room_chat, MessageType.private_chat])  # command_type 参数可让本指令在哪些地方生效，发送弹幕需验证手机号，每天20条。本参数需要输入列表，默认不输入的情况下只对房间消息做出反应，单个类型也需要是列表
async def bangumitoday(Message):  # 请保证同一个插件内不要有两个相同的指令函数名进行注册，否则只会保留最后一个注册的
    global weekdays
    response = requests.get(f'{bangumiapi}').json()
    bangumi_today = []
    for i in response:
        weekday = i["weekday"]["id"]
        if weekday == datetime.datetime.now().isoweekday():
            for a in i["items"]:
                bangumi_today.append(f'番剧：[{a["name_cn"]}]({a["url"]})\n'
                           f'日文名：{a["name"]}\n'
                           f'![番剧封面]({a["images"]["large"]}#e)')
        else:
            pass
    msg = "\n".join(bangumi_today)
    await API.send_msg(Message, r'\\\*'
                       f'\n# 以下是今日番剧更新\n'
                       f'今日是{weekdays[str(datetime.datetime.now().isoweekday())]}\n'
                       f'{msg}')

@on_command('>番剧更新 ', True, command_type=[MessageType.room_chat, MessageType.private_chat])  # command_type 参数可让本指令在哪些地方生效，发送弹幕需验证手机号，每天20条。本参数需要输入列表，默认不输入的情况下只对房间消息做出反应，单个类型也需要是列表
async def bangumiday(Message, text):  # 请保证同一个插件内不要有两个相同的指令函数名进行注册，否则只会保留最后一个注册的
    global weekdays
    response = requests.get(f'{bangumiapi}').json()
    bangumi_today = []
    for i in response:
        weekday = i["weekday"]["id"]
        if weekday == int(weekdays[text]):
            for a in i["items"]:
                bangumi_today.append(f'番剧：[{a["name_cn"]}]({a["url"]})\n'
                           f'日文名：{a["name"]}\n'
                           f'![番剧封面]({a["images"]["large"]}#e)')
        else:
            pass
    msg = "\n".join(bangumi_today)
    await API.send_msg(Message, r'\\\*'
                       f'\n# 以下是{text}的番剧更新\n'
                       f'{msg}')