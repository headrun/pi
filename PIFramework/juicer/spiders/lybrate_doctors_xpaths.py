doc_nodes = '//div[@class="grid__col-11 grid__col-lt-md-20"]//div[@class="grid"]'
#doctorinfo
photo_xpath = './div[@class="grid__col-14 grid__col-xs-20 grid--direction-row"]//a/div[@class="ly-avatar round"]/img//@src'
name_xpath = './div[@class="grid__col-14 grid__col-xs-20 grid--direction-row"]//div[@class="grid__col-15 lybPad-top"]/h2[@itemprop="name"]/a[@itemprop="url"]/text()'
link_xpath = './/div[@class="grid__col-15 lybPad-top"]/h2[@itemprop="name"]/a[@itemprop="url"]/@href'
qua_xpath = './/div[@class="grid__col-15 lybPad-top"]/div[@class="lybEllipsis ly-doctor__degree grid__col-20"]//text()'
spe_xpath = './/div[@class="grid__col-15 lybPad-top"]//div[@itemprop="medicalSpecialty"]//text()'
clic_xpath = './/div[@class="grid__col-15 lybPad-top"]/div[@itemprop="branchOf"]/a/span[@itemprop="name"]//text()'
cic_img_xpath = './/div[@class="ly-doctor__clinic-photos grid--direction-row lybMar-top--half"]//span/div/img/@ng-src'
st_ad_xpath = './/div[@class="grid__col-15 lybPad-top"]//span[@itemprop="address"]/span[@itemprop="streetAddress"]//text()'
loc_ad_xpath = './/div[@class="grid__col-15 lybPad-top"]//span[@itemprop="address"]/span[@itemprop="addressLocality"]//text()'
ad_re_xpath = './/div[@class="grid__col-15 lybPad-top"]//span[@itemprop="address"]/span[@itemprop="addressRegion"]//text()'
ad_cou_xpath = './/div[@class="grid__col-15 lybPad-top"]//span[@itemprop="address"]/meta[@itemprop="addressCountry"]/@content'
ad_pos_xpath = './/div[@class="grid__col-15 lybPad-top"]//span[@itemprop="address"]/meta[@itemprop="postalCode"]/@content'
consulted_xpath = './/div[@class="grid__col-15 lybPad-top"]//div[@class="lybText--light lybMar-top"]/span/text()'
lat_xpath = './/div[@class="grid__col-15 lybPad-top"]//span[@itemprop="geo"]/meta[@itemprop="latitude"]/@content'
lon_xpath = './/div[@class="grid__col-15 lybPad-top"]//span[@itemprop="geo"]/meta[@itemprop="longitude"]/@content'
rat_xpath = './/div[@class="grid--direction-row grid--wrap grid__col-xs-20 hack"]/div[@class="grid__col-xs-10 grid--direction-row"]/span[@class="lybText--green"]/text()'
vote_xpath = './/div[@class="grid--direction-row grid--wrap grid__col-xs-20 hack"]/div[@class="grid__col-xs-10 grid--direction-row"]//span[contains(text(),"ratings")]/text()'
exp_xpath = './/div[@class="grid--direction-row grid--wrap grid__col-xs-20 hack"]/div[@class="grid__col-xs-10 grid--direction-row"]/span[@class="lybGreen"]/text()'
cur_xpath = './/div[@class="grid--direction-row grid--wrap grid__col-xs-20 hack"]/div[@class="grid__col-xs-10 grid--direction-row"]/ly-svg-icon[@p="cash"]/following-sibling::span[1]/text()'
cur_mny_xpath = './/div[@class="grid--direction-row grid--wrap grid__col-xs-20 hack"]/div[@class="grid__col-xs-10 grid--direction-row"]/ly-svg-icon[@p="cash"]/following-sibling::span[2]/text()'
avai_xpath = './/div[@class="grid--direction-row grid--wrap grid__col-xs-20 hack"]/div[@class="grid__col-20 grid--direction-row grid--align-center grid--justify-start"]/span/text()'
sch_xpath = './/div[@class="grid--direction-row grid--wrap grid__col-xs-20 hack"]/div[@class="today-time lybGrey"]/div/span/text()'
