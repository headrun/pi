from juicer.utils import *

class MahaRera(JuicerSpider):
	name = 'maharera_browse'
	start_urls = ['https://maharerait.mahaonline.gov.in/PrintPreview/PrintPreview/UHJvamVjdElEPTkxMiZEaXZpc2lvbj01JlVzZXJJRD0yMTI3MSZSb2xlSUQ9MSZBcHBJRD0xMTk3MSZBY3Rpb249U0VBUkNIJkNoYXJhY3RlckQ9OTYmRXh0QXBwSUQ9']

	def parse(self, response):
		sel = Selector(response)
		import pdb;pdb.set_trace()
