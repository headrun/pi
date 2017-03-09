scrapy crawl consumerpatrol_browse -a  search="$1"
scrapy crawl complaintboard_browse -a  search="$1"
scrapy crawl complaintlists_browse -a  search="$1"
scrapy crawl complaintsboard_browse -a  search="$1"
scrapy crawl consumercomplaints_browse -a search="$1"
scrapy crawl consumercourt_browse -a  search="$1"
scrapy crawl consumerdaddy_browse -a  search="$1"
scrapy crawl indiaconsumerforum_browse -a  search="$1"
scrapy crawl mouthshut_browse -a search="$1"

echo eg run command:sh commands.sh "apollo hospitals"


