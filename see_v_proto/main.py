import cv
from datetime import date
from weasyprint import HTML
"""
choice = raw_input("New entry?")
while (choice.upper() == "Y"):
	category = raw_input("Category: ")
	content = raw_input("Content: ")
	choice = raw_input("New entry?")
"""

group1 = cv.CVGroup()

group1.set_name("Education")

entry1 = cv.CVEntry()
entry1.add_tag("UKZN")
entry1.add_tag("IT")
entry1.set_content("BSc IT")
entry1.set_date(date(2007,6,1))

entry2 = cv.CVEntry()
entry2.add_tag("UKZN")
entry2.add_tag("IT")
entry2.set_content("Honours IT")
entry2.set_date(date(2008,6,1))

group1.add_entry(entry1)
group1.add_entry(entry2)



group2 = cv.CVGroup()

group2.set_name("Work Experience")

work_entry1 = cv.CVEntry()
work_entry1.add_tag("FNB")
work_entry1.add_tag("IT")
work_entry1.set_content("I built a cool application at FNB. I built a cool application at FNB. I built a cool application at FNB. I built a cool application at FNB. I built a cool application at FNB.I built a cool application at FNB")
work_entry1.set_date(date(2009,1,1))

group2.add_entry(work_entry1)

HTML(string = group1.to_html() + group2.to_html()).write_pdf("test.pdf")