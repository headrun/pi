"""from juicer.utils import *
from juicer.items import *
import MySQLdb
import time

class AddressLatLongTerminal(JuicerSpider):
    name = 'address_latlong_terminal'


    def __init__(self, *args, **kwargs):
        super(AddressLatLongTerminal, self).__init__(*args, **kwargs)
        settings.overrides['DOWNLOADER_CLIENTCONTEXTFACTORY'] = \
        'juicer.contextfactory.CustomClientContextFactory'
        self.con = MySQLdb.connect(db='address_components',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
      
        #self.address_qry = 'insert into New_address(id,key,address_original,address_new,formatted_address,geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,location_lat,location_lng,location_type,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng,partial_match,place_id,types,status,reference_url,long_name,short_name,component_type) values (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'       

        self.address_qry = 'insert into pincode_new(sk,Pol_id,availability,formatted_address,geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,location_lat,location_lng,location_type,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng,partial_match,place_id,types,status,reference_url,long_name,short_name,component_type,proxy_ip,pincode,created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'


    def parse(self, response):
        sel = Selector(response)
        import pdb;pdb.set_trace()
        sk = response.meta['sk']
        #pol_id = response.meta['data']['count']
        #availablity =  response.meta['data']['availability']
        data_ = json.loads(response.body)
        data = json.loads(response.body)
        availablity = ''
        add_types_ = '' 
        ip = response.request.meta['proxy']
        pincode =  response.meta['data']['pincode']

        #pol_id = response.meta['count']
        #availablity = response.meta['availability']
        #sk = response.meta['sk']
        
        data_ = data_['results']
        if len(data_) == 2 : 
            add_types = data['results'][1]['types']
            add_types_ = "<>".join(add_types)
        elif len(data_) == 1 :
            add_types = data['results'][0]['types']
            add_types_ = "<>".join(add_types)
        else :
            add_types = ''
     
        status = data['status']
        if status : status = status
        else : status = ''
        if not data_ : 
            #availablity =  response.meta['data']['availability']
            vals = (str(sk),'','','', '','','','','','','','','','', '','','','',str(status),str(response.url),'','','',ip,str(pincode))
	    self.cur.execute(self.address_qry, vals)
	    update_qry = 'update ignore urlqueue_dev.address_crawl set crawl_status = 1 where crawl_status = 9 and  sk="%s" limit 1'% sk
	    self.cur.execute(update_qry)
	    self.con.commit()

     
        else :
            for i in data_ :
                    geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,location_lat,location_lng,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng = '','','','','','','','','',''
                 
		    formatted_address = i.get('formatted_address','').replace(u'\\u0142','l').replace(u'\u0142','l')
                    formatted_address = formatted_address
                    try : formatted_address = MySQLdb.escape_string(formatted_address)#repr(formatted_address)
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
                    vals = (str(sk), '' ,'',formatted_address, geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat,geometry_bounds_sw_lng,json.dumps(location_lat),json.dumps(location_lng),location_type,viewport_ne_lat,viewport_ne_lng,viewport_sw_lat,viewport_sw_lng,str(partial_match),place_id,add_types_,status,normalize(response.url),long_name,short_name,str(types),ip,pincode)
                    self.cur.execute(self.address_qry, vals)
            update_qry = 'update ignore  urlqueue_dev.address_crawl set crawl_status = 1 where crawl_status = 9 and  sk="%s"'% sk
            self.cur.execute(update_qry)
            self.con.commit()


    def normalize(self,text):
        return clean(compact(xcode(text)))

    def xcode(self,text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def compact(self,text, level=0):
        if text is None: return ''
        if level == 0:
            text = text.replace("\r", " ")
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
        return text"""

                    
