from juicer.utils import *
from juicer.items import *
import MySQLdb

class AddressCleanTerminal(JuicerSpider):
    name = 'address_clean_terminal'


    def __init__(self, *args, **kwargs):
        super(AddressCleanTerminal, self).__init__(*args, **kwargs)
        settings.overrides['DOWNLOADER_CLIENTCONTEXTFACTORY'] = \
        'juicer.contextfactory.CustomClientContextFactory'
        self.con = MySQLdb.connect(db='address_components',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
      
        #self.address_qry = 'insert into New_address(id,key,address_original,address_new,formatted_address,geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,location_lat,location_lng,location_type,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng,partial_match,place_id,types,status,reference_url,long_name,short_name,component_type) values (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'       

        self.address_qry = 'insert into Permutations(sk,s_no,key_value,old_address,new_address,address,formatted_address,geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,location_lat,location_lng,location_type,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng,partial_match,place_id,types,status,reference_url,long_name,short_name,component_type) values (%s, %s, %s, %s, %s, %s, %s, %s,%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)'


    def parse(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        address =  response.meta['data']['address']
        old_address = response.meta['data']['old_address']
        key_value = response.meta['data']['key_value']
        new_address = response.meta['data']['new_address']
        s_no = response.meta['data']['s_no']
        yield Request(response.url, self.parse_data,meta={'sk' : sk,'address' : address,'new_address' : new_address,'old_address' : old_address,'s_no' : s_no,'key_value' : key_value} ,  dont_filter=True) 
        
   
    def parse_data(self,response):
        #import pdb;pdb.set_trace()
        data_ = json.loads(response.body)
        data = json.loads(response.body)
        add_types = '' 
        sk = response.meta['sk']
        data_ = data_['results']
        """if len(data_) == 2 : 
            add_types = data['results'][1]['types']
            add_types_ = "<>".join(add_types)
        elif len(data_) == 1 :
            add_types = data['results'][0]['types']
            add_types_ = "<>".join(add_types)
        else :
            add_types = ''"""
     
        new_address = response.meta['new_address']
        key_value = response.meta['key_value']
        old_address = response.meta['old_address']
        address = response.meta['address']
        s_no = response.meta['s_no']

        try : address = MySQLdb.escape_string(address)
        except : address = address.encode('utf8')
        try : old_address = MySQLdb.escape_string(old_address)
        except : old_address= old_address.encode('utf8')

        try : new_address =  MySQLdb.escape_string(new_address)
        except : new_address = new_address.encode('utf8')
        status = data['status']
        if status : status = status
        else : status = ''
        if not data_ : 
            #import pdb;pdb.set_trace()
            vals = (str(sk) ,s_no ,key_value ,old_address ,new_address ,address, '', '','','','','','','','','','', '','','','',str(status),str(response.url),'','','')
	    self.cur.execute(self.address_qry, vals)
	    update_qry = 'update urlqueue_dev.address_crawl set crawl_status = 1 where crawl_status = 9 and  sk="%s" limit 1'% sk
	    self.cur.execute(update_qry)
	    self.con.commit()

     
        else :
            for i in data_ :
                    add_types = ''
                    geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,location_lat,location_lng,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng = '','','','','','','','','',''
                    add_types = i.get('types','')
                    add_types = '<>'.join(add_types)
		    formatted_address = i.get('formatted_address','').replace(u'\\u0142','l').replace(u'\u0142','l')
                    formatted_address = formatted_address
                    try : formatted_address = MySQLdb.escape_string(formatted_address)
                    except : formatted_address = formatted_address.encode('utf-8')
		    geometry_bounds_sw = i.get('geometry','').get('bounds','')
		    if geometry_bounds_sw : 
			geometry_bounds_sw_lat = i.get('geometry','').get('bounds','').get('southwest','').get('lat','')
                        geometry_bounds_sw_lng = i.get('geometry','').get('bounds','').get('southwest','').get('lng','')
                        geometry_bounds_sw_lng = json.dumps(geometry_bounds_sw_lng)
                        geometry_bounds_sw_lat = json.dumps(geometry_bounds_sw_lat)
		    else : geometry_bounds_sw_lat,geometry_bounds_ne_lng = '',''
		    geometry_bounds_ne = i.get('geometry','').get('bounds','')
		    if geometry_bounds_ne : 
			geometry_bounds_ne_lat = geometry_bounds_ne.get('northeast','').get('lat','')
                        geometry_bounds_ne_lng = geometry_bounds_ne.get('northeast','').get('lng','')
                        geometry_bounds_ne_lat = json.dumps(geometry_bounds_ne_lat)
                        geometry_bounds_ne_lng = json.dumps(geometry_bounds_ne_lng)
                        
		    else : geometry_bounds_nei_lat,geometry_bounds_ne_lng = '',''
		    location_lat = i.get('geometry','').get('location','').get('lat','')
                    location_lng = i.get('geometry','').get('location','').get('lng','')
		    location_type = i.get('geometry','').get('location_type','')
		    viewport_ne = i.get('geometry','').get('viewport','')
		    if viewport_ne : 
                        viewport_ne_lat = i.get('geometry','').get('viewport','').get('northeast','').get('lat','')
                        viewport_ne_lng = i.get('geometry','').get('viewport','').get('northeast','').get('lng','')
                        viewport_ne_lat = json.dumps(viewport_ne_lat)
                        viewport_ne_lng = json.dumps(viewport_ne_lng)

		    else : 
                        viewport_ne_lat,viewport_ne_lng = '',''
		    viewport_sw = i.get('geometry','').get('viewport','')
		    if viewport_sw : 
                        viewport_sw_lat = i.get('geometry','').get('viewport','').get('southwest','').get('lat','')
                        viewport_sw_lng = i.get('geometry','').get('viewport','').get('southwest','').get('lng','')
                        viewport_sw_lat = json.dumps(viewport_sw_lat)
                        viewport_sw_lng = json.dumps(viewport_sw_lng)
		    else : 
                        viewport_sw_lat, viewport_sw_lng = '',''
		    partial_match = i.get('partial_match','')
		    place_id = i.get('place_id','')
		    components_data = i.get('address_components','')
                    long_name , types , short_name = [] , [] , []
		    for i in components_data:
                   
			long_name_ = i.get('long_name','').strip("'").replace(u'\\u0142','l').replace(u'\u0142','l').replace(u'\\u0142','l').replace(u'\u0142','l')
                        long_name.append(long_name_)
                   
			types_ = i.get('types','')
                    
			types_ = "<>".join(types_) 
                        types.append(types_)
			short_name_ = i.get('short_name').strip("'").replace(u'\\u0142','l').replace(u'\u0142','l').replace(u'\\u0142','l').replace(u'\u0142','l')
                        short_name.append(short_name_)
                    short_name = normalize("<>".join(short_name))
                    long_name = normalize("<>".join(long_name))
                    types = ",".join(types)
                 
		
                    vals = (str(sk), s_no, key_value, old_address, new_address, address,formatted_address, geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,json.dumps(location_lat),json.dumps(location_lng),location_type,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng,str(partial_match),place_id,add_types,status,normalize(response.url),long_name,short_name,str(types))
                    self.cur.execute(self.address_qry, vals)
                    update_qry = 'update urlqueue_dev.address_crawl set crawl_status = 1 where crawl_status = 9 and  sk="%s" limit 1'% sk
                    self.cur.execute(update_qry)
                    self.con.commit()


    def normalize(self,text):
      
        return clean(compact(xcode(text)))

    def xcode(self,text, encoding='utf8', mode='strict'):
        import pdb;pdb.set_trace()
        return text.encode(encoding, mode) if isinstance(text, unicode) else text
    def compact(self,text, level=0):
        if text is None: return ''

        if level == 0:
            
            text = text.replace("\r", " ")
        import pdb;pdb.set_trace()
        compacted = re.sub("\s\s(?m)", " ", text)
        if compacted != text:
            compacted = compact(compacted, level+1)

        return compacted.strip()

    def clean(self,text):
        if not text: return text

	value = text
	value = re.sub("&amp;", "&", value)
	value = re.sub("&lt;", "<", value)
	value = re.sub("&gt;", ">", value)
	value = re.sub("&quot;", '"', value)
	value = re.sub("&apos;", "'", value)

	return value



    def un(self,text):
        text = text.replace('\t','').replace('\r','').strip()
        return text

                    
