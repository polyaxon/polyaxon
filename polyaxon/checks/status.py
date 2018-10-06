from checks.crons import CronsCheck
from checks.events import EventsCheck
from checks.hpsearch import HPSearchCheck
from checks.pipelines import PipelinesCheck
from checks.postgres import PostgresCheck
from checks.rabbitmq import RabbitMQCheck
from checks.redis import RedisCheck
from checks.scheduler import SchedulerCheck


def get_status():
    status = {}
    status.update(CronsCheck.run())
    status.update(EventsCheck.run())
    status.update(HPSearchCheck.run())
    status.update(PipelinesCheck.run())
    status.update(PostgresCheck.run())
    status.update(RabbitMQCheck.run())
    status.update(RedisCheck.run())
    status.update(SchedulerCheck.run())
    return {k: v.to_dict() for k, v in status.items()}
