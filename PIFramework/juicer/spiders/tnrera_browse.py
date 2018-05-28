from juicer.utils import *

class SampleProject(JuicerSpider):
    name = "sample_browse"
    start_urls = ["http://www.tnrera.in/index.php"]

    def parse(self, response):
        sel = Selector(response)
        links = extract_list_data(sel, '//li/a[contains(text(), "REGISTERED")]/../div//li//@href')
        for link in links:
            if "http" in link:
                yield Request(link, callback=self.parse_next)

    def parse_next(self, response):
        sel = Selector(response)
        import pdb;pdb.set_trace()
        links = extract_list_data(sel, '//ul[@class="list-inline"]//a/@href')
        for link in links:
            yield Request(link, callback=self.parse_meta)

    def parse_meta(self, response):
        sel = Selector(response)
        nodes = get_nodes(sel, '//table[@id="example"]//tbody//tr')
        for node in nodes:
            sno = extract_data(node, './/td[1]/text()')
            project_registration_no = extract_data(node, './/td[2]/text()')
            name_of_applicant = extract_data(node, './/td[3]/text()')
            agents = project_details = extract_data(node, './/td[4]/text()')
            agent_type = approval_details = extract_data(node, './/td[5]/text()')
            validity = project_completion = extract_data(node, './/td[6]/text()')
            other_links = extract_list_data(node, './/td[7]//a//@href')
            current_status_link = extract_data(node, './/td[8]//a//@href')
            current_status = extract_data(node, './/td[9]//text()')

