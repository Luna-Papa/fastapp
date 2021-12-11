# 消息中间件 Broker
# Broker ，即为任务调度队列，接收任务生产者发来的消息（即任务），将任务存入队列
broker_url = "redis://127.0.0.1:6379/0"
# Backend 用于存储任务的执行结果，以供查询。
# 同消息中间件一样，存储也可使用 RabbitMQ, Redis 和 MongoDB 等。
result_backend = "redis://127.0.0.1:6379/1"  # 使用redis存储结果
# 指定任务序列化方式
task_serializer = 'json'
# 指定结果序列化方式
result_serializer = 'json'
# 指定任务接受的序列化类型.
accept_content = ['json']
timezone = "Asia/Shanghai"  # 时区设置
worker_hijack_root_logger = False  # celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
result_expires = 60 * 60 * 24  # 存储结果过期时间（默认1天）

# celery_imports = (                                  # 指定导入的任务模块
#     'celery_app.tasks',
# )
