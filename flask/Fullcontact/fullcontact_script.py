from db_operations import *
from constants import *
from generic_functions import *

class Fullcontact(object):
    def __init__(self, *args, **kwargs):
        self.search_url = 'https://api.fullcontact.com/v2/person.json?email=%s'
        self.listt = options.mails_list
        self.meta_data = options.meta
        self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME, '')
        if  self.listt:
            self.emails_list = self.listt.split(',')
            self.mails = []
            for br in self.emails_list:
                self.mails.append(br)
            self.main()

    def __del__(self):
        self.con.close()
        self.cur.close()

    def main(self):
        for i in self.mails:
            headers_contact = {}
            meta_data = self.meta_data
            if '<' and '>' in i:
                i = ''.join(re.findall('<(.*?)>', i))
            params = (
              ('email', i),
            )
            headers_contact.update({'X-FullContact-APIKey':meta_data})
            api_response = requests.get(api_url, headers=headers_contact, params=params)
            data = json.loads(api_response.text)
            print data
            message_searched = data.get('message','')
            sk = i
            social_profiles = data.get('socialProfiles')
            if social_profiles:
                self.parse_socialprofiles(sk, social_profiles)
            organizations = data.get('organizations', '')
            if organizations:
                self.parse_organizations(sk, organizations)
            contact_info = data.get('contactInfo', {})
            given_name = contact_info.get('givenName', '')
            full_name = contact_info.get('fullName', '')
            family_name = contact_info.get('familyName', '')
            websites = contact_info.get('websites', '')
            dg = data.get('demographics', {})
            dgl = dg.get('locationDeduced', {})
            city, state, country, continent, location = self.parse_dgl(dgl)
            likelihood = data.get('likelihood', '')
            gender = dg.get('gender', '')
            age = dg.get('age', '')
            if websites:
                websites = '<>'.join([i.get('url') for i in websites])
            values = (sk, full_name, family_name, websites,
            age, gender, state, city, country, location, continent, likelihood, sk)

            try:
                self.cur.execute(profile_details_query, values)
            except: pass
            photos = data.get('photos')
            if photos: self.parse_photos(sk, photos)

    def parse_dgl(self, dgl):
        city = dgl.get('city', {}).get('name', '')
        state = dgl.get('state', {}).get('name', '')
        country  = dgl.get('country', {}).get('name', '')
        continent = dgl.get('continent', {}).get('name', '')
        location = dgl.get('normalizedLocation', '')
        return city, state, country, continent, location

    def parse_photos(self, sk, photos):
        for ph in photos:
                ph_url, ph_type = ph.get('url'), ph.get('typeId')
                values3 = (md5('%s%s'%(ph_url, sk)), sk, ph_type, ph_url, md5('%s%s'%(ph_url, sk)))
                self.cur.execute(profile_richmedia_query, values3)

    def parse_organizations(self, sk, organizations):
        for org in organizations:
            org_name, org_start, org_end, org_title = org.get('name', ''), org.get('startDate', ''), org.get('endDate', ''),org.get('title', '')
            org_name = normalize(org_name.replace( u'\u2013', '-'))
            org_title = normalize(org_title)
            current = org.get('current', '')
            values2 = (md5('%s%s%s%s%s%s'%(org_title, sk,org_name.decode('utf8'), current, org_start, org_end)), sk, org_name, org_title, current, org_start, org_end, md5('%s%s%s%s%s%s'%(org_title, sk,org_name.decode('utf8'), current, org_start, org_end)))
            self.cur.execute(organizations_query, values2)

    def parse_socialprofiles(self, sk, social_profiles):
        for i in social_profiles:
            type_name, user_name, p_url = i.get('typeName'), i.get('username', ''), i.get('url')
            type_id, followers = i.get('typeId'), i.get('followers', '')
            values1 = (md5('%s%s%s'%(type_id, p_url, sk)), sk, user_name, '', type_name, followers, p_url, md5('%s%s%s'%(type_id, p_url, sk)))
            self.cur.execute(social_profiles_query, values1)

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-m', '--mails-list', default='', help = 'mails_list')
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        parser.add_option('-e', '--meta', default='', help = 'meta')
        (options, args) = parser.parse_args()
        Fullcontact(options)



