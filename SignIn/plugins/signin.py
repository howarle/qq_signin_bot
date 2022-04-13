import datetime
import os

from SignIn.userconfig import *
from SignIn.recorder import is_signin, sign_it, revoke_sign, sign_gugugu
from chinese_calendar import is_workday
from nonebot import on_command, CommandSession, SenderRoles

record_froce_time = datetime.datetime.now()

recordlog_file = os.path.split(os.path.realpath(__file__))[
    0] + '/../signin.log'


def from_target_group(sender: SenderRoles):
    return sender.from_group(target_group)


def admin_permission(sender: SenderRoles):
    return (sender.is_admin or sender.is_owner or sender.sent_by(admin_whitelist))


@on_command('bothelp', permission=from_target_group, only_to_me=False)
async def readme(session: CommandSession):
    ret_str = '''签到 ：当天签到；
咕咕：咕咕；
签到撤销 ：撤销当天签到；'''
    await session.send(ret_str)


@on_command('签到', permission=from_target_group, only_to_me=False)
async def record_sign_in(session: CommandSession):
    # 获取qq号
    user_id = session.event['sender']['user_id']
    user_nikename = session.event['sender']['nickname']
    user_name = ''
    user_itself = True

    args_name = session.current_arg_text.strip()
    if (int(user_id) in admin_whitelist) and (args_name != '') and (args_name):
        if args_name not in name_list:
            await session.send('名单里没有%s呢 ::>_<::' % args_name)
            return
        user_name = args_name
        user_itself = False
    else:
        if args_name != '' and not(int(user_id) in admin_whitelist):
            await session.send('权限不够呢  ::>_<::')
            return
        if user_id not in qq_to_name:
            await session.send('%s 名单里没有你呢 ::>_<::' % user_nikename)
            return
        user_name = qq_to_name[user_id]

    fo = open(recordlog_file, "a+")
    fo.write("[%s] sign_in : %s(%s)\n" %
             (datetime.datetime.now(), user_name, user_id))
    fo.close()

    if is_signin(user_name) == True:
        await session.send('(°⌓°) %s已经签过到了呀' % user_name)
        return

    global record_froce_time
    now_time = datetime.datetime.now().time()
    if record_froce_time >= datetime.datetime.now() or (is_workday(datetime.datetime.now().date()) and signin_time_start <= now_time and signin_time_stop >= now_time):
        result = sign_it(user_name)
        if user_itself:
            await session.send('~\(≧▽≦)/~\n别忘了也要在本本上签名呐' if result else '签到失败')
        else:
            await session.send(('~\(≧▽≦)/~\n%s签到成功' if result else '%s签到失败') % user_name)
    else:
        if not is_workday(datetime.datetime.now().date()):
            await session.send('今天似乎不用值班呢 (・ω・)')
        elif not(signin_time_start <= now_time and signin_time_stop >= now_time):
            await session.send('还没到签到时间呐 ::>_<::\n签到时间：%s ~ %s' % (signin_time_start.strftime('%H:%M'), signin_time_stop.strftime('%H:%M')))


@on_command('签到撤销', aliases=['撤销签到'], permission=from_target_group, only_to_me=False)
async def record_sign_in_revoke(session: CommandSession):
    user_id = session.event['sender']['user_id']
    user_nikename = session.event['sender']['nickname']
    args_name = session.current_arg_text.strip()
    user_name = ''
    user_itself = True

    if (int(user_id) in admin_whitelist) and (args_name != ''):
        if args_name not in name_list:
            await session.send('名单里没有%s呢 ::>_<::' % args_name)
            return
        user_name = args_name
        user_itself = True
    else:
        if args_name != '' and not(int(user_id) in admin_whitelist):
            await session.send('权限不够呢  ::>_<::')
            return
        if user_id not in qq_to_name:
            await session.send('%s 名单里没有你呢 ::>_<::' % user_nikename)
            return
        user_name = qq_to_name[user_id]

    fo = open(recordlog_file, "a+")
    fo.write("[%s] sign_in_revoke : %s(%s)\n" %
             (datetime.datetime.now(), user_name, user_id))
    fo.close()

    if not is_signin(user_name):
        await session.send('%s还没签过到呢 Ծ‸Ծ' % user_name)
        return

    result = revoke_sign(user_name)
    if user_itself:
        await session.send('撤掉啦  ᐕ)⁾⁾' if result else '撤销签到失败')
    else:
        await session.send('%s %s' % (user_name, '撤掉啦  ᐕ)⁾⁾' if result else '撤销签到失败'))


@ on_command('咕咕', permission=from_target_group, only_to_me=False)
async def record_gugugu(session: CommandSession):
    user_id = session.event['sender']['user_id']
    user_nikename = session.event['sender']['nickname']
    args_name = session.current_arg_text.strip()
    user_name = ''
    user_itself = True

    if (int(user_id) in admin_whitelist) and (args_name != ''):
        if args_name not in name_list:
            await session.send('名单里没有%s呢 ::>_<::' % args_name)
            return
        user_name = args_name
        user_itself = False
    else:
        if args_name != '' and not(int(user_id) in admin_whitelist):
            await session.send('权限不够呢  ::>_<::')
            return
        if user_id not in qq_to_name:
            await session.send('%s 名单里没有你呢 ::>_<::' % user_nikename)
            return
        user_name = qq_to_name[user_id]

    fo = open(recordlog_file, "a+")
    fo.write("[%s] gugugu : %s(%s)\n" %
             (datetime.datetime.now(), user_name, user_id))
    fo.close()

    if is_signin(user_name):
        await session.send('%s已经签过到呢 Ծ‸Ծ\n先撤销签到吧' % user_name)
        return

    result = sign_gugugu(user_name)
    if user_itself:
        await session.send('咕|ω・`)' if result else '失败')
    else:
        await session.send('%s %s' %(user_name, ('咕|ω・`)' if result else '失败')))


@ on_command(('签到', 'open'), permission=[admin_permission, from_target_group], only_to_me=False)
async def heartbeat(session: CommandSession):
    global record_froce_time
    record_froce_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
    await session.send('开启额外签到\n签到截止时间：%s' % (record_froce_time.strftime('%m-%d %H:%M')))


@ on_command(('签到', 'close'), permission=[admin_permission, from_target_group], only_to_me=False)
async def heartbeat(session: CommandSession):
    global record_froce_time
    record_froce_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    await session.send('额外签到关闭')


@ on_command('ping', permission=from_target_group, only_to_me=False)
async def heartbeat(session: CommandSession):
    await session.send('~\(≧▽≦)/~  pong!')
    ret_str = ''
    now_time = datetime.datetime.now().time()
    if is_workday(datetime.datetime.now().date()):
        ret_str = ret_str + '今天大家记得值班哦!'
    else:
        ret_str = ret_str + '好耶！今天不用值班'

    await session.send(ret_str)
