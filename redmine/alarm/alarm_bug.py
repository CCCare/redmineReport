import datetime

from redmine.common.base.config_operate import ReadConfig
from redmine.common.redmine_common import MyRedmine
from redmine.common.redmine_issues import MyIssue
from redmine.tools import json_file
# from redmine.tools.dingtalk import send_dingtalk_markdown
from redmine.tools.dingtalk import send_dingtalk_markdown

def get_higher_bugs(issues,priorities):

    final = {}
    for priority in priorities:
        pri_list = []
        for i in issues:
            try:
                if str(i.priority.name) == priority:
                    pri_list.append(i.id)
            except Exception as e:
                pass
        final[priority] = pri_list
    return final

def get_recent_updated_issues(issues,hourdif):
    recent_issues = []
    for issue in issues:
        history = issue.journals
        history = sorted(history, key=lambda his: his.created_on,reverse=True)
        create_on = None
        for his in history:
            details = his.details
            for detail in details:
                if(detail["name"] == 'status_id' and detail["new_value"] == '3'):
                    create_on = his.created_on
                    break
            if create_on is not None:
                break
        # date = ((datetime.datetime.now() - datetime.timedelta(hours=timedif)).strptime("%Y-%m-%d %H:%M:%S"))
        # date = datetime.datetime.strptime((datetime.datetime.now() - datetime.timedelta(hours=timedif)),"%Y-%m-%d %H:%M:%S")
        date = datetime.datetime.now() - datetime.timedelta(hours=hourdif)
        if(create_on is not None):
            if(create_on>date):
                recent_issues.append(issue)
    return recent_issues


# def compare_alarm_bugs(prepare_bugs,query_name):
#     result_bugs = dict()
#     file_path = "alarm_bug.json"
#     last_bugs = json_file.read_json_file(file_path)
#     if(last_bugs is None or not last_bugs or last_bugs[query_name] is None or not last_bugs[query_name]):
#         result_bugs = prepare_bugs
#     else:
#         pingtai_last_bugs = last_bugs[query_name]
#         for key in prepare_bugs.keys():
#             tmp_bug_ids=[]
#             prepare_bug_ids = prepare_bugs[key]
#             last_bug_ids = pingtai_last_bugs[key]
#             for bug_id in prepare_bug_ids:
#                 if bug_id not in last_bug_ids:
#                     tmp_bug_ids.append(bug_id)
#             result_bugs[key] = tmp_bug_ids
#     return result_bugs

def merge(higher_bugs,not_closed_bugs):
    higher_bugs['long_time_no_close']=not_closed_bugs
    return higher_bugs

def generate_dingtalk_message(redmine,result_bugs,hourdif,daydif):
    result_text = ""
    for pingtai_name in result_bugs.keys():
        n = 0
        m = 0
        higher_bug_text = ""
        not_closed_text = ""
        pingtai_bugs = result_bugs[pingtai_name]
        for key in pingtai_bugs :
            bugs = pingtai_bugs[key]
            myIssue = MyIssue(redmine)
            if( bugs is not None and len(bugs)!=0):
                if(key != 'long_time_no_close'):
                    higher_bug_text = higher_bug_text + "#### " + key + ":\n"
                    for bug_id in bugs :
                        n = n+1
                        bug = myIssue.get_issue_by_id(bug_id)
                        higher_bug_text = higher_bug_text + "* ["+bug.subject+"]("+redmine.url+"/issues/%s) \n" %(bug.id)
                else:
                    not_closed_bugs = pingtai_bugs[key]
                    if (not_closed_bugs is not None and len(not_closed_bugs) != 0):
                        for nc_bug_id in not_closed_bugs:
                            bug = myIssue.get_issue_by_id(nc_bug_id)
                            not_closed_text = not_closed_text + "* [" + bug.subject + "](" + redmine.url + "/issues/%s) \n" % (
                                bug.id)
                            m = m + 1
        if (n==0 and m==0):
            text = None
        else:
            text = "> ### %s小时内新增待验证的高优先级BUG<font color=#FF0000> %s </font>个：\n" %(hourdif,n) + higher_bug_text
            # text = "### 新增待验证的高优先级BUG<font color='red'> %s </font>个：\n" %(n) + higher_bug_text
            text = text + "> ### 超过%s天未验证的BUG<font color=#FF0000> %s </font>个：\n" % (daydif,m) + not_closed_text
            result_text = result_text +"## "+ pingtai_name + "\n" + text+"\n"
    print(result_text)
    return result_text

def get_long_time_no_deal_bugs(issues,day):
    long_time_no_deal_bugs = []
    if(issues is None):
        return []
    else:
        for issue in issues:
            update_time = issue.updated_on
            now = datetime.datetime.now()
            dayDiff = (now-update_time).days
            # print(dayDiff)
            if(dayDiff>day):
                long_time_no_deal_bugs.append(issue.id)
    return long_time_no_deal_bugs

def get_result(redmine,project_name,query,priorities,hourdif,daydif):
    final={}
    if query is not None:
        for query_name in query.keys():
            myIssue = MyIssue(redmine)
            issues = myIssue.get_issues_by_query_id(project_name, query[query_name])
            recent_issues = get_recent_updated_issues(issues,hourdif)
            higher_bugs = get_higher_bugs(recent_issues, priorities);
            long_time_no_deal_bugs = get_long_time_no_deal_bugs(issues, daydif)
            prepare_bugs = merge(higher_bugs, long_time_no_deal_bugs)
            # result_bugs = compare_alarm_bugs(prepare_bugs,query_name)
            final[query_name] = prepare_bugs
    return final

if __name__ == '__main__':
    config = ReadConfig()
    project_id = config.ALARM_PROJECT
    redmine = MyRedmine(config.REDMINE_URL,config.REDMINE_KEY).redmine
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token='+config.WEBHOOK  #填写你自己创建的机器人
    title = config.MESSAGE_TITLE
    query = config.ALARM_QUERY
    priorities = config.ALARM_PRIORITIES
    hourdif=config.HOUR_DIFF
    daydif=config.DAY_DIFF
    final=get_result(redmine, project_id,query,priorities,hourdif,daydif)
    text = generate_dingtalk_message(final,hourdif,daydif)
    # send_dingtalk_markdown(redmine,webhook,title,text)
