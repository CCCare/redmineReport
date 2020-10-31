# 获取跟踪标签
def get_trackers(redmine):
    trackers = redmine.tracker.all()
    return trackers


def get_trackerId_by_name(redmine, name):
    trackers = get_trackers(redmine)
    for tracker in trackers:
        if tracker.name == name:
            return tracker.id