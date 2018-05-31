from api import license
from apistar import Route

license_routes = [
    Route('/license/configs', method='GET', handler=license.get_license_configs),
]
