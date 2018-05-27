from apistar import ASyncApp
from .urls import license_routes

__all__ = ['app']

app = ASyncApp(routes=license_routes)
