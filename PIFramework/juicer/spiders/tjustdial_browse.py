import json
import MySQLdb
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request, FormRequest
import md5
import json
import datetime
import csv

class TJustdialbrowse(BaseSpider):
                name        = 'tjustdail_browse'
		start_urls = []
                for i in range(0,200):
                    url = 'https://t.justdial.com/api/india_api_write/10aug2016/searchziva.php?city=Delhi&state=&case=spcall&stype=category_list&search=Architects&national_catid=10020039&lat=28.475934000000&long=77.047949000000&area=Gurgaon Ho&gcity=&garea=&glat=&glon=&max=10&pg_no=%s&rnd1=0.24653&rnd2=0.56421&rnd3=0.93683&wap=2&moviedate=2018-03-14&mvbksrc=ft,pvr,cinemax,fc&jdlite=0&docid=&paidstatus=&darea_flg=1&cat_search_type=L'%str(i)
                    start_urls.append(url)
		handle_httpstatus_list = [401, 404, 302, 303, 403, 500, 100]
		
		def __init__(self, *args, **kwargs):
			super(TJustdialbrowse, self).__init__(*args, **kwargs)
			self.con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="urlqueue_dev",charset="utf8",use_unicode=True)
			self.cur = self.con.cursor()
                        self.domain = 'https://t.justdial.com'
                        self.header_params = []
                        self.todays_excel_file_name = 'Tjustdial_gurguoan_Metadata_on_%s.csv'%str(datetime.datetime.now().date())
                        oupf = open(self.todays_excel_file_name, 'wb+')
                        self.todays_excel_file_name  = csv.writer(oupf)
                        self.todays_excel_file_name.writerow(self.header_params)
                        self.header_params2 = ['No_of_reviews','Reviewed_By','Mobile','Email','Review','Review_rating','Review_date','Emo_count','profile_image','reference_url']

                        self.excel_file_name2 = 'Tjustdial_Reviewsdata_on_%s.csv'%str(datetime.datetime.now().date())
                        oupf2 = open(self.excel_file_name2, 'wb+')
                        self.todays_excel_file2  = csv.writer(oupf2)
                        self.todays_excel_file2.writerow(self.header_params2)
		
                def parse(self,response):
             
                	sel  = Selector(response)
                        import pdb;pdb.set_trace()
                        lat,long_ = '',''
                        json_data = json.loads(response.body)
                        results = json_data.get('results','')
                        print "****************################################*******************************"
                        #print len(results)
			for data in results:
                                doc_id = data.get('docId','')
                                
                                geocodes = data.get('companyGeocodes','')
                                if geocodes : 
                                    lat = geocodes.split(',')[0]
                                    long_ = geocodes.split(',')[-1]         
                                name = data.get('name','')
                                if not name : print response.url
				image = data.get('thumbnail','')
                                address = data.get('address','')
                                total_rev_count = data.get('totalReviews','')
                                new_address = data.get('NewAddress','')
                                name_ = name.replace(' ','-')+'-'+str(new_address).replace(' ','-')
                                landmark = data.get('landmark','')
                                area = data.get('area','')
                                contact = data.get('an',{}).get('l','')
                                rating = data.get('compRating','')
                                url = "https://t.justdial.com/Delhi/"+str(name_)+'/'+str(doc_id)+'_BZDET?vpfs=&stxt=Architects&catid=3663&bdmsgtype=7&bdcaptiontype=6&stype='
				if url:
					yield Request(url, callback = self.parse_meta,meta={'name':name,'image':image,'address':address,'total_rev_count':total_rev_count,'New_address':new_address,'landmark':landmark, 'area':area,'rating':rating,'doc_id':doc_id,'lat':lat,'long_':long_,'reference_url':url} , dont_filter=True)

		def parse_meta(self, response):
			sel  = Selector(response)
                        services_list = []
                        contact = str("<>".join(list(set(sel.xpath('//span[@class="contactNo"]/text()').extract()))))
                        meta_data = json.loads(sel.xpath('//script//text()').extract()[-1].split('window.__data=')[-1].split('; window.__clientInfo=')[0])
                        openhrs = "<>".join(meta_data.get('detailPage',{}).get('data',{}).get('main',{}).get('results',{}).get('HoursOfOperation',''))
                        services = meta_data.get('detailPage',{}).get('data',{}).get('main',{}).get('results',{}).get('services',{}).get('general',[])
                        for service in services :
                            services_ = service.get('att','') 
                            services_list.append(services_)
                        services_list = "<>".join(services_list)
                        year = meta_data.get('detailPage',{}).get('data',{}).get('main',{}).get('results',{}).get('YOE','')
                        doc_id = response.meta.get('doc_id','')
                        try : website =  "<>".join(meta_data.get('detailPage',{}).get('data',{}).get('main',{}).get('results',{}).get('websiteList',''))
                        except : website = ''
                        also_listed_link = "https://t.justdial.com/api/india_api_write/07aug2017/more_listed.php?docid="+str(doc_id)+"&case=listed&jdlite=0"
                        if also_listed_link : yield Request(also_listed_link,callback=self.parse_more_listings,meta={'meta_data':response.meta,'year':year,'openhrs':openhrs,'doc_id':doc_id,'services_list':services_list,'website_list':website,'contact':contact})
                        
                        rating_link = "https://t.justdial.com/api/graph_api/php/qua/GetRatingsFeed.php?docid="+str(doc_id)+"&ps=100&np=1&mobile=&smode=po&wap=2&gdocids=&jdlite=0&referer=https://t.justdial.com/Delhi/Architects/nct-10020039?catid=10020039&nmflg=0"
                        if rating_link : yield Request(str(rating_link),callback=self.parse_ratings,meta={'reference_url':response.url})
             

                def parse_more_listings(self, response):
                        sel = Selector(response)
                        meta_values = response.meta.get('meta_data').values()
                        doc_id = response.meta.get('doc_id','')
                        final_list = ''
                        list_ = []
                        try : 
                            json_data = json.loads(response.body)
                            listing = json_data.get('results',[])
                            for data in listing :
                                cate = data.get('category','')
                                list_.append(cate)
                            final_list = "<>".join(list_)
                        except :  print "no data"
                        image_api = "https://t.justdial.com/api/india_api_write/10aug2016/get_catalogue.php?docid="+str(doc_id)+"&jdlite=0"
                        if image_api :  yield Request(image_api,callback=self.parse_image,meta={'meta_data':response.meta,'year':response.meta.get('year',''),'openhrs':response.meta.get('openhrs',''),'doc_id':doc_id,'more_listing':final_list,'services_list':response.meta.get('services_list',''),'website_list':response.meta.get('website_list',''),'contact':response.meta.get('contact','')})
                        
		
                def parse_ratings(self,response):
                        sel  = Selector(response)
                        total_count = ''
                        rev_data = []
                        json_data = json.loads(response.body)
                        try : total_count = json_data.get('data',{}).get('count',{})
                        except : print response.url
                        if total_count>= 100 : import pdb;pdb.set_trace()
                        rev_data = json_data.get('data',{}).get('rating',[])
                        for rev in rev_data :
                                email = rev.get('email','')
                                review_date = rev.get('age','')
                                if review_date : review_date = datetime.datetime.fromtimestamp(float(review_date)/1000.).strftime("%Y-%m-%d %H:%M:%S")
                                like_count = rev.get('like_count','')
                                #if not like_count : like_count = 0
                                mobile = rev.get('mobile','')
                                name = rev.get('name','')
                                photos = rev.get('photos','')
                                rating = rev.get('rating','')
                                review = rev.get('rev','')
                                #emo_count = rev.get('emo_count','')
                                profile_picture = rev.get('dp','')
                                if 'profilepic/'  in profile_picture : profile_picture = ''
                           
                                values = [total_count,name,mobile,email,review,rating,like_count,review_date,profile_picture,response.meta.get('reference_url')]
                                self.todays_excel_file2.writerow(values)

                def parse_image(self,response):
                	sel =  Selector(response)
                        meta_values = response.meta.get('meta_data',{}).get('meta_data',{})
                        year = response.meta.get('meta_data').get('year','')
                        openhrs = response.meta.get('meta_data').get('openhrs','')
                        name = meta_values.get('name','')
                        image = meta_values.get('image','')
                        Full_address = meta_values.get('address','')
                        tot_rev_count = meta_values.get('total_rev_count','')
                        New_address = meta_values.get('New_address','')
                        lat = meta_values.get('lat','')
                        long_ = meta_values.get('long_','')
                        landmark =  meta_values.get('landmark','')
                        area = meta_values.get('area','')
                        contact = response.meta.get('contact','')
                        rating = meta_values.get('rating','')
                        reference_url = meta_values.get('reference_url','')
                        more_listing =  response.meta.get('more_listing','')
                        image_list = []
                        try : 
                            json_data = json.loads(response.body)
                            data = json_data.get('res',[])
                            for img in data :
                                url = img.get('io','')
                                if url : url = "https://content.jdmagicbox.com/" + str(url)
                                image_list.append(url)
                            if image_list : image_list = "<>".join(image_list)
                        except : image_list = ''
                        final = [name,Full_address,New_address,landmark,area,tot_rev_count,rating,contact,lat,long_]+[response.meta.get('year','')]+[response.meta.get('openhrs','')] + [response.meta.get('services_list','')]+ [more_listing] +[response.meta.get('website_list','')] + [image_list] + [reference_url]
             
                        self.todays_excel_file_name.writerow(final)
                  
