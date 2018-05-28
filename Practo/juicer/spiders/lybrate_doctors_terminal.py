from juicer.utils import *
from juicer.items import DoctorMeta, DoctorHospital
from lybrate_doctors_xpaths import *

class LybrateDoctors(JuicerSpider):
    name = 'lybrate_doctors_terminal'
    handle_http_status_list = ['302', '504']

    def __init__(self, *args, **kwargs):
        super(LybrateDoctors, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"

    def parse(self, response):
        sel = Selector(response)
        dct_id = response.meta['sk']

