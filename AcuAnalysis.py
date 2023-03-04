from utility import *
from Nifty import *
from BankNifty import *

output_data = ""
space_string = "&nbsp;<br />"
   
#print_hr() 
output_data += space_string + print_adv_dec()
output_data += space_string + print_adv_dec("BANK")
processNifty()
processBankNifty()
#print(json.dumps(dbData["thisProps"], indent = 2))
#print_hr()

json_object = json.dumps(dbData, indent=4)
 
# Writing to sample.json
with open("AcuAnalysisDB.json", "w") as outfile:
    outfile.write(json_object)

html_template = '<html><head><title>AcuTrade</title></head><body><h2>Welcome To AcuTrade</h2><strong>'
html_template += output_data
html_template += '</strong></body></html>'

with open("index.html", "w") as outfile1:
    outfile1.write(html_template)