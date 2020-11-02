import datetime

from redmine.common.redmine_common import set_Redmine
from redmine.common.redmine_issues import get_issues, get_issue_by_id
from redmine.common.redmine_trackers import get_trackerId_by_name
from redmine.tools import json_file
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

def compare_alarm_bugs(prepare_bugs,query_name):
    result_bugs = dict()
    file_path = "alarm_bug.json"
    last_bugs = json_file.read_json_file(file_path)
    if(last_bugs is None or not last_bugs or last_bugs[query_name] is None or not last_bugs[query_name]):
        result_bugs = prepare_bugs
    else:
        pingtai_last_bugs = last_bugs[query_name]
        for key in prepare_bugs.keys():
            tmp_bug_ids=[]
            prepare_bug_ids = prepare_bugs[key]
            last_bug_ids = pingtai_last_bugs[key]
            for bug_id in prepare_bug_ids:
                if bug_id not in last_bug_ids:
                    tmp_bug_ids.append(bug_id)
            result_bugs[key] = tmp_bug_ids
    return result_bugs

def save_data(result_bugs):
    # alarm_bugs = merge(higher_bugs, not_closed_bugs)
    file_path = "alarm_bug.json"
    json_file.write_json_file(result_bugs,file_path)


def merge(higher_bugs,not_closed_bugs):
    higher_bugs['long_time_no_close']=not_closed_bugs
    return higher_bugs

def generate_dingtalk_message(redmine, result_bugs):
    result_text = ""
    for pingtai_name in result_bugs.keys():
        n = 0
        m = 0
        higher_bug_text = ""
        not_closed_text = ""
        pingtai_bugs = result_bugs[pingtai_name]
        for key in pingtai_bugs :
            bugs = pingtai_bugs[key]
            if( bugs is not None and len(bugs)!=0):
                if(key != 'long_time_no_close'):
                    higher_bug_text = higher_bug_text + "#### " + key + ":\n"
                    for bug_id in bugs :
                        n = n+1
                        bug = get_issue_by_id(redmine,bug_id)
                        higher_bug_text = higher_bug_text + "* ["+bug.subject+"]("+redmine.url+"/issues/%s) \n" %(bug.id)
                else:
                    not_closed_bugs = pingtai_bugs[key]
                    if (not_closed_bugs is not None and len(not_closed_bugs) != 0):
                        for nc_bug_id in not_closed_bugs:
                            bug = get_issue_by_id(redmine, nc_bug_id)
                            not_closed_text = not_closed_text + "* [" + bug.subject + "](" + redmine.url + "/issues/%s) \n" % (
                                bug.id)
                            m = m + 1
        if (n==0 and m==0):
            text = None
        else:
            text = "### 新增待验证的高优先级BUG%s个：\n" %(n) + higher_bug_text
            text = text + "### 长时间未验证的BUG%s个：\n" % (m) + not_closed_text
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

def get_result(redmine, project_name,query,tracker_id, status_name,priorities):
    final={}
    if query is not None:
        for query_name in query.keys():
            issues = get_issues(redmine, project_name, query[query_name], tracker_id, status_name)
            higher_bugs = get_higher_bugs(issues, priorities);
            long_time_no_deal_bugs = get_long_time_no_deal_bugs(issues, 3)
            prepare_bugs = merge(higher_bugs, long_time_no_deal_bugs)
            result_bugs = compare_alarm_bugs(prepare_bugs,query_name)
            final[query_name] = result_bugs
    return final

if __name__ == '__main__':
    redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
    redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
    project_name = 'online'
    priorities = ['High', 'Urgent', 'Immediate']
    status_name = "Resolved"
    redmine = set_Redmine(redmine_url, redmine_key)
    tracker_id = get_trackerId_by_name(redmine, "Bug")
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=1327a4db1da11ec25e51569678f69241039e18e1426301e535b73961643ee665'  #填写你自己创建的机器人
    title = '【测试】线上BUG提醒'
    query = {}
    query['资产平台'] = 120
    query['离线计算'] = 128
    query['实时计算'] = 129
    query['应用平台'] = 130
    final=get_result(redmine, project_name,query,tracker_id, status_name,priorities)
    save_data(final)
    text = generate_dingtalk_message(redmine, final)
    send_dingtalk_markdown(webhook,title,text)
