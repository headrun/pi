#import xlwt
import csv
import MySQLdb
import json
import datetime
import sys
sys.path.append('/root/pi_automation/table_schemas')
from generic_functions import *

class Denormxlsfile(object):

    def is_path_file_name(self, excel_file_name):
        #if os.path.isfile(excel_file_name):
         #   os.system('rm %s' % excel_file_name)
        oupf = open(excel_file_name, 'ab+')
        todays_excel_file = csv.writer(oupf)
        return todays_excel_file

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = REQ_DB_NAME , \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
	self.cur = self.con.cursor()
        headers_params = ['Sr No','Name','Source','Source URL',	'Work Experience','','','','','','','','Post graduation','','','Graduation','','','Schooling','','','Any other degree','Personal Details','','','','Interests/ Followings','','Social Media Presence','','','','','','','']							
	self.excel_file_name = 'facebook_linkedin_twitter_data_on_%s.csv'%str(datetime.datetime.now().date())
	oupf = open(self.excel_file_name, 'ab+')
        todays_excel_file = csv.writer(oupf)
        self.todays_excel_file = todays_excel_file
        headers5 = ['','','','','Present Org','Designation','Location','Duration','Past Org','Designation','Location','Duration','Degree','Name of Institution','Year of passing','Degree','Name of Institution','Year of passing','Degree','Name of Institution','Year of passing','Gender','Date of birth','Marital status','Hometown','1','2','Facebook','Linkedin','Twitter','Instagram','Google+','Youtube','Naukri','Any other news URL']
	#self.todays_excel_file.writerow(headers_params)
        #self.todays_excel_file.writerow(headers5)
        self.main()    

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',').replace('\\','')
        if '<>' in text:
            text = set(text.split('<>'))
            text = '<>'.join(text)
        return text

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def main(self):
	selectall_params_ =  'select *  from pi_automation where date(Lnkd_modified_at)>="2018-05-08"'
	self.cur.execute(selectall_params_)
	records = self.cur.fetchall()
	for record in records:
		    pi_id,sk,s_no,pm_id,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,Twt_aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day, name1, profile_id1, aux_info1, aux_info_read_followers,aux_info_books_likes,aux_info_read_books,aux_info_movie_watched,aux_info_movie_likes,aux_info_tvshow_watched, aux_info_tvshow_likes, aux_info_inspirational_people, aux_info_sports, aux_info_family, aux_info_education, aux_info_work, aux_info_clothing, aux_info_friends, aux_info_atheletes, aux_info_teams, aux_info_book, aux_info_music, aux_info_games, aux_info_websites, aux_info_restaurants, aux_info_activities, aux_info_interests, aux_info_tvshows, aux_info_movies, aux_info_life_events,aux_info_quotes,aux_info_about,aux_info_lived_places,aux_info_others, profile_url1,Lnkd_original_url, Lnkd_status_of_url, Lnkd_data_available_flag, Lnkd_profile_url, Lnkd_name, Lnkd_first_name, Lnkd_last_name, Lnkd_headline, Lnkd_no_of_followers, Lnkd_summary, Lnkd_number_of_connections, Lnkd_industry, Lnkd_location, Lnkd_Accomplishments_languages, Lnkd_emails, Lnkd_websites, Lnkd_addresses, Lnkd_message_handles, Lnkd_phone_numbers, Lnkd_twitter_accounts, Lnkd_profile_image, Lnkd_interests, Lnkd_linkedin_certifications, Lnkd_linkedin_following_channels, Lnkd_linkedin_following_companies, Lnkd_linkedin_following_influencers, Lnkd_linkedin_following_schools, Lnkd_linkedin_given_recommendations, Lnkd_linkedin_groups, Lnkd_Accomplishments_projects, Lnkd_linkedin_received_recommendations, Lnkd_linkedin_skills, Lnkd_linkedin_volunteer_experiences, Lnkd_edu_start_year1, Lnkd_edu_start_month1, Lnkd_edu_start_date1, Lnkd_edu_end_year1, Lnkd_edu_end_date1, Lnkd_edu_end_month1, Lnkd_edu_degree1, Lnkd_edu_field_of_study1, Lnkd_edu_school_name1, Lnkd_school_logo1, Lnkd_edu_start_year2, Lnkd_edu_start_month2, Lnkd_edu_start_date2, Lnkd_edu_end_year2, Lnkd_edu_end_date2, Lnkd_edu_end_month2, Lnkd_edu_degree2, Lnkd_edu_field_of_study2, Lnkd_edu_school_name2, Lnkd_school_logo2, Lnkd_edu_start_year3, Lnkd_edu_start_month3, Lnkd_edu_start_date3, Lnkd_edu_end_year3, Lnkd_edu_end_date3, Lnkd_edu_end_month3, Lnkd_edu_degree3, Lnkd_edu_field_of_study3, Lnkd_edu_school_name3, Lnkd_school_logo3, Lnkd_edu_start_year4, Lnkd_edu_start_month4, Lnkd_edu_start_date4, Lnkd_edu_end_year4, Lnkd_edu_end_date4, Lnkd_edu_end_month4, Lnkd_edu_degree4, Lnkd_edu_field_of_study4, Lnkd_edu_school_name4, Lnkd_school_logo4, Lnkd_edu_start_year5, Lnkd_edu_start_month5, Lnkd_edu_start_date5, Lnkd_edu_end_year5, Lnkd_edu_end_date5, Lnkd_edu_end_month5, Lnkd_edu_degree5, Lnkd_edu_field_of_study5, Lnkd_edu_school_name5, Lnkd_school_logo5, Lnkd_edu_start_year6, Lnkd_edu_start_month6, Lnkd_edu_start_date6, Lnkd_edu_end_year6, Lnkd_edu_end_date6, Lnkd_edu_end_month6, Lnkd_edu_degree6, Lnkd_edu_field_of_study6, Lnkd_edu_school_name6, Lnkd_school_logo6, Lnkd_edu_start_year7, Lnkd_edu_start_month7, Lnkd_edu_start_date7, Lnkd_edu_end_year7, Lnkd_edu_end_date7, Lnkd_edu_end_month7, Lnkd_edu_degree7, Lnkd_edu_field_of_study7, Lnkd_edu_school_name7, Lnkd_school_logo7, Lnkd_exp_location1, Lnkd_exp_company_name1, Lnkd_exp_title1, Lnkd_start_date1, Lnkd_end_date1, Lnkd_exp_company_logo1, Lnkd_exp_duration1, Lnkd_exp_summary1, Lnkd_exp_location2, Lnkd_exp_company_name2, Lnkd_exp_title2, Lnkd_start_date2, Lnkd_end_date2, Lnkd_exp_company_logo2, Lnkd_exp_duration2, Lnkd_exp_summary2, Lnkd_exp_location3, Lnkd_exp_company_name3, Lnkd_exp_title3, Lnkd_start_date3, Lnkd_end_date3, Lnkd_exp_company_logo3, Lnkd_exp_duration3, Lnkd_exp_summary3, Lnkd_exp_location4, Lnkd_exp_company_name4, Lnkd_exp_title4, Lnkd_start_date4, Lnkd_end_date4, Lnkd_exp_company_logo4, Lnkd_exp_duration4, Lnkd_exp_summary4, Lnkd_exp_location5, Lnkd_exp_company_name5, Lnkd_exp_title5, Lnkd_start_date5, Lnkd_end_date5, Lnkd_exp_company_logo5, Lnkd_exp_duration5, Lnkd_exp_summary5, Lnkd_exp_location6, Lnkd_exp_company_name6, Lnkd_exp_title6, Lnkd_start_date6, Lnkd_end_date6, Lnkd_exp_company_logo6, Lnkd_exp_duration6, Lnkd_exp_summary6, Lnkd_exp_location7, Lnkd_exp_company_name7, Lnkd_exp_title7, Lnkd_start_date7, Lnkd_end_date7, Lnkd_exp_company_logo7, Lnkd_exp_duration7, Lnkd_exp_summary7, Lnkd_exp_location8, Lnkd_exp_company_name8, Lnkd_exp_title8, Lnkd_start_date8, Lnkd_end_date8, Lnkd_exp_company_logo8, Lnkd_exp_duration8, Lnkd_exp_summary8, Lnkd_exp_location9, Lnkd_exp_company_name9, Lnkd_exp_title9, Lnkd_start_date9, Lnkd_end_date9, Lnkd_exp_company_logo9, Lnkd_exp_duration9, Lnkd_exp_summary9, Lnkd_exp_location10, Lnkd_exp_company_name10, Lnkd_exp_title10, Lnkd_start_date10, Lnkd_end_date10, Lnkd_exp_company_logo10, Lnkd_exp_duration10, Lnkd_exp_summary10,Lnkd_honor_on_Date1, Lnkd_honor_issuer1, Lnkd_honor_Description_Summary1, Lnkd_honor_Occupation1, honor_on2, honor_issuer2, honor_summary2, occupation2, honor_on3, honor_issuer3, honor_summary3, occupation3, honor_on4, honor_issuer4, honor_summary4, occupation4, honor_on5, honor_issuer5, honor_summary5, occupation5, Lnkd_created_at, Lnkd_modified_at,tot_exp = record

                    try : 
                        aux_infof = json.loads(aux_info1.replace('\\','').replace('\r\n',''))
		        aux_info_read_followers = json.loads(aux_info_read_followers.replace('\\',''))
		        aux_info_books_likes = json.loads(aux_info_books_likes.replace('\\',''))
		        aux_info_read_books = json.loads(aux_info_read_books.replace('\\',''))
		        aux_info_movie_watched = json.loads(aux_info_movie_watched.replace('\\',''))
		        aux_info_movie_likes = json.loads(aux_info_movie_likes.replace('\\',''))
		        aux_info_tvshow_watched = json.loads(aux_info_tvshow_watched.replace('\\',''))
		        aux_info_tvshow_likes = json.loads(aux_info_tvshow_likes.replace('\\',''))
		        aux_info_inspirational_people = json.loads(aux_info_inspirational_people.replace('\\',''))
		        aux_info_sports = json.loads(aux_info_sports.replace('\\',''))
		        aux_info_family = json.loads(aux_info_family.replace('\\',''))
		        aux_info_education = json.loads(aux_info_education.replace('\\',''))
		        aux_info_work = json.loads(aux_info_work.replace('\\',''))
		        try:
			    aux_info_clothing = json.loads(aux_info_clothing.replace('\\',''))
		        except:
			    aux_info_clothing = {"fb_clothing":'<>'.join(aux_info_friends.replace(' "',"").replace('{"fb_clothing":','').split('<>'))}

		        try:aux_info_friends = json.loads(aux_info_friends.replace('\\',''))
		        except:
			    aux_info_friends = {"fb_friends":'<>'.join(aux_info_friends.replace(' "',"").replace('{"fb_friends":','').split('<>'))}
		        aux_info_atheletes = json.loads(aux_info_atheletes.replace('\\',''))
		        aux_info_teams = json.loads(aux_info_teams.replace('\\',''))
		        aux_info_book = json.loads(aux_info_book.replace('\\',''))
		        aux_info_music = json.loads(aux_info_music.replace('\\',''))
		        aux_info_games = json.loads(aux_info_games.replace('\\',''))
		        aux_info_websites = json.loads(aux_info_websites.replace('\\',''))
		        aux_info_restaurants = json.loads(aux_info_restaurants.replace('\\',''))
		        aux_info_activities = json.loads(aux_info_activities.replace('\\',''))
		        aux_info_interests = json.loads(aux_info_interests.replace('\\',''))
		        aux_info_tvshows = json.loads(aux_info_tvshows.replace('\\',''))
		        aux_info_movies = json.loads(aux_info_movies.replace('\\',''))
		        try: aux_info_others = json.loads(aux_info_others.replace('\\',''))
		        except:
			    aux_info_others = {"fb_others":'<>'.join(aux_info_others.replace(' "',"").replace('{"fb_others":','').split('<>'))} 
		        response_flag = ''
		        if name1:
			    response_flag = 'Response Available'
		        if not name1: response_flag = 'Response Not Available'
		        aux_info_life_events = json.loads(aux_info_life_events.replace('\\',''))
		        aux_info_quotes = json.loads(aux_info_quotes.replace('\\',''))
		        aux_info_about = json.loads(aux_info_about.replace('\\',''))
		        aux_info_lived_places = json.loads(aux_info_lived_places.replace('\\',''))
		        id1=''
		    except : profile_id1, aux_infof, aux_info1, aux_info_read_followers,aux_info_books_likes,aux_info_read_books,aux_info_movie_watched,aux_info_movie_likes,aux_info_tvshow_watched, aux_info_tvshow_likes, aux_info_inspirational_people, aux_info_sports, aux_info_family, aux_info_education, aux_info_work, aux_info_clothing, aux_info_friends, aux_info_atheletes, aux_info_teams, aux_info_book, aux_info_music, aux_info_games, aux_info_websites, aux_info_restaurants, aux_info_activities, aux_info_interests, aux_info_tvshows, aux_info_movies, aux_info_life_events,aux_info_quotes,aux_info_about,aux_info_lived_places,aux_info_others, profile_url1, response_flag = {},{},{},{},{},{},{},{},{},{}, {}, {}, {}, {}, {}, {}, {}, {}, {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},''

                    values = [1,Lnkd_name,'Linkedin',Lnkd_original_url,Lnkd_exp_company_name1, Lnkd_exp_title1,Lnkd_exp_location1,Lnkd_exp_duration1,Lnkd_exp_company_name2, Lnkd_exp_title2,Lnkd_exp_location2,Lnkd_exp_duration2,Lnkd_edu_degree3,Lnkd_edu_school_name3, Lnkd_edu_end_year3,Lnkd_edu_degree2,Lnkd_edu_school_name2, Lnkd_edu_end_year2,Lnkd_edu_degree1,Lnkd_edu_school_name1, Lnkd_edu_end_year1]
		    final = []
                    
		    for i in values:
                        if type(i)==int:final.append(str(i))
                        elif type(i)==long:final.append(str(i))
                        elif type(i)==dict:i=final.append(i)
                        else : final.append(normalize(i))
                       
		    self.todays_excel_file.writerow(final)
                    
                    """edu_data = aux_info_education.get('fb_education','').split('<>')
                    grad_degree = edu_data[0].split(':-')[-1]
                    grad_name_of_ins = edu_data[0].split('###')[-1]
                    school_name = edu_data[1].split(':-')[0]
                    school_degree = edu_data[1].split(':-')[-1]
                    other_degree = edu_data[2].replace('###',',').replace(':-','')  
                    fb_vals = [2,name1,'Facebook',profile_url1,'',self.restore(aux_infof.get('fb_work','')),'','','','','','','','','','',grad_degree,grad_name_of_ins,'',school_degree,school_name,'',other_degree,self.restore(aux_infof.get('gender','')),self.restore(aux_infof.get('birthday','')),self.restore(aux_infof.get('home_town','')),self.restore(aux_info_life_events.get('fb_life_events','')),self.restore(aux_info_read_followers.get('fb_following','')),self.restore(aux_infof.get('interested_in',''))]
                    #self.todays_excel_file.writerow(fb_vals)"""

def main():
        obj = Denormxlsfile()
        obj.send_xls()

if __name__ == '__main__':
    Denormxlsfile().main()
