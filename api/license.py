from base.license import License
from base import log


async def get_license_configs(lic: License, show_global: bool = False):
    # result, error = await lic.get_license_configs({'global': show_global})
    # if error:
    #     return {'data': None, 'result': False, 'message': result}
    # return {'data': result, 'result': True, 'message': None}
    return {1: 1, 2: 2}
