import unittest

from meniscus.data.model.worker import SystemInfo
from meniscus.data.model.worker import Worker
from meniscus.data.model.worker import WorkerConfiguration
from meniscus.data.model.worker import WorkerRegistration


def suite():
    suite = unittest.TestSuite()
    suite.addTest(WhenTestingWorkerObject())
    suite.addTest(WhenTestingWorkerRegistrationObject())
    suite.addTest(WhenTestingSystemInfoObject())
    suite.addTest(WhenTestingWorkerConfigurationObject())


class WhenTestingWorkerObject(unittest.TestCase):

    def setUp(self):
        self.system_info = SystemInfo()

        self.test_worker = Worker(_id='010101',
                                  worker_id='0123456789',
                                  worker_token='9876543210',
                                  hostname='worker01',
                                  callback='172.22.15.25:8080/v1/config/',
                                  ip_address_v4='172.23.1.100',
                                  ip_address_v6='::1',
                                  personality='worker.correlation',
                                  status='new',
                                  system_info=self.system_info.format())
        self.test_worker_lite = Worker(hostname='worker01',
                                       callback='172.22.15.25:8080/v1/config/',
                                       ip_address_v4='172.23.1.100',
                                       ip_address_v6='::1',
                                       personality='worker.correlation',
                                       status='new',
                                       system_info=self.system_info.format())
        self.worker_pipeline = self.test_worker.get_pipeline_info()

    def test_new_worker_no_ids(self):
        worker_dict = self.test_worker_lite.format()
        self.assertTrue('worker_id' in worker_dict)
        self.assertTrue('worker_token' in worker_dict)

    def test_new_worker_format_for_save(self):
        self.assertTrue('_id' in self.test_worker.format_for_save())

    def test_new_worker_get_registration_identity(self):
        self.assertTrue('personality_module'
                        in self.test_worker.get_registration_identity())

    def test_new_worker_pipeline(self):
        self.assertEqual(self.worker_pipeline['hostname'], 'worker01')
        self.assertEqual(self.worker_pipeline['ip_address_v4'], '172.23.1.100')
        self.assertEqual(self.worker_pipeline['ip_address_v6'], '::1')
        self.assertEqual(
            self.worker_pipeline['personality'], 'worker.correlation')


class WhenTestingWorkerRegistrationObject(unittest.TestCase):
    def setUp(self):
        self.worker_reg = WorkerRegistration('correlation', 'new')

    def test_WorkerRegistration_new(self):
        worker_dict = self.worker_reg.format()
        self.assertTrue('hostname' in worker_dict)
        self.assertTrue('callback' in worker_dict)
        self.assertTrue('ip_address_v4' in worker_dict)
        self.assertTrue('ip_address_v6' in worker_dict)
        self.assertTrue('personality' in worker_dict)
        self.assertTrue('status' in worker_dict)
        self.assertTrue('system_info' in worker_dict)


class WhenTestingSystemInfoObject(unittest.TestCase):
    def setUp(self):
        self.system_info = SystemInfo(
            cpu_cores='4',
            os_type='Darwin-11.4.2-x86-64bit',
            memory_mb='1024',
            architecture='x86_64',
            load_average={
                "1": 0.24755859375,
                "5": 1.0751953125,
                "15": 0.9365234375
            },
            disk_usage={
                "/dev/sda1": {
                    "total": 313764528,
                    "used": 112512436
                }
            }
        )

    def test_new_system_info_obj(self):
        self.assertEqual(self.system_info.cpu_cores, '4')
        self.assertEqual(self.system_info.os_type, 'Darwin-11.4.2-x86-64bit')
        self.assertEqual(self.system_info.memory_mb, '1024')
        self.assertEqual(self.system_info.architecture, 'x86_64')
        self.assertEqual(
            self.system_info.disk_usage["/dev/sda1"],
            {
                "total": 313764528,
                "used": 112512436
            }
        )
        self.assertEqual(self.system_info.load_average["1"], 0.24755859375)
        self.assertEqual(self.system_info.load_average["5"], 1.0751953125)
        self.assertEqual(self.system_info.load_average["15"], 0.9365234375)

    def test_new_system_info_empty_obj(self):
        system_info = SystemInfo()
        system_dict = system_info.format()
        self.assertTrue('cpu_cores' in system_dict)
        self.assertTrue('os_type' in system_dict)
        self.assertTrue('memory_mb' in system_dict)
        self.assertTrue('architecture' in system_dict)
        self.assertTrue('load_average' in system_dict)
        self.assertTrue('disk_usage' in system_dict)


class WhenTestingWorkerConfigurationObject(unittest.TestCase):

    def setUp(self):
        self.worker_config = WorkerConfiguration(
            "correlation",
            "meniscus.personas.worker.correlation",
            "94d6176b-9188-4409-8648-7374d0326e6b",
            "8cc3b103-9b23-4e1c-afb1-8c5973621b55",
            "http://172.22.15.25:8080/v1")

    def test_worker_configuration(self):
        self.assertEqual(self.worker_config.personality, 'correlation')
        self.assertEqual(self.worker_config.personality_module,
                         'meniscus.personas.worker.correlation')
        self.assertEqual(self.worker_config.worker_token,
                         '94d6176b-9188-4409-8648-7374d0326e6b')
        self.assertEqual(self.worker_config.worker_id,
                         '8cc3b103-9b23-4e1c-afb1-8c5973621b55')
        self.assertEqual(self.worker_config.coordinator_uri,
                         'http://172.22.15.25:8080/v1')

    def test_worker_configuration_format(self):
        worker_dict = self.worker_config.format()
        self.assertEqual(worker_dict['personality'], 'correlation')
        self.assertEqual(worker_dict['personality_module'],
                         'meniscus.personas.worker.correlation')
        self.assertEqual(worker_dict['worker_token'],
                         '94d6176b-9188-4409-8648-7374d0326e6b')
        self.assertEqual(worker_dict['worker_id'],
                         '8cc3b103-9b23-4e1c-afb1-8c5973621b55')
        self.assertEqual(worker_dict['coordinator_uri'],
                         'http://172.22.15.25:8080/v1')


if __name__ == '__main__':
    unittest.main()