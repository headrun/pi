import os

grep_cmd = 'cd /home/veveo/datagen; ls *_MERGE > /home/veveo/headrun/aruna/text'

os.system(grep_cmd)

result = open("text", 'r')

for line in result:
    if 'MERGE' in line:

        source = line.replace(':', '').strip()
        rm_cmd = 'cd /home/veveo/datagen/%s; rm -rf logs_gmrf_wrapper_* logs_crew_merge_*' %source
        os.system(rm_cmd)


