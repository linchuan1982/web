from celery.schedules import crontab

# 导入任务所在文件
imports = [
    'analysis.fetch',  # 导入py文件
    'data.download',
]

timezone = 'Asia/Shanghai'


# 需要执行任务的配置
beat_schedule = {
    'fetch': {
        'task': 'analysis.fetch.fetch_all',  #执行的函数
        'schedule': crontab(minute='*/30'),   # every minute 每分钟执行
        'args': ()  # # 任务函数参数
    },
    'check': {
        'task': 'data.download.check_assets',  #执行的函数
        'schedule': crontab(minute='*/120'),   # every minute 每分钟执行
        'args': ()  # # 任务函数参数
    },
}
