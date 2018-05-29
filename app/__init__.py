from apistar import ASyncApp
from .routes import license_routes
from base.license import LicenseComponent

__all__ = ['app']

app = ASyncApp(
    routes=license_routes,
    components=[LicenseComponent(), ],
)
