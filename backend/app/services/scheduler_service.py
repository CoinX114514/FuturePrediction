"""定时任务服务。

负责管理定时任务，如定期更新价格等。
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor

# 配置日志
logger = logging.getLogger(__name__)


class SchedulerService:
    """定时任务服务类。

    管理所有定时任务的调度。
    """

    def __init__(self):
        """初始化定时任务服务。"""
        # 创建后台调度器
        # 使用线程池执行器，最多 5 个线程
        executors = {
            'default': ThreadPoolExecutor(5)
        }
        
        self.scheduler = BackgroundScheduler(executors=executors)
        self.is_running = False

    def start(self):
        """启动定时任务调度器。"""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("定时任务调度器已启动")

    def stop(self):
        """停止定时任务调度器。"""
        if self.is_running:
            self.scheduler.shutdown(wait=True)
            self.is_running = False
            logger.info("定时任务调度器已停止")

    def add_price_update_job(
        self,
        update_func,
        interval_minutes: int = 10,
        job_id: str = "price_update_job"
    ):
        """添加价格更新定时任务。

        Args:
            update_func: 更新价格的函数，应该接受 db 参数。
            interval_minutes: 更新间隔（分钟），默认 10 分钟。
            job_id: 任务ID，默认 "price_update_job"。
        """
        try:
            # 如果任务已存在，先移除
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.info(f"已移除现有任务: {job_id}")

            # 添加新的定时任务
            # 使用间隔触发器，每 interval_minutes 分钟执行一次
            trigger = IntervalTrigger(minutes=interval_minutes)
            
            self.scheduler.add_job(
                func=update_func,
                trigger=trigger,
                id=job_id,
                name="价格更新任务",
                replace_existing=True,
                max_instances=1,  # 同一时间只允许一个实例运行
                coalesce=True,  # 如果任务被延迟，只执行最后一次
            )
            
            logger.info(f"已添加价格更新任务，间隔: {interval_minutes} 分钟")
            
        except Exception as e:
            logger.error(f"添加价格更新任务失败: {str(e)}", exc_info=True)
            raise

    def remove_job(self, job_id: str):
        """移除指定的定时任务。

        Args:
            job_id: 任务ID。
        """
        try:
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.info(f"已移除任务: {job_id}")
            else:
                logger.warning(f"任务不存在: {job_id}")
        except Exception as e:
            logger.error(f"移除任务失败: {job_id}, 错误: {str(e)}", exc_info=True)

    def get_jobs(self):
        """获取所有定时任务。

        Returns:
            list: 任务列表。
        """
        return self.scheduler.get_jobs()

    def pause_job(self, job_id: str):
        """暂停指定的定时任务。

        Args:
            job_id: 任务ID。
        """
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"已暂停任务: {job_id}")
        except Exception as e:
            logger.error(f"暂停任务失败: {job_id}, 错误: {str(e)}", exc_info=True)

    def resume_job(self, job_id: str):
        """恢复指定的定时任务。

        Args:
            job_id: 任务ID。
        """
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"已恢复任务: {job_id}")
        except Exception as e:
            logger.error(f"恢复任务失败: {job_id}, 错误: {str(e)}", exc_info=True)


# 全局调度器实例
scheduler_service = SchedulerService()



