from juicer.utils import *
import MySQLdb
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from maharera_insertqueries import *


class MahareraTerminal(JuicerSpider):
    name='maharera_browse_crawl1'
    start_urls=['https://maharerait.mahaonline.gov.in/SearchList/Search']

    def __init__(self, *args, **kwargs):
        super(MahareraTerminal, self).__init__(*args, **kwargs)
        self.domain = 'https://maharerait.mahaonline.gov.in'
        self.con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="MAHARERA",charset="utf8",use_unicode=True)
        self.cur = self.con.cursor()

    def parse(self, response):
        sel = Selector(response)
        data = [('__RequestVerificationToken', 'z6YMmQ9D2IdQTDjjmXkezO0FZPqzV0jPvDcwIytncECaz1Yt-ungGlhW6x-6NPfQ15_y7ro1TMT6jRi0-HBV8g-qzm75z-8ecZGUUX9mVBg1'), ('Type', 'Promoter'), ('ID', '0'), ('pageTraverse', '1'), ('Project', ''), ('hdnProject', ''), ('hdnProject', ''), ('Promoter', 'TATA'), ('hdnPromoter', ''), ('CertiNo', ''), ('hdnCertiNo', ''), ('State', ''), ('Division', ''), ('hdnDivision', ''), ('hdnDistrict', ''), ('hdnDTaluka', ''), ('hdnVillage', ''), ('hdnState', ''), ('District', ''), ('Taluka', ''), ('Village', ''), ('CompletionDate_From', ''), ('hdnfromdate', ''), ('CompletionDate_To', ''), ('hdntodate', ''), ('PType', ''), ('hdnPType', ''), ('btnSearch', 'Search')]

        cookies = {'__RequestVerificationToken': 'DVMgpZ7-it-9SJB0joEdAnCTfhcymY1hMn4LGMGcSbBlc_aowW21Ze_46d3wKysWzB6FBzLNYGyYDNKaE5HIK8VI_t_NgZyUM2mkTz6MTgQ1', 'ASP.NET_SessionId': 'yjoaj45lc4ohojrd3u4dpkof'}

        headers = {'Host': 'maharerait.mahaonline.gov.in', 'Accept-Language': 'en-US,en;q=0.5', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Referer': 'https://maharerait.mahaonline.gov.in/SearchList/Search', 'Upgrade-Insecure-Requests': '1', 'Content-Type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:56.0) Gecko/20100101 Firefox/56.0'}

        yield FormRequest('https://maharerait.mahaonline.gov.in/SearchList/Search', headers=headers, cookies=cookies, formdata=data, dont_filter = True, callback = self.parse_next)

    def parse_next(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//table[@class="table table-striped grid-table"]//tr')
        for node in nodes :
            view_link = node.xpath('.//td//@href').extract()
            data_ = node.xpath('.//td//text()').extract()
            data = data_[0:5]
           
            if not data : continue
            sr_no,proj_name,promoter_name,last_modified,view_details = data
            if view_link :
                view_link = self.domain + "".join(view_link)
                main_values = (normalize(proj_name),normalize(promoter_name),normalize(last_modified),normalize(view_link),'NA',normalize(response.url))
                self.cur.execute(mainpage_metaquery,main_values)
                self.con.commit()
                yield FormRequest(view_link, dont_filter = True, callback = self.parse_meta,meta={'sk':proj_name})
 

    def parse_meta(self,response):
        sel = Selector(response)
        program_sk = response.meta['sk']
        information_type = normalize(extract_data(sel, '//div[@class="form-group"]//div//label[contains(text(),"Information Type")]//..//following-sibling::div[1]/text()'))
        organization_name = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyName")]]/following-sibling::div[1]//text()'))
        organization_type = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_OrgType")]]/following-sibling::div[1]//text()'))
        desc_other_type_org = normalize(extract_data(sel, '//div[label[contains(text(),"Description For Other Type Organization ")]]/following-sibling::div[1]/text()'))
        past_exp = normalize(extract_data(sel, '//div[@class="form-group"]/div[contains(text(),"Do you have any Past Experience ?")]/following-sibling::div[1]/text()'))
        org_add_block_number = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyHouseNo")]]/following-sibling::div[1]//text()'))
        org_add_build_name = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyBuilding")]]/following-sibling::div[1]//text()'))
        org_add_street_name = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyStreet")]]/following-sibling::div[1]//text()'))
        org_add_company_locality = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyLocality")]]/following-sibling::div[1]//text()'))
        org_add_company_landmark = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyLandmark")]]/following-sibling::div[1]//text()'))
        org_add_company_state = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyState")]]/following-sibling::div[1]//text()'))
        org_add_division = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyDivisionValue")]]/following-sibling::div[1]//text()'))
        org_add_district = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyDistrictValue")]]/following-sibling::div[1]//text()'))
        org_add_taluka = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyTalukaValue")]]/following-sibling::div[1]//text()'))
        org_add_village = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyVillageValue")]]/following-sibling::div[1]//text()'))
        org_add_pincode = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyPinCode")]]/following-sibling::div[1]//text()'))
        org_contact_office_number = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_CompanyOfficeNo")]]/following-sibling::div[1]//text()'))
        org_contact_website_url = normalize(extract_data(sel, '//div[@class="form-group"]//div[label[contains(@for,"PersonalInfoModel_WebsiteURL")]]/following-sibling::div[1]//text()'))
        fsi_built_area_proposed = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Built-up-Area as per Proposed FSI")]]/following-sibling::div[1]/text()'))
        fsi_built_area_approved = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Built-up-Area as per Approved FSI (In sqmts)")]]/following-sibling::div[1]/text()'))
        fsi_totalfsi = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  TotalFSI")]]/following-sibling::div[1]/text()'))
        doc_names = []
        documents = normalize("<>".join(sel.xpath('//div[@id="DivDocument"]//table//tr//td//span//text()').extract()))
        aux_info=''
        if program_sk:
            values = (normalize(program_sk),information_type,organization_name,organization_type,desc_other_type_org,past_exp,org_add_block_number,org_add_build_name,org_add_street_name,org_add_company_locality,org_add_company_landmark,org_add_company_state,org_add_division,org_add_district,org_add_taluka,org_add_village,org_add_pincode,org_contact_office_number,org_contact_website_url,fsi_built_area_proposed,fsi_built_area_approved,fsi_totalfsi,documents,normalize(response.url),aux_info)
            self.cur.execute(mahameta_query,values)
            self.con.commit()
        org_project_name = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Project Name")]]/following-sibling::div[1]/text()'))
        org_project_status = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Project Status")]]/following-sibling::div[1]/text()'))
        org_project_prop_completion = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Proposed Date of Completion")]]/following-sibling::div[1]/text()'))
        org_project_revised_prop_completion = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Revised Proposed Date of Completion")]]/following-sibling::div[1]/text()'))
        org_project_liti_project = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Litigations related to the project ?")]]/following-sibling::div[1]/text()'))
        org_project_type = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Project Type")]]/following-sibling::div[1]/text()'))
        org_project_any_promoter = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Are there any Promoter(Land Owner/ Investor)")]]/following-sibling::div[1]/text()'))
        org_project_plot_sur = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Plot Bearing No / CTS no  / Survey Number/Final Plot no.")]]/following-sibling::div[1]/text()'))
        org_project_boundaries_east = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Boundaries East")]]/following-sibling::div[1]/text()'))
        org_project_boundaries_west = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Boundaries West")]]/following-sibling::div[1]/text()'))
        org_project_boundaries_north = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Boundaries North")]]/following-sibling::div[1]/text()'))
        org_project_boundaries_south = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"Boundaries South")]]/following-sibling::div[1]/text()'))
        org_project_state = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  State/UT")]]/following-sibling::div[1]/text()'))
        org_project_division = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text()," Division")]]/following-sibling::div[1]/text()'))
        org_project_district = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  District")]]/following-sibling::div[1]/text()'))
        org_project_taluka = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Taluka")]]/following-sibling::div[1]/text()'))
        org_project_village = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Village")]]/following-sibling::div[1]/text()'))
        org_project_street = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Street")]]/following-sibling::div[1]/text()'))
        org_project_locality = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Locality")]]/following-sibling::div[1]/text()'))
        org_project_pincode = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Pin Code")]]/following-sibling::div[1]/text()'))
        org_project_area = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Area(In sqmts)")]]/following-sibling::div[1]/text()'))
        org_project_total_build = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Total Building Count")]]/following-sibling::div[1]/text()'))
        org_project_sanc_count = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Sanctioned Buildings Count")]]/following-sibling::div[1]/text()'))
        org_project_prop_not_sanct = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Proposed But Not Sanctioned Buildings Count")]]/following-sibling::div[1]/text()'))
        org_project_agg_area = normalize(extract_data(sel, '//div[@class="form-group"]/div[label[contains(text(),"  Aggregate area(In sqmts) of recreational open space")]]/following-sibling::div[1]/text()'))
        aux_info1=''
        if program_sk and org_project_name:
            project_sk = md5(normalize(program_sk)+org_project_name)
            values1 = (normalize(project_sk),normalize(program_sk),org_project_name,org_project_status,org_project_prop_completion,org_project_revised_prop_completion,org_project_liti_project,org_project_type,org_project_any_promoter,org_project_plot_sur,org_project_boundaries_east,org_project_boundaries_west,org_project_boundaries_north,org_project_boundaries_south,org_project_state,org_project_division,org_project_district,org_project_taluka,org_project_village,org_project_street,org_project_locality,org_project_pincode,org_project_area,org_project_total_build,org_project_sanc_count,org_project_prop_not_sanct,org_project_agg_area,normalize(response.url),aux_info1)
            self.cur.execute(projectmaha_metaquery,values1)
            self.con.commit()
        past_exp_nodes = sel.xpath('//div[@id="DivExp"]//table//tr')
        for exp_node in past_exp_nodes :
            proj_name = normalize("".join(exp_node.xpath('./td[@data-name="ProjectName"]//text()').extract()))
            if not proj_name : continue
            type_of_proj = normalize("".join(exp_node.xpath('./td[@data-name="TypeofProject"]//text()').extract()))
            others = normalize("".join(exp_node.xpath('./td[@data-name="PTypeOther"]//text()').extract()))
            land_area = normalize("".join(exp_node.xpath('./td[@data-name="LandArea"]//text()').extract()))
            address = normalize("".join(exp_node.xpath('./td[@data-name="Address"]//text()').extract()))
            cts_num = normalize("".join(exp_node.xpath('./td[@data-name="CTSNo"]//text()').extract()))
            no_of_buildings = normalize("".join(exp_node.xpath('./td[@data-name="BuildPlotCount"]//text()').extract()))
            appartment_count = normalize("".join(exp_node.xpath('./td[@data-name="Apartmentcount"]//text()').extract()))
            original_date = normalize("".join(exp_node.xpath('./td[@data-name="ProjectStartDate"]//text()').extract()))
            actual_date = normalize("".join(exp_node.xpath('./td[@data-name="ProjectEndDate"]//text()').extract()))
            past_exp_sk = md5(normalize(program_sk)+proj_name)
            aux_info2 = ''
            if program_sk and past_exp_sk:
                values2 = (normalize(past_exp_sk),normalize(program_sk),proj_name,type_of_proj,others,land_area,address,cts_num,no_of_buildings,appartment_count,original_date,actual_date,normalize(response.url),aux_info2)
                self.cur.execute(past_exp_metaquery,values2)
                self.con.commit()
        litigation_details = sel.xpath('//div[@id="fldindtxt"]//table//tr')
        for lit_nodes in litigation_details :
            lit_prj_name = normalize("".join(lit_nodes.xpath('./td[1]//text()').extract()))
            if not lit_prj_name : continue
            lit_court_name = normalize("".join(lit_nodes.xpath('./td[2]//text()').extract()))
            lit_case_no = normalize("".join(lit_nodes.xpath('./td[3]//text()').extract()))
            lit_case_type = normalize("".join(lit_nodes.xpath('./td[4]//text()').extract()))
            lit_preventive = normalize("".join(lit_nodes.xpath('./td[5]//text()').extract()))
            lit_petition = normalize("".join(lit_nodes.xpath('./td[6]//text()').extract()))
            lit_othr_petition = normalize("".join(lit_nodes.xpath('./td[7]//text()').extract()))
            year = normalize("".join(lit_nodes.xpath('./td[8]//text()').extract()))
            lit_present_states = normalize("".join(lit_nodes.xpath('./td[9]//text()').extract()))
            lit_documents = normalize("".join(lit_nodes.xpath('./td[10]//text()').extract()))
            lit_prj_sk = md5(normalize(program_sk)+lit_prj_name)
            aux_info7 = ''
            if lit_prj_sk and program_sk:
                values7 = (normalize(lit_prj_sk),normalize(program_sk),lit_prj_name,lit_court_name,lit_case_no,lit_case_type,lit_preventive,lit_petition,lit_othr_petition,year,lit_present_states,lit_documents,normalize(response.url),aux_info7)
                self.cur.execute(litigation_det_metaquery, values7)
                self.con.commit()

        proj_prof_info = sel.xpath('//h2[contains(text(),"Project Professional Information")]//parent::div[@class="x_title"]//following-sibling::table//tr')
        for proj_prof_nodes in proj_prof_info :
            profess_name = normalize("".join(proj_prof_nodes.xpath('./td[1]//text()').extract()))    
            if not profess_name : continue
            certificate_no = normalize("".join(proj_prof_nodes.xpath('./td[2]//text()').extract()))
            prof_typ = normalize("".join(proj_prof_nodes.xpath('./td[3]//text()').extract()))
            proj_prof_sk = md5(normalize(program_sk)+profess_name)
            aux_info6 = ''
            if program_sk and proj_prof_sk:
                values6 = (normalize(proj_prof_sk),normalize(program_sk),profess_name,certificate_no,prof_typ,normalize(response.url),aux_info6)
                self.cur.execute(proj_prof_metaquery, values6)
                self.con.commit()

        compliant_details = sel.xpath('//h2[contains(text(),"Complaint Details")]//parent::div[@class="x_title"]//following-sibling::table//tr')
        for compliant_nodes in compliant_details :
            compliant_no = normalize("".join(compliant_nodes.xpath('./td[1]//text()').extract()))
            if not compliant_no : continue
            compliant_name = normalize("".join(compliant_nodes.xpath('./td[2]//text()').extract()))
            compliant_sk = md5(normalize(program_sk)+compliant_no+compliant_name)
            if compliant_sk and compliant_no:
                values10 = (normalize(compliant_sk),normalize(program_sk),compliant_no,compliant_name,normalize(response.url))
                self.cur.execute(compliant_metaquery, values10)
                self.con.commit()

        promotor_details = sel.xpath('//h2[contains(text(),"Promoter(Land Owner/ Investor) Details")]//parent::div[@class="x_title"]//following-sibling::table//tr')
    
        for pro_node in promotor_details:
            pro_project_name = normalize("".join(pro_node.xpath('./td[1]//text()').extract()))
            if not pro_project_name : continue
            pro_promoter_name = normalize("".join(pro_node.xpath('./td[2]//text()').extract()))
            land_owner_type = normalize("".join(pro_node.xpath('./td[3]//text()').extract())) 
            agreement =  normalize("".join(pro_node.xpath('./td[4]//text()').extract()))
            office_num =  normalize("".join(pro_node.xpath('./td[5]//text()').extract()))
            other_det =  normalize("".join(pro_node.xpath('./td[6]//text()').extract()))
            pro_sk =  md5(normalize(program_sk)+pro_project_name+pro_promoter_name)   
            qry_values = (normalize(pro_sk),normalize(program_sk),pro_project_name,pro_promoter_name,land_owner_type,agreement,str(office_num),other_det,normalize(response.url))
            self.cur.execute(promoter_det_metaquery,qry_values)
            self.con.commit() 
	rows_dict = {}
	building_details = sel.xpath('//div[@class="x_title"]/h2[contains(text(), "Building Details")]/../following-sibling::table[1]/tr')
	tab_data_list, inner_tab_nodes = []*11, []
        for idx, build_detail_node in enumerate(building_details):
		list_ = []
		for i in range(12):
		   _name = normalize("".join(build_detail_node.xpath('./td[%s]/text()'%i).extract()))
                   list_.append(_name)
                if list_[1]:
		   tab_data_list = list_
		check = normalize("".join(build_detail_node.xpath('./td[1]/text()').extract())).strip()
               
                try : empty, sno , building_project_name, build_name, proposed_date_of_completion, no_of_basements, no_of_plinth, no_of_podium, no_of_slab, no_of_slits, no_of_open_parking, no_of_closed_parking = tab_data_list
                except : continue
              
		if not check:
		    inner_nodes = build_detail_node.xpath('./td//table/tr')
		    headers_lst = []
		    for idx, inner_node in enumerate(inner_nodes):
			if idx == 0:
			    val  = inner_node.xpath('./th/text()').extract()
			    val = [normalize(x) for x in val if x]
		            if val: headers_lst = val
                        
                        sr_no = normalize("".join(inner_node.xpath('.//td[1]//text()').extract()))
                        if not sr_no : continue
                        build_apartment_type = normalize("".join(inner_node.xpath('.//td[2]//text()').extract()))
                        build_carpet_area = normalize("".join(inner_node.xpath('.//td[3]//text()').extract()))
                        build_no_of_appartment = normalize("".join(inner_node.xpath('.//td[4]//text()').extract()))
                        no_of_booked_aprtmnt = normalize("".join(inner_node.xpath('.//td[5]//text()').extract()))
                        aux_info8 = ''
                        build_det_apartment_sk = md5(normalize(program_sk)+build_apartment_type+build_carpet_area+str(sr_no)+str(build_name)+proposed_date_of_completion+no_of_basements+no_of_plinth+no_of_booked_aprtmnt+build_no_of_appartment)
                        if 'Apartment Type' in headers_lst :
                            if program_sk and build_det_apartment_sk:
                                values8 = (normalize(build_det_apartment_sk),normalize(program_sk),building_project_name,build_name,proposed_date_of_completion,no_of_basements,no_of_plinth,no_of_podium,no_of_slab,no_of_slits,no_of_open_parking,no_of_closed_parking,build_apartment_type,build_carpet_area,build_no_of_appartment,no_of_booked_aprtmnt,normalize(response.url),aux_info8)
                                self.cur.execute(build_det_apartment_metaquery, values8)
                                self.con.commit()
                        elif 'Tasks / Activity' in headers_lst : 
                                    values9 = (normalize(build_det_apartment_sk),normalize(program_sk),building_project_name,build_name,proposed_date_of_completion,no_of_basements,no_of_plinth,no_of_podium,no_of_slab,no_of_slits,no_of_open_parking,no_of_closed_parking,build_apartment_type,build_carpet_area,normalize(response.url),'')
                                    self.cur.execute(build_det_tasks_metaquery, values9)
                                    self.con.commit()

        dev_work = sel.xpath('//h2[contains(text(),"Development Work")]//parent::div[@class="x_title"]//following-sibling::table//tr')
        for dev_work_node in dev_work :
            amenties = normalize("".join(dev_work_node.xpath('./td[1]//text()').extract()))
            if not amenties : continue
            available = normalize("".join(dev_work_node.xpath('./td[2]//text()').extract()))
            percent = normalize("".join(dev_work_node.xpath('./td[3]//text()').extract()))
            details = normalize("".join(dev_work_node.xpath('./td[4]//text()').extract()))
            dev_work_sk = md5(normalize(program_sk)+amenties+available+percent)
            aux_info5 = ''
            if program_sk and dev_work_sk:
                values5 = (normalize(dev_work_sk),normalize(program_sk),amenties,available,percent,details,normalize(response.url),aux_info5)
                self.cur.execute(dev_work_metaquery,values5)
                self.con.commit()

        proj_details = sel.xpath('//h2[contains(text(),"  Project Details")]//parent::div[@class="x_title"]/following-sibling::div[@class="x_content"]//h2[contains(text(),"Development Work")]//parent::div[@class="x_title"]//preceding-sibling::table//tr')
        for proj_node in proj_details :
            name = normalize("".join(proj_node.xpath('./td[1]//text()').extract()))
            if not name : continue
            proposed = normalize("".join(proj_node.xpath('./td[2]//text()').extract()))
            booked = normalize("".join(proj_node.xpath('./td[3]//text()').extract()))
            work_done = normalize("".join(proj_node.xpath('./td[4]//text()').extract()))
            proj_det_sk = md5(normalize(program_sk)+name+proposed+booked)
            aux_info4 = ''
            if program_sk and proj_det_sk:
                values4 = (normalize(proj_det_sk),normalize(program_sk),name,proposed,booked,work_done,normalize(response.url),aux_info4)
                self.cur.execute(pro_det_metaquery,values4)
                self.con.commit()

        member_info = sel.xpath('//div[@id="fldindtxt78"]//table//tr')
        for member_node in member_info :
            member_name = normalize("".join(member_node.xpath('./td[1]//text()').extract()))
            if not member_name : continue
            designation = normalize("".join(member_node.xpath('./td[2]//text()').extract()))
            aux_info3 = ''
            member_sk = md5(normalize(program_sk)+member_name+designation)
            if program_sk and member_sk:
                values3 = (normalize(member_sk),normalize(program_sk),member_name,designation,normalize(response.url),aux_info3)
                self.cur.execute(member_info_metaquery,values3)
                self.con.commit()

