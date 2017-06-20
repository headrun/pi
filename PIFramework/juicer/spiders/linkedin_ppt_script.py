import re
import optparse
import MySQLdb
from pptx import Presentation
from pptx.util import Inches
from pptx.util import Pt
from pptx.util import Cm
from pptx.dml.color import RGBColor

class Login(object):

    def __init__(self,options):

        self.con = MySQLdb.connect(db='FACEBOOK',
                      user='root',
                      passwd='root',
                      charset="utf8",
                      host='localhost',
                      use_unicode=True)

        self.cur = self.con.cursor()
        self.prs = Presentation()
        self.sample_text = "test1.pptx"
        self.select_qry = 'select name,sk,summary,headline,location from linkedin_meta where member_id = "%s" '
        self.select_qry1 = 'select exp_title,exp_company_name,start_date,end_date,exp_location from linkedin_experiences where profile_sk ="%s" limit 3'
        self.select_qry2 = 'select image_path from linkedin_connections where member_id = "%s" limit 1'
        self.select_qry3 = 'select edu_school_name,edu_degree,edu_start_year,edu_end_year  from linkedin_educations where profile_sk="%s" limit 3'
        self.select_qry4 =  'select exp_duration from linkedin_experiences where profile_sk ="%s"'
        self.main()

    def main(self):
        member_id = int(options.memberid)
        self.cur.execute(self.select_qry%member_id)
        rows = self.cur.fetchall()
        rows = rows[0]
        name,sk,summary,headline,location = rows
        self.cur.execute(self.select_qry2%member_id)
        img_path = self.cur.fetchall()
        try:img_path = img_path[0][0]
        except : img_path = ''
        self.get_ppt(rows,img_path,sk)

    def get_ppt(self,records,img_path,sk):
        self.cur.execute(self.select_qry1%sk)
        exp_data = self.cur.fetchall()
	title_only_slide_layout = self.prs.slide_layouts[0]
	slide = self.prs.slides.add_slide(title_only_slide_layout)
	shapes = slide.shapes
        #Adding title
	txBox = slide.shapes.add_textbox(left=Cm(0.7),top=Cm(0),width=Cm(10),height=Cm(1))
	tf = txBox.text_frame
	p = tf.add_paragraph()
	run = p.add_run()
	run.text = "Profile :"+ ' ' + records[0]
	font = run.font
        font.bold = True
	font.size = Pt(20)
        font.color.rgb = RGBColor(0,0,255)
	table = shapes.add_table(rows=5, cols=2, \
        left=Inches(2.0),top=Inches(1.0), width=Inches(2.0),\
        height=Inches(1.0)).table
	#  column widths
	table.columns[0].width = Inches(2)
	table.columns[1].width = Inches(6.0)
        table.cell(0, 0).text = 'Previous Organisation'
        table.cell(0, 1).text = exp_data[0][1]
        table.cell(1, 0).text  = 'Title/Designation'
	table.cell(1, 1).text  = records[3]
	table.cell(2, 0).text = 'Current Location'
	table.cell(2, 1).text = records[4]
        table.cell(3, 0).text = 'Work Experience'
        self.cur.execute(self.select_qry4%sk)
        exp_dur = self.cur.fetchall()
        exp_list = []
        if exp_duration : 
            for exp in exp_dur :
               if 'years' in exp[0] :
                   dura =  re.findall('\d+',exp[0])[0]
                   exp_list.append(int(dura))
               else :
                   exp_duration = 'Below 2 years'
            exp_duration = str(sum(exp_list))+'+ Years'
            table.cell(3,1).text= exp_duration

        #Setting font size for whole table
        for row in table.rows:
            for cell in row.cells:
               for paragraph in cell.text_frame.paragraphs:
                   for run in paragraph.runs:
                       run.font.size = Pt(7)

        self.cur.execute(self.select_qry1%sk)
        exp_data = self.cur.fetchall()
        #Creating second table 
        table2 = shapes.add_table(rows=3, cols=4, left=Inches(0.0), \
        top=Inches(2.5), width=Inches(6.0), height=Inches(0.5)).table
        table2.columns[0].width = Inches(2.0)
        table2.columns[1].width = Inches(5)
        table2.columns[2].width = Inches(1)
        table2.columns[3].width = Inches(2)
        table2.cell(0, 0).text = 'Professional experiences'
        table2.cell(1, 0).text = 'Education'
        table2.cell(2, 0).text = 'comments'
        #Merging cells horizantally
        row_idx=2
        start_col_idx=1
        end_col_idx=3
        col_count = end_col_idx - start_col_idx + 1
        row_cells = [c for c in table2.rows[row_idx].cells][start_col_idx:end_col_idx]
        row_cells[0]._tc.set('gridSpan', str(col_count))
        for c in row_cells[1:]:
            c._tc.set('hMerge', '2')
        row_idx=1
        start_col_idx=1
        end_col_idx=2
        col_count = end_col_idx - start_col_idx + 1
        row_cells = [c for c in table2.rows[row_idx].cells][start_col_idx:end_col_idx]
        row_cells[0]._tc.set('gridSpan', str(col_count))
        for c in row_cells[2:]:
            c._tc.set('hMerge', '2')
        
        table2.columns[2].width = Inches(2.0)
        table2.columns[3].width = Inches(1.0)
	for ind, colu in enumerate(exp_data):
		ans = ''
		for i in exp_data:
			if ind == 0:
				ans += '\n'.join(list(i[0:2]))+'\n\n'
			if ind == 1:
				ans += '\n'.join(list(i[2:4]))+'\n\n'
                        if ind == 2:
                                ans +=  "".join(list(i[4]))+'\n\n'
		try : 
                    table2.cell(0, ind+1).text = ans
                except : break

        self.cur.execute(self.select_qry3%sk)
        edu_data = self.cur.fetchall()
        for ind, colu in enumerate(edu_data):
                ans = ''
                for i in edu_data:
                        if ind == 0:
                                ans += '\n'.join(list(i[0:2]))+'\n\n'
                        if ind == 1:
                                ans += '-'.join(list(i[2:4]))+'\n\n'
                try :
                    if ind == 1 : table2.cell(1, ind+2).text = ans
                    if ind == 0 : table2.cell(1, ind+1).text = ans
                except : break

        table2.cell(2, 1).text = records[2]
        for row in table2.rows:
            for cell in row.cells:
               for paragraph in cell.text_frame.paragraphs:
                   for run in paragraph.runs:
                       run.font.size = Pt(7)

        #Inserting persons  image
        try : pic = slide.shapes.add_picture(img_path,\
              left=Inches(0),top=Inches(1),width=Inches(2),height=Inches(1.5)) 
        except : pic = ''

        #Inserting logo
        pic2 = slide.shapes.add_picture('/root/test/ppt/Pmoves-1.png', \
              left=Inches(8.5),top= Inches(0.2),width=Inches(1.2))
       
        self.prs.save('test1.pptx')
        

    def __del__(self):
        self.con.close()
        self.cur.close()

     

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-m', '--memberid', default=None, help='member_id')
    (options, args) = parser.parse_args()
    Login(options)

