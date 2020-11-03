import schedule
import datetime

from redmine.alarm.alarm_bug import generate_dingtalk_message, get_result
from redmine.common.base.config_operate import ReadConfig
from redmine.common.redmine_common import MyRedmine
from redmine.tools.dingtalk import send_dingtalk_markdown


def job1(redmine,project_name,query,priorities,webhook,title,hourdif,daydif):
    print('Job1:每隔10秒执行一次的任务')
    print('Job1-startTime:%s' %(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # final = get_result(redmine, project_name, query, tracker_id, status_name, priorities)
    # # save_data(final)
    # text = generate_dingtalk_message(redmine, final)
    # send_dingtalk_markdown(webhook, title, text)
    final = get_result(redmine, project_name, query, priorities, hourdif, daydif)
    # save_data(final)
    text = generate_dingtalk_message(redmine, final, hourdif, daydif)
    send_dingtalk_markdown(webhook, title, text)
    print('Job1-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

if __name__ == '__main__':

    # redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
    # redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
    # project_name = 'online'
    # priorities = ['High', 'Urgent', 'Immediate']
    # status_name = "Resolved"
    # # query_id = 128
    # redmine = set_Redmine(redmine_url, redmine_key)
    # tracker_id = get_trackerId_by_name(redmine, "产品BUG")
    # # issues = get_issues(redmine, None, 128, tracker_id, status_name)
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=500008fda504c16db55761cef3068f09b4d38b1c4dede057c33cd721b8026834'  # 测试组机器人
    # # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=aff741f23bba7e599d512586944537f623464c46d75af860990e2c21435e7d37'  # 填写你自己创建的机器人
    # title = '线上BUG提醒'
    # query = {}
    # query['资产平台'] = 120
    # query['离线计算'] = 128
    # query['实时计算'] = 129
    # query['应用平台'] = 130
    #
    # hourdif = 24  # 获取24小时内未验证的线上问题
    # daydif = 3  # 获取超过3天未验证的线上问题
    config = ReadConfig()
    project_id = config.ALARM_PROJECT
    redmine = MyRedmine(config.REDMINE_URL, config.REDMINE_KEY).redmine
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=' + config.WEBHOOK  # 填写你自己创建的机器人
    title = config.MESSAGE_TITLE
    query = config.ALARM_QUERY
    priorities = config.ALARM_PRIORITIES
    hourdif = config.HOUR_DIFF
    daydif = config.DAY_DIFF
    final = get_result(redmine, project_id, query, priorities, hourdif, daydif)
    text = generate_dingtalk_message(redmine,final, hourdif, daydif)
    schedule.every(20).seconds.do(job1,redmine,project_id,query,priorities,webhook,title,hourdif,daydif)
    # schedule.every().day.at('18:00').do(job1,redmine,project_id,query,priorities,webhook,title,hourdif,daydif)
    # schedule.every(20).seconds.do(job1,redmine,project_name,query,tracker_id,priorities,status_name,webhook,title)
    # schedule.every(30).seconds.do(job2)
    # schedule.every(1).minutes.do(job1)
    # schedule.every().day.at('17:49').do(job4)
    # schedule.every(5).to(10).seconds.do(job5)
    while True:
        schedule.run_pending()