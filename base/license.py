import requests
from . import log
from apistar.server.components import Component


class License(object):
    def __init__(self):
        self.master_ip = '10.20.0.135'  # master 节点的ip地址
        self.all_ips = []  # 所有节点的ip
        self.port = 50598

    @staticmethod
    def _get(url, params: dict):
        """
        :param url: the url of license server api
        :param params: the params of http get
        :return: result, error
        """
        error = None
        try:
            response = requests.get(url, params, verify=False)
            if response.status_code == 200:
                result = response.json()
            else:
                result, error = response.content, True
                log.error('request license api error: url[%s], detail: %s' % (response.url, result))
        except Exception as e:
            result, error = str(e), True
            log.error('request license api error: %s', result)
        return result, error

    def url_format(self, url: str):
        return 'https://{ip}:{port}{url}'.format(ip=self.master_ip, port=self.port, url=url)

    async def get_license_configs(self, params: dict):
        url = self.url_format('/api/license/configs')
        return self._get(url, params)


class LicenseComponent(Component):
    def resolve(self) -> License:
        return License()
