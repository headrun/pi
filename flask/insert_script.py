from Fullcontact.generic_functions import *
from Fullcontact.db_operations import insert_script_query

class Insert(object):

    def main(self, key_name, sk, profile_url, media_type, meta_aux_info):
        con, cur = get_mysql_connection(DB_HOST, DB_NAME, '')
        if media_type == 'linkedin':
            profile_url = self.linkedin_pub_url(profile_url)
        values  = (key_name, sk, profile_url, media_type, 0, meta_aux_info, meta_aux_info)
        execute_query(cur, insert_script_query%values)


    def linkedin_pub_url(self, linkedin_profilef):
        if 'http:' in linkedin_profilef:
            linkedin_profilef = linkedin_profilef.replace('http:','https:')
        if 'id.www' in linkedin_profilef:
            linkedin_profilef = linkedin_profilef.replace('id.www','https://www')
        if 'www.linkedin.com' and 'https:' not in linkedin_profilef:
            linkedin_profilef = linkedin_profilef.replace('www.','https://www')
        if linkedin_profilef.startswith('linkedin.com'):
            linkedin_profilef = linkedin_profilef.replace('linkedin.com','https://www.linkedin.com')
        if 'https:' not in linkedin_profilef:
            linkedin_profilef = re.sub('(\D+)\.linkedin.com','https://www.linkedin.com',linkedin_profilef) 
        linkedin_profilef = re.sub('https://(.*?).linkedin.com/','https://www.linkedin.com/',linkedin_profilef)
        if linkedin_profilef.endswith('/en') or linkedin_profilef.endswith('/fr'):
            linkedin_profilef = linkedin_profilef[:-3]
        linkedin_profilef = linkedin_profilef.strip('"').strip().strip("'").strip().strip('/').strip()
        if not linkedin_profilef.startswith('https://www.linkedin.com'):
            linkedin_profilef = ''.join(re.findall('.*(https://.*)', linkedin_profilef))
        if '/pub/' in linkedin_profilef:
            cv = ''.join(filter(None,re.split('https://www.linkedin.com/pub/.*?/(.*)',linkedin_profilef))).split('/')[::-1]
            cv[0] = cv[0].zfill(3)
            cv[1] = cv[1].zfill(3)
            if cv[-1] == '0': del cv[-1]
            linkedin_profilef = ( '%s%s%s%s'%('https://www.linkedin.com/in/',''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*',linkedin_profilef)),'-',''.join(cv)))
        return linkedin_profilef


if __name__ == "__main__":
    Insert().main('', '', '', '', '')

