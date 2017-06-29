from Twitter.twitter_xlsheet import *
from insert_script import *
from flask import Flask, render_template, jsonify
from flask import request
from flask.ext.triangle import Triangle
from Fullcontact.generic_functions import *
from Fullcontact.db_operations import *

app = Flask(__name__)
Triangle(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats_calculator')
def stats():
    return render_template('stats_calculator.html')


@app.route('/information/<media_type>', methods=['POST'])
def information(media_type):
    profile_url = request.form.get('action', '')
    emailid = request.args.get('email_id','')
    lists = ['twitter', 'facebook', 'linkedin']
    for inner in lists:
        if media_type == inner:
             key_name, sk, profile_url,\
             media_type, meta_aux_info = checking(profile_url,
                inner, emailid, media_type)
             Insert().main(key_name, sk, profile_url,
            media_type, meta_aux_info)
            #return render_template('%s.html' % inner)
             if media_type == 'twitter':
                twitter_data = twitter(sk, emailid)
                if twitter_data:
                    return render_template('twitter_data.html', twd = twitter_data)
                else:
                    return jsonify('No data for this profile')

def twitter(sk, emailid):
    cmd = 'python tweet_analyzer.py -n %s -e %s'%(sk, emailid)
    real_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir("%s%s" % (real_path, '/Twitter'))
    os.system(cmd)
    os.chdir(real_path)
    twitter_data = Tixlsfile().main(sk)
    return twitter_data

def checking(profile_url, inner, emailid, media_type):
    meta_aux_info = {'email_address':emailid}
    key_name  = ''
    sk = md5("%s%s"%(normalize(emailid),normalize(profile_url)))
    if media_type == 'twitter':
        key_name = 'twitter_crawl'
        meta_aux_info = meta_aux_info['email_address']
        sk = profile_url.split('/')[-1].strip()
    elif media_type == 'linkedin':
        key_name = 'linkedin_crawl'
        meta_aux_info.update({"linkedin_url":profile_url})
    elif media_type == 'facebook':
        key_name = 'facebook_crawl'
        meta_aux_info.update({"mbasic_url": profile_url.replace('www', 'mbasic')})
    return key_name, sk, profile_url, media_type, meta_aux_info

@app.route('/', methods=['POST'])
def my_form_post():
    email = request.form['email']
    #python fullcontact_script.py -d 'FULLCO' -m 'nakul@aromathai.net' -e '9fe11c7ab65dacbd'
    if email:
        excel_file_name = 'fullcontact_%s.txt'%str(datetime.datetime.now().date())
        real_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir("%s%s" % (real_path, '/Fullcontact'))
        if os.path.isfile(excel_file_name):
            os.system('rm %s'% excel_file_name)
        cmd = "python fullcontact_script.py -d '%s' -m '%s' -e '%s' >> %s"%(DB_NAME, email, '9fe11c7ab65dacbd', excel_file_name)
        os.system(cmd)
        os.chdir(real_path)
        con, cur = get_mysql_connection(DB_HOST, DB_NAME, '')
        recs = fetchmany(cur, query1_full%email)
        name, family_name, websites, age, gender, country, state, city, continent, location, likelihood = ['']*11
        if recs and len(recs[0]) == 11:
            name, family_name, websites, age,\
                gender, country, state, city,\
                continent, location, likelihood = recs[0]
        profile_details_list = [('name',name), ('family_name', family_name),
        ('websites', websites.split('<>')), ('age', age),
        ('gender', gender), ('country', country), ('state', state), ('city', city),
        ('continent', continent), ('location', location), ('likelihood', likelihood)]
        data_dic = {}
        data_dic.update({"enter_email_id":email})
        for pd in profile_details_list:
            data_dic.update({pd[0]:pd[1]})
        all_tables = [("social_profiles", list_variables), ("organizations", variables_organizations), ("richmedia", variables_richmedia)]
        for table in all_tables:
            recs = ()
            if table[0] == "social_profiles":
                execute_query(cur, query2_full%(email, 'twitter', 'linkedin', 'facebook'))
                recs = cur.fetchmany(BATCH_SIZE)
            elif table[0] == "organizations":
                execute_query(cur, query4_full%email)
                recs = cur.fetchmany(BATCH_SIZE)
            else:
                execute_query(cur, query3_full%email)
                recs = cur.fetchmany(BATCH_SIZE)
            final_profiles_list = []
            if recs:
                for record in recs:
                    inner_dic = {}
                    for var_name, var_value in zip(table[1], record):
                        inner_dic.update({var_name:var_value})
                    final_profiles_list.append(inner_dic)
            if final_profiles_list:
                data_dic.update({table[0]:final_profiles_list})
        if data_dic.get('social_profiles',[]):
            for soc in data_dic.get('social_profiles'):
                if 'facebook' in soc.get('type_name').lower():
                    data_dic.update({'facebook_field':soc})
                if 'twitter' in soc.get('type_name').lower():
                    data_dic.update({'twitter_field':soc})
                if 'linkedin' in soc.get('type_name').lower():
                    data_dic.update({'linkedin_field':soc})
        checking = ''
        with file("%s%s" % ("Fullcontact/",excel_file_name)) as f:
            s = f.read()
            if s:
                checking = s
        data_from_ful = ast.literal_eval(json.loads(json.dumps(checking.replace('\n',''))))
        if 'message' in data_from_ful.keys():
            return jsonify(data_from_ful)
        else:
            return render_template('profiles_data.html', data_dic = data_dic)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8545, debug=True)
