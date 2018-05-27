from api import license
from apistar import Route

license_routes = [
    Route('/', method='GET', handler=license.hello),
]
