from multiprocessing import Process
from datetime import timedelta

import falcon

from dreadfort.api.http_log.resources import PublishMessageResource
from dreadfort.api.version.resources import VersionResource
from dreadfort import config
from dreadfort import env
from dreadfort.correlation import receiver
from dreadfort.personas.common import publish_stats
from dreadfort.queue import celery
from dreadfort.sinks.elasticsearch import ElasticSearchStreamBulker


_LOG = env.get_logger(__name__)


def start_up():
    try:
        config.init_config()
    except config.cfg.ConfigFilesNotFoundError as ex:
        _LOG.exception(ex.message)

    application = api = falcon.API()
    api.add_route('/', VersionResource())

    # http correlation endpoint
    api.add_route('/v1/tenant/{tenant_id}/publish', PublishMessageResource())

    # syslog correlation endpoint
    server = receiver.new_correlation_input_server()

    server_proc = Process(target=server.start)
    server_proc.start()

    _LOG.info(
        'ZeroMQ reception server started as process: {}'.format(
            server_proc.pid)
    )

    celery.conf.CELERYBEAT_SCHEDULE = {
        'worker_stats': {
            'task': 'stats.publish',
            'schedule': timedelta(seconds=publish_stats.WORKER_STATUS_INTERVAL)
        },
    }

    # include blank argument to celery in order for beat to start correctly
    celery_proc = Process(target=celery.worker_main, args=[['', '--beat']])
    celery_proc.start()
    _LOG.info(
        'Celery started as process: {}'.format(celery_proc.pid)
    )

    es_flusher = ElasticSearchStreamBulker()
    flush_proc = Process(target=es_flusher.start)
    flush_proc.start()
    _LOG.info(
        'ElasticSearchStreamBulker started as process: {}'.format(
            flush_proc.pid)
    )
    return application
