from juicer.utils import *


con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="Men_Names",charset="utf8",use_unicode=True)
cur = con.cursor()

class BabyNamesTerminal(JuicerSpider):
    name = 'baby_names_terminal'
    handle_httpstatus_list = [301,302,204,401, 404,303, 403, 500, 100]

    def parse(self,response):
        sel = Selector(response)
        sk = response.meta['sk']
        ref_url = response.meta['data']['ref_url']
        name = extract_data(sel, '//section[contains(@class, "single left")]//table//tr//td/b[contains(text(),"Name:")]/../../td/text()')
        gender = extract_data(sel, '//section[contains(@class, "single left")]//table//tr//td/b[contains(text(),"Gender:")]/../../td/text()')
        names_similar = '<>'.join(sel.xpath('//div[contains(text(),"Names Similar")]/../div/a/text()').extract())
        meaning_name = ''.join(sel.xpath('//div/b[contains(text(),"Meaning of")]/..//following-sibling::div/div/text()').extract()).replace('; ','<>')
        popularity = extract_data(sel,'//section[contains(@class, "single left")]//table//tr//td/s/text()')
        origin = '<>'.join(response.xpath('//div/b[contains(text(),"Origin / Tag / Usage")]/..//following-sibling::div/div/ul/li/em/i[not(contains(@style,"width:0%"))]/../../a/text()').extract())
        origin1 = '<>'.join(response.xpath('//div/b[contains(text(),"Origin / Tag / Usage")]/..//following-sibling::div/div/ul/li/a/text()').extract())
        famous_pe,famous_people=[],[]
        nodes = response.xpath('//div[@class="celeb"]/div')
        for node in nodes:
            ra=node.xpath('./div/text()').extract()
            famous_pe.append(ra)
        for fa in famous_pe:
            people = ','.join(fa)
            famous_people.append(people)
        famous_names='<>'.join(famous_people)
        if name and sk:
            print name
            query = "insert into baby_names(sk,name,gender,similar_names,meaning_name,popularity,name_usage,origin_usage,famous_names,reference_url,main_url,created_at,modified_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now(),reference_url=%s,origin_usage=%s"
            values = (normalize(sk),normalize(name),normalize(gender),normalize(names_similar),normalize(meaning_name),normalize(popularity),normalize(origin),normalize(origin1),normalize(famous_names),normalize(response.url),normalize(ref_url),normalize(response.url),normalize(origin1))
            cur.execute(query,values)
            con.commit()
            up_qry = 'update urlqueue_dev.baby_crawl set crawl_status=1 where crawl_status=9 and url="%s"' %str(response.url)
            cur.execute(up_qry)
            con.commit()
