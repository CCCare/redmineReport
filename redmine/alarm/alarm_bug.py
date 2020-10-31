from redmine.common.redmine_common import set_Redmine
from redmine.common.redmine_trackers import get_trackerId_by_name


def get_higher_bugs():
    priorities = ['High','Urgent','Immediate']
    return None

if __name__ == '__main__':
    redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
    redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
    # project_name = 'online'
    project_name = 'dataapi-v4-0-3_beta'
    redmine = set_Redmine(redmine_url, redmine_key)
    tracker_id = get_trackerId_by_name(redmine, "Bug")