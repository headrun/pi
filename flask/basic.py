from flask import Flask, render_template, jsonify
from flask import request
from linkedin_functions import *
from db_operations import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    email = request.form['email']
    if email:
        excel_file_name = 'fullcontact_%s.txt'%str(datetime.datetime.now().date())
        if os.path.isfile(excel_file_name):
            os.system('rm %s'%excel_file_name)
        cmd = "python fullcontact_script.py -d '%s' -m '%s' -e '%s' >> %s"%(DB_NAME, email, '9fe11c7ab65dacbd', excel_file_name)
        os.system(cmd)
        con, cur = get_mysql_connection(DB_HOST, DB_NAME, '')
        name, family_name, websites, age,\
        gender, country, state, city,\
        continent, location, likelihood = fetchone(cur, query1_full%email)
        profile_details_list = [('name',name), ('family_name', family_name),
        ('websites', websites.split('<>')), ('age', age),
        ('gender', gender), ('country', country), ('state', state), ('city', city),
        ('continent', continent), ('location', location), ('likelihood', likelihood)]
        data_dic = {}
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
        checking_ = ''
        with file(excel_file_name) as f:
            s = f.read()
            if s:
                checking = s
        data_from_ful = ast.literal_eval(json.loads(json.dumps(checking.replace('\n',''))))
        if 'message' in data_from_ful.keys():
            return jsonify(data_from_ful)
        else:
            return render_template('profiles_data.html', data_dic = data_dic)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8545, debug=True)
