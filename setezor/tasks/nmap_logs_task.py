from setezor.tasks.nmap_scan_task import NmapScanTask
from setezor.modules.nmap.scanner import NmapScanner
from setezor.modules.nmap.parser import NmapParser
from .base_job import MessageObserver, BaseJob
from setezor.database.queries import Queries
from setezor.tools.ip_tools import get_ipv4, get_mac
from time import time
import traceback
import asyncio

from setezor.modules.nmap.parser import NmapStructure


class NmapLogTask(NmapScanTask):
    
    def __init__(self, observer: MessageObserver, scheduler, name: str, task_id: int, 
                 data: str, scanning_ip: str, scanning_mac: str, nmap_logs: str, agent_id: int, db: Queries):
        super(NmapScanTask, self).__init__(agent_id = agent_id, observer = observer, scheduler = scheduler, name = name, update_graph=False)
        self.agent_id = agent_id
        self.task_id = task_id
        self._coro = self.run(data=data, task_id=task_id, scanning_ip=scanning_ip, scanning_mac=scanning_mac, nmap_logs=nmap_logs, db=db)

    async def _task_func(self, data: str, scanning_ip: str, 
                         scanning_mac: str, nmap_logs: str, agent_id: int) -> NmapStructure:
        """Метод задачи для парсинга xml-логов nmap-а

        Args:
            xml_log (str): xml-логи

        Returns:
            _type_: результат выполнения парсинга логов
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, NmapScanner.save_source_data, nmap_logs, data, 'parse_xml_log')
        log_result = await loop.run_in_executor(None, NmapScanner().parse_xml, data)
        address_data = {'ip': scanning_ip, 'mac': scanning_mac}
        return await loop.run_in_executor(None, NmapParser().parse_hosts, log_result.get('nmaprun'), agent_id, address_data)

    async def run(self, db: Queries, task_id: int, data: str, scanning_ip: str, scanning_mac: str, nmap_logs: str):
        """Метод выполнения задачи
        1. Произвести операции согласно методу self._task_func
        2. Записать результаты в базу согласно методу self._write_result_to_db
        3. Попутно менять статут задачи

        Args:
            db (Queries): объект запросов к базе
            task_id (int): идентификатор задачи
        """
        db.task.set_pending_status(index=task_id)
        ses = db.db.create_session()
        agent = db.agent.get_by_id(session=ses, id=self.agent_id)
        address = agent.ip
        try:
            t1 = time()
            result = await self._task_func(data=data, scanning_ip=address.ip, scanning_mac=address._mac.mac, nmap_logs=nmap_logs, agent_id=self.agent_id)
            self.logger.debug('Task func "%s" finished after %.2f seconds', self.__class__.__name__, time() - t1)
            self._write_result_to_db(db=db, result=result)
            self.logger.debug('Result of task "%s" wrote to db', self.__class__.__name__)
        except Exception as e:
            self.logger.error('Task "%s" failed with error\n%s', self.__class__.__name__, traceback.format_exc())
            db.task.set_failed_status(index=task_id, error_message=traceback.format_exc())
            raise e
        db.task.set_finished_status(index=task_id)