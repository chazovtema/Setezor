from aiohttp import web
from setezor.tasks.nmap_scan_task import NmapScanTask


app = web.Application()

routers = []
tasks = [
    NmapScanTask,
    ]
for task in tasks:
    task.spy_computation = True
    routers.append(task.__route__())


app.add_routes(routers)

def run_spy():
    web.run_app(app, host='0.0.0.0', port=NmapScanTask.__port__())
