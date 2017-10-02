import smtplib
from linkedin_voyager_functions import *
from linkedin_voyager_items import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Voyagerapi(Voyagerapiitems):

    def __init__(self, name=None, **kwargs):
        super(Voyagerapi, self).__init__(name, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')

    def spider_closed(self, spider):
        close_mysql_connection(self.con, self.cur)

    def update_status(self, sk, crawl_status, where_status):
        delete_query = 'DELETE FROM linkedin_crawl WHERE crawl_status=%s AND sk ="%s"' % (
            crawl_status, sk)
        execute_query(self.cur, delete_query)
        bkup_query = 'select sk from linkedin_crawl where sk = "%s" group by sk  having count(sk)>1' % (
            sk)
        update_query = 'UPDATE linkedin_crawl SET crawl_status=%s, modified_at=NOW() WHERE sk = "%s"' % (
            crawl_status, sk)
        if where_status == 0:
            update_query = 'UPDATE linkedin_crawl SET crawl_status=%s, modified_at=NOW() WHERE sk = "%s" and crawl_status= %s' % (
                crawl_status, sk, where_status)
        else:
            update_query = 'UPDATE linkedin_crawl SET crawl_status=%s, modified_at=NOW() WHERE sk = "%s" and (crawl_status=9 or crawl_status=10)' % (
                crawl_status, sk)
        if update_query:
            try:
                self.cur.execute(update_query)
            except:
                try:
                    recs_ = fetchall(self.cur, bkup_query)
                    if recs_:
                        query2 = 'select max(modified_at) from linkedin_crawl where sk ="%s"' % sk
                        recs_1 = fetchall(self.cur, query2)
                        del_qu = "delete from linkedin_crawl where sk ='%s' and modified_at not like '%s'" % (
                            sk, str(recs_1[0][0]))
                        execute_query(self.cur, del_qu)
                        self.cur.execute(update_query)

                except:
                    error = traceback.format_exc()
                    self.alert_mail(sk, crawl_status, error)

    def checking_for_limit(self, account_mail, logind_date, sk_login_self, command_prxy):
	import pdb;pdb.set_trace()
        count_from_ = fetchall(self.cur, "select count from linkedin_loginlimit where sk = '%s' and login_date='%s' and proxy_ip='%s'" %
                               (sk_login_self, logind_date, command_prxy))
        if count_from_ and count_from_[0][0] < 30000:
            return count_from_[0][0], sk_login_self
        else:
            count_from_1 = fetchall(
                self.cur, "select sk, count from linkedin_loginlimit where count < 30000 and login_date='%s' and sk != '%s' order by rand() limit 1" % (logind_date, sk_login_self))
            if count_from_1:
                sk_login, countc = count_from_1[0]
                return countc, sk_login
            else:
                self.alert_mail(
                    'updations', 0, 'all accounts are exceeded with todays limit')
                return '', ''

    def alert_mail(self, sk, crawl_status, error):
        sender_mail = 'facebookdummyfb01@gmail.com'
        # receivers_mail_list = ['kiranmayi@headrun.net','aravind@headrun.com',
        # 'anushab@headrun.net']
        receivers_mail_list = ['kiranmayi@headrun.net']
        sender, receivers = sender_mail, ','.join(receivers_mail_list)
        msg = MIMEMultipart('alternative')
        if sk == 'updations':
            msg['Subject'] = 'Alert mail for accounts login limit'
            mas = '<h3> All accounts are exceeded with todays limit</h3>'
        else:

            msg['Subject'] = 'Testing: bug raises while crawl status updation for linkedin'
            mas = '<html><head><link href="http://getbootstrap.com/dist/css/bootstrap.css" rel="stylesheet"></head>'
            mas += '<table border="1" style="border-collapse:collapse;" cellpadding="3px" cellspacing="3px"><tr><th>TableName</th><th>crawl_status</th><th>sk</th><th>error</th></tr>'
            mas += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></br>' % (
                'linkedin_crawl', str(crawl_status), sk, error)
            mas += '</table></html>'
        msg['From'] = sender
        msg['To'] = receivers
        tem = MIMEText(''.join(mas), 'html')
        msg.attach(tem)
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()
        s.starttls()
        s.login(sender_mail, '01123123')
        s.sendmail(sender, receivers_mail_list, msg.as_string())
        s.quit()

    def type_of_item(self, data_elements, url_type, main_member_id, sk):
        item = ''
        if url_type == 'groups':
            item = self.get_groups_data(data_elements, url_type, sk)
        elif url_type == 'schools':
            item = self.get_groups_data(data_elements, url_type, sk)
        elif url_type == 'companies':
            item = self.get_groups_data(data_elements, url_type, sk)
        elif url_type == 'channel':
            item = self.get_channel_data(data_elements, url_type, sk)
        elif url_type == 'influencers':
            item = self.get_influencers_data(data_elements, url_type, sk)
        elif url_type == 'educations':
            item = self.get_educations_data(data_elements, url_type, sk)
        elif url_type == 'certifications':
            item = self.get_certifications_data(data_elements, url_type, sk)
        elif url_type == 'courses':
            item = self.get_courses_data(data_elements, url_type, sk)
        elif url_type == 'publications':
            item = self.get_public_data(data_elements, url_type, sk)
        elif url_type == 'honors':
            item = self.get_honors_data(data_elements, url_type, sk)
        elif url_type == 'organizations':
            item = self.get_orgs_data(data_elements, url_type, sk)
        elif url_type == 'posts':
            item = self.get_posts_data(
                data_elements, url_type, main_member_id, sk)
        elif url_type == 'volunteer':
            item = self.get_volunteers_data(data_elements, url_type, sk)
        elif url_type == 'experiences':
            item = self.get_experiences_data(data_elements, url_type, sk)
        elif url_type == 'skills':
            item = self.get_skills_data(data_elements, url_type, sk)
        elif url_type == 'received':
            item = self.get_received_data(data_elements, url_type, sk)
        elif url_type == 'given':
            item = self.get_given_data(data_elements, url_type, sk)
        elif url_type == 'projects':
            item = self.get_projects_data(data_elements, url_type, sk)
        elif url_type == 'testscores':
            item = self.get_testscores_data(data_elements, url_type, sk)
        else:
            item = ''
        return item

    def get_groups_data(self, data_elements, url_type, sk):
        entity = data_elements.get('entity', {}).get(
            'com.linkedin.voyager.entities.shared.MiniGroup', {})
        if url_type == 'schools':
            entity = data_elements.get('entity', {}).get(
                'com.linkedin.voyager.entities.shared.MiniSchool', {})
        if url_type == 'companies':
            entity = data_elements.get('entity', {}).get(
                'com.linkedin.voyager.entities.shared.MiniCompany', {})
        group_description = entity.get('groupDescription', '')
        group_link = entity.get('objectUrn', '')
        group_link = self.get_digit(group_link)
        group_id = group_link
        if group_link:
            if url_type == 'schools':
                group_link = "https://www.linkedin.com/edu/school?id=%s" % (
                    group_link)
            elif url_type == 'companies':
                group_link = "https://www.linkedin.com/company-beta/%s/" % (
                    group_link)
            else:
                group_link = "https://www.linkedin.com/groups?gid=%s&goback=" % (
                    group_link)
        group_name = entity.get('groupName', '')
        if url_type == 'schools':
            group_name = entity.get('schoolName', '')
        if url_type == 'companies':
            group_name = entity.get('name', '')

        group_logo = entity.get('logo', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if group_logo:
            group_logo = "%s%s" % ("https://media.licdn.com/media", group_logo)

        grp_no_members = data_elements.get(
            'followingInfo', {}).get('followerCount', '')
        if url_type == 'groups':
            item = self.get_groups_item(
                sk, group_description, group_link, group_name, str(grp_no_members), group_id, group_logo)
            return item
        if url_type == 'schools':
            item = self.get_schools_item(
                sk, str(grp_no_members), group_name, group_link, group_logo)
            return item
        if url_type == 'companies':
            item = self.get_companies_item(
                sk, group_name, group_logo, group_link, str(grp_no_members))
            return item

    def get_certifications_data(self, data_elements, url_type, sk):
        certification_id = data_elements.get('entityUrn', '')
        certification_id = self.get_digit(certification_id)
        time_period = data_elements.get('timePeriod', '')
        start_year, start_month = [''] * 2
        if time_period:
            end_year, end_month, start_year, start_month = self.get_start_end_date(
                time_period)
        date_cer = ('%s%s%s' %
                    (start_year, '-', start_month)).strip('-').strip()
        certification_title = data_elements.get('name', '')
        certification_company_logo = data_elements.get('company', {}).get('logo', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if certification_company_logo:
            certification_company_logo = "%s%s" % (
                "https://media.licdn.com/media", certification_company_logo)

        certification_company_name = data_elements.get('authority', '')
        certifications_licence = data_elements.get('licenseNumber', '')
        item = self.get_certifications_item(
            sk, certification_id, certification_title, date_cer,
            certification_company_name, certification_company_logo, certifications_licence)
        return item

    def get_testscores_data(self, data_elements, url_type, sk):
        test_score_name = data_elements.get('name', '')
        test_score = data_elements.get('score', '')
        test_score_description = data_elements.get('description', '')
        test_score_date = data_elements.get('date', {})
        test_score_day, test_score_month, test_score_year = [''] * 3
        if test_score_date:
            test_score_day = test_score_date.get('day', '')
            test_score_month = test_score_date.get('month', '')
            test_score_year = test_score_date.get('year', '')
        item = self.get_testscores_item(
            sk, test_score_name, test_score, test_score_description, test_score_day, test_score_month, test_score_year)
        return item

    def get_educations_data(self, data_elements, url_type, sk):
        time_period = data_elements.get('timePeriod', '')
        start_year, start_month, end_year, end_month = [''] * 4
        if time_period:
            end_year, end_month, start_year, start_month = self.get_start_end_date(
                time_period)
        edu_degree = data_elements.get('degreeName', '')
        edu_field_of_study = data_elements.get('fieldOfStudy', '')
        edu_school_name = data_elements.get('schoolName', '')
        school_logo = data_elements.get('school', {}).get('logo', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if school_logo:
            school_logo = "%s%s" % (
                "https://media.licdn.com/media", school_logo)
        edu_activities = data_elements.get('activities', '')
        edu_grade = data_elements.get('grade', '')
        edu_school_id = data_elements.get('schoolUrn', '')
        edu_school_id = self.get_digit(edu_school_id)
        education_id = data_elements.get('entityUrn', '')
        education_id = self.get_digit(education_id)
        item = self.get_educations_item(
            sk, start_year, start_month, '', end_year, '', end_month, edu_degree,
            edu_field_of_study, edu_school_name, school_logo, edu_grade, edu_activities, education_id, edu_school_id)
        return item

    def get_start_end_date(self, data):
        start_date = data.get('startDate', {})
        end_date = data.get('endDate', {})
        start_year = start_date.get('year', '')
        start_month = start_date.get('month', '')
        end_year = end_date.get('year', '')
        end_month = end_date.get('month', '')
        return str(end_year), str(end_month), str(start_year), str(start_month)

    def get_skills_data(self, data_elements, url_type, sk):
        skill_part = data_elements.get('skill', {})
        skill_name = skill_part.get('name', '')
        skill_entity_urn = skill_part.get('entityUrn', '')
        skill_endorsement_count = str(
            data_elements.get('endorsementCount', ''))
        public_topic_skill_url, member_topic_skill_url = [''] * 2
        if '..' not in skill_name and skill_name:
            skill_url_part = skill_name.lower().replace(' ', '-')
            public_topic_skill_url = "https://www.linkedin.com/topic/%s?trk=pprofile_topic" % skill_url_part
            member_topic_skill_url = "https://www.linkedin.com/topic/%s?trk=mprofile_topic" % skill_url_part
        item = self.get_skills_item(
            sk, skill_name, skill_endorsement_count, public_topic_skill_url, member_topic_skill_url)
        return item

    def get_volunteers_data(self,  data_elements, url_type, sk):
        volunteer_role = data_elements.get('role', '')
        volunteer_cause = data_elements.get('cause', '')
        organization_name = data_elements.get('companyName', '')
        organization_logo = data_elements.get('company', {}).get('miniCompany', {}).get(
            'logo', {}).get('com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if organization_logo:
            organization_logo = "%s%s" % (
                "https://media.licdn.com/media", organization_logo)
        description = data_elements.get('description', '')
        time_period = data_elements.get('timePeriod')
        organization_id = data_elements.get('companyUrn', '')
        organization_id = self.get_digit(organization_id)
        start_year, start_month, end_year, end_month = [''] * 4
        if time_period:
            end_year, end_month, start_year, start_month = self.get_start_end_date(
                time_period)

        item = self.get_volunteers_item(
            sk, '', description, volunteer_cause, organization_name, volunteer_role,
            organization_logo, str(start_year), str(start_month), '', str(end_month), str(end_year), organization_id)
        return item

    def get_given_data(self, data_elements, url_type, sk):
        summary = data_elements.get('recommendationText', '')
        recommendation_id = data_elements.get('entityUrn', '')
        if recommendation_id:
            recommendation_id = self.get_digit(recommendation_id)
        recommendee = data_elements.get('recommendee', '')
        recommender = data_elements.get('recommender', '')
        recommender_name = recommender.get('firstName', '')
        recommendee_name = recommendee.get('firstName', '')
        recommendee_lastname = recommendee.get('lastName', '')
        recommendee_name_full = "%s%s%s" % (
            recommendee_name, ' ', recommendee_lastname)
        profile_url = recommendee.get('publicIdentifier', '')
        profile_image = recommendee.get('picture', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if profile_image:
            profile_image = "%s%s" % (
                "https://media.licdn.com/media", profile_image)

        if profile_url:
            profile_url = "https://www.linkedin.com/in/%s/" % (profile_url)
        profile_member_id = recommendee.get('objectUrn', '')
        if profile_member_id:
            profile_member_id = self.get_digit(profile_member_id)

        created = data_elements.get('created', '')
        if created:
            created = str(
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(created) / 1000)))
        relation_ship = data_elements.get('relationship', '').lower().replace('_', ' ').replace(
            'recommender', recommender_name).replace('recommendee', recommendee_name)
        date_and_relationship = ''
        try:
            date_and_relationship = ', '.join(
                [str(created), str(relation_ship)]).strip(', ').strip()
        except:
            date_and_relationship = ', '.join(
                [str(created), str(relation_ship.encode('utf8'))])
        item = self.get_given_item(
            sk, recommendee_lastname, recommendee_name_full, summary, '',
            recommendation_id, date_and_relationship, profile_image, profile_member_id, profile_url, created)
        return item

    def get_projects_data(self, data_elements, url_type, sk):
        project_description = data_elements.get('description', '')
        time_period = data_elements.get('timePeriod', {})
        end_year, end_month, start_year, start_month = [''] * 4
        if time_period:
            end_year, end_month, start_year, start_month = self.get_start_end_date(
                time_period)
        start_date = '-'.join([start_year, start_month]).strip().strip('-')
        end_date = '-'.join([end_year, end_month]).strip().strip('-')
        project_url = data_elements.get('url', '')
        project_title = data_elements.get('title', '')
        project_members_count = data_elements.get('memebers', [])
        project_members_names = ''
        if project_members_count:
            project_members_count = str(len(project_members_count) - 1)
            if project_members_count != 0:
                project_members_names = '<>'.join(["%s%s%s" % (member.get('member', {}).get('firstName', ''), ' ', member.get(
                    'member', {}).get('lastName', '')) for member in data_elements.get('members', [])]).strip('<>').strip()
        else:
            project_members_count = ''
        item = self.get_projects_item(sk, project_title, project_url, project_description, str(
            project_members_count), start_date, end_date, project_members_names)
        return item

    def get_digit(self, value):
        values = textify(re.findall(',(\d+)', value))
        if not values:
            values = textify(re.findall('\d+', value))
        return values

    def get_posts_data(self, data_elements, url_type, main_member_id, sk):
        post_url = data_elements.get('permaLink', '')
        post_image = data_elements.get('image', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if post_image:
            post_image = "%s%s" % ("https://media.licdn.com/media", post_image)
        post_title = data_elements.get('title', '')
        post_author_id = main_member_id
        posted_date = data_elements.get('postedDate', {})
        posted_year = posted_date.get('year', '')
        posted_month = posted_date.get('month', '')
        posted_day = posted_date.get('day', '')
        posted_date = ("%s%s%s%s%s" %
                       (posted_year, '-', posted_month, '-', posted_day)).strip().strip('-')
        post_article_id = data_elements.get('entityUrn', '')
        post_article_id = self.get_digit(post_article_id)
        item = self.get_posts_item(
            sk, post_url, post_image, post_title, post_author_id, '', posted_date, post_article_id)
        return item

    def get_received_data(self, data_elements, url_type, sk):
        summary = data_elements.get('recommendationText', '')
        recommender = data_elements.get('recommender', {})
        recommendee_name = data_elements.get(
            'recommendee', {}).get('firstName', {})
        profile_identifier = recommender.get('publicIdentifier', '')
        if profile_identifier:
            profile_identifier = "https://www.linkedin.com/in/%s/" % (
                profile_identifier)
        headline = recommender.get('occupation', '')
        recommender_name = recommender.get('firstName', '')
        relation_ship = data_elements.get('relationship', '').lower().replace('_', ' ').replace(
            'recommender', recommender_name).replace('recommendee', recommendee_name)
        created = data_elements.get('created', '')
        if created:
            created = str(
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(created) / 1000)))
        date_and_relationship = ', '.join(
            [created, relation_ship]).strip(', ').strip()
        first_name = recommender.get('firstName', '')
        last_name = recommender.get('lastName', '')
        name = ("%s%s%s" % (first_name, ' ', last_name)).strip()
        object_urn_member_id = recommender.get('objectUrn', '')
        ent_id = data_elements.get('entityUrn', '')
        if object_urn_member_id:
            object_urn_member_id = self.get_digit(object_urn_member_id)
        if ent_id:
            ent_id = self.get_digit(ent_id)
        profile_image = recommender.get('picture', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if profile_image:
            profile_image = "%s%s" % (
                "https://media.licdn.com/media", profile_image)
        item = self.get_received_item(
            sk, '', ent_id, object_urn_member_id, name,  summary,
            profile_image, profile_identifier, headline, date_and_relationship, created, '')
        return item

    def get_experiences_data(self, data_elements, url_type, sk):
        exp_location = data_elements.get('locationName', '')
        exp_company_name = data_elements.get('companyName', '')
        exp_company_beta = data_elements.get('companyUrn', '')
        exp_entity_urn = data_elements.get('entityUrn', '')
        exp_company_url = ''
        if exp_company_beta:
            exp_company_beta = textify(re.findall('\d+', exp_company_beta))
            exp_company_url = "https://www.linkedin.com/company-beta/%s/" % exp_company_beta
        if exp_entity_urn:
            exp_entity_urn = self.get_digit(exp_entity_urn)
        exp_title = data_elements.get('title', '')
        time_period = data_elements.get('timePeriod')
        end_year, end_month, start_year, start_month = [''] * 4
        if time_period:
            end_year, end_month, start_year, start_month = self.get_start_end_date(
                time_period)
        start_date = '-'.join([start_year, start_month]).strip('-').strip()
        end_date = '-'.join([end_year, end_month]).strip('-').strip()
        exp_company_logo = data_elements.get('company', {}).get('miniCompany', {}).get(
            'logo', {}).get('com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if exp_company_logo:
            exp_company_logo = "%s%s" % (
                "https://media.licdn.com/media", exp_company_logo)

        exp_company_id = str(exp_company_beta)
        exp_position_id = exp_entity_urn
        exp_summary = data_elements.get('description', '')
        item = self.get_experiences_item(
            sk, exp_location, exp_position_id, exp_company_id, start_date,
            exp_summary, exp_company_name, exp_company_url, exp_title, end_date, exp_company_logo, '')
        return item

    def get_orgs_data(self, data_elements, url_type, sk):
        description = data_elements.get('description', '')
        occupation_name = data_elements.get('occupation', '')
        time_period = data_elements.get('timePeriod')
        start_year, start_month, end_year, end_month = [''] * 4
        if time_period:
            end_year, end_month, start_year, start_month = self.get_start_end_date(
                time_period)
        start_date = ("%s%s%s" %
                      (start_year, '-', start_month)).strip().strip('-')
        end_date = ("%s%s%s" % (end_year, '-', end_month)).strip().strip('-')
        postion = data_elements.get('position', '')
        name = data_elements.get('name', '')
        item = self.get_orgs_item(
            sk, name, postion,  start_date, description, end_date, '')
        return item

    def get_public_data(self, data_elements, url_type, sk):
        publication_title = data_elements.get('name', '')
        publication_url = data_elements.get('url', '')
        publisher_name = data_elements.get('publisher', '')
        pulication_description = data_elements.get('description', '')
        publication_date = data_elements.get('date', {})
        publication_day = str(publication_date.get('day', ''))
        publication_month = str(publication_date.get('month', ''))
        publication_year = str(publication_date.get('year', ''))
        if publication_date:
            publication_date = '-'.join(
                [publication_year, publication_month, publication_day])
        else:
            publication_date = ''
        item = self.get_public_item(
            sk, publication_title, publisher_name, pulication_description, publication_url, publication_date)
        return item

    def get_honors_data(self, data_elements, url_type, sk):
        honor_summary = data_elements.get('description', '')
        honor_title = data_elements.get('title', '')
        honor_issuer = data_elements.get('issuer', '')
        iss_date = data_elements.get('issueDate', {})
        iss_month = iss_date.get('month', '')
        iss_year = iss_date.get('year', '')
        iss_day = iss_date.get('day', '')
        hon_id = data_elements.get('entityUrn', '')
        hon_id = self.get_digit(hon_id)
        if iss_month:
            iss_month = calendar.month_name[iss_month]
        honor_on = ("%s%s%s%s%s" %
                    (iss_day, ' ', iss_month, ' ', iss_year)).strip()
        item = self.get_honors_item(
            sk, honor_title, honor_issuer, honor_on, honor_summary, hon_id)
        return item

    def get_courses_data(self, data_elements, url_type, sk):
        course_name = data_elements.get('name', '')
        course_number = data_elements.get('number', '')
        link_course_ = Linkedincourse()
        link_course_['sk'] = md5(
            "%s%s%s" % (sk, course_name, str(course_number)))
        link_course_['profile_sk'] = normalize(sk)
        link_course_['course_name'] = normalize(course_name)
        link_course_['course_number'] = normalize(course_number)
        if course_name or course_number:
            return link_course_
        else:
            return ''

    def get_channel_data(self, data_elements, url_type, sk):
        entity = data_elements.get('entity', {}).get(
            'com.linkedin.voyager.growth.interests.Channel', {})
        channel_followers = data_elements.get(
            'followingInfo', {}).get('followerCount', '')
        channel_title = entity.get('name', '')
        channel_link = entity.get('id', '')
        if channel_link:
            channel_link = "https://www.linkedin.com/channels/%s?trk=prof-following-chan-icon" % (
                channel_link)
        channel_image = entity.get('logo', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if channel_image:
            channel_image = "%s%s" % (
                "https://media.licdn.com/media", channel_image)
        item = self.get_channel_item(
            sk, str(channel_followers), channel_title, channel_link, channel_image)
        return item

    def get_influencers_data(self, data_elements, url_type, sk):
        entity = data_elements.get('entity', {}).get(
            'com.linkedin.voyager.identity.shared.MiniProfile', {})
        inflencer_first_name = entity.get('firstName', '')
        influencer_last_name = entity.get('lastName', '')
        influencer_name = "%s%s%s" % (
            inflencer_first_name, ' ', influencer_last_name)
        influencer_image = entity.get('picture', {}).get(
            'com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
        if influencer_image:
            influencer_image = "%s%s" % (
                "https://media.licdn.com/media", influencer_image)

        influencer_profile_url = entity.get('publicIdentifier', '')
        if influencer_profile_url:
            influencer_profile_url = "https://www.linkedin.com/in/%s/" % (
                influencer_profile_url)
        influencer_headline = entity.get('occupation', '')
        influencer_no_of_members = data_elements.get(
            'followingInfo', {}).get('followerCount', '')
        item = self.get_influencers_item(
            sk, influencer_name, influencer_profile_url, influencer_headline,
            inflencer_first_name, influencer_last_name, influencer_image, str(influencer_no_of_members))
        return item
