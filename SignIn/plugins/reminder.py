import datetime
import os

from SignIn.userconfig import *
from SignIn.recorder import is_signin, is_submit_signed
from chinese_calendar import is_workday
import nonebot


@nonebot.scheduler.scheduled_job('cron', hour=signin_time_remind.hour, minute=signin_time_remind.minute)
async def remind_job():
    if not is_workday(datetime.datetime.now().date()):
        return
    day_of_week = datetime.datetime.now().weekday()
    user_not_sign = []
    for user in sign_schedule[day_of_week]:
        if not is_submit_signed(user):
            user_not_sign.append(user)

    if user_not_sign:
        message_str = '记得值班哦  O(∩_∩)O\n'
        for user in user_not_sign:
            message_str = message_str + f'[CQ:at,qq={name_to_qq[user]}] '
        bot = nonebot.get_bot()
        await bot.send_group_msg(group_id=target_group, message=message_str)


@nonebot.scheduler.scheduled_job('cron', hour=signin_time_warning.hour, minute=signin_time_warning.minute)
async def push_job():
    if not is_workday(datetime.datetime.now().date()):
        return
    day_of_week = datetime.datetime.now().weekday()
    user_not_sign = []
    for user in sign_schedule[day_of_week]:
        if not is_submit_signed(user):
            user_not_sign.append(user)

    if user_not_sign:
        message_str = '怎么还没签到呀 (눈‸눈) 咕咕也要和人家说嘛\n'
        for user in user_not_sign:
            message_str = message_str + f'[CQ:at,qq={name_to_qq[user]}] '
        bot = nonebot.get_bot()
        await bot.send_group_msg(group_id=target_group, message=message_str)
