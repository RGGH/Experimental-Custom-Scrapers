
# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

'''        Scraping the impossible?         '''
'''        Thanks to Code Monkey King       '''

# ROUND, ITEM GETTER, VARIABLE IN XPATH PREDICATE #

import csv
from operator import itemgetter
from requests_html import HTMLSession
#
#

# Make a List of dictionaries (CSS Name, left value, top value)
def css_dict(style):
    dct = {}
    try:
        # css name
        dct['name'] = style.split("{")[0].replace("\n","").strip()
        # left px
        left = style.split("left")[1].replace("\n","").replace(":","").strip().split(";")[0].replace("px","")
        dct['left'] = round((int(left)),-2) # left = round more
        #print(dct['left'])
        # top px
        top = style.split("left")[1].replace("\n","").replace(":","").strip().split(";")[1].split("top")[1].strip().replace("px","")
        dct['top'] = round((int(top)),-1) # top = round less
        #print(dct['top'])
        ls.append(dct)
    except:
        pass

# main
if __name__ == "__main__":

    session = HTMLSession()

    # URL of a Non Sequential CSS Site :
    url='http://audioeden.com/useddemo-gear/4525583102'
    r = session.get(url)
    ls = []
    # Get the <style> css to parse for column px, and row px values
    style = r.html.xpath("//style/text()")

    # put CSS into list so the top and left px can be found
    style = "".join(style)
    style = style.split("}")

    # build the list of dicitonaries
    len_ind = (len(style))
    for i in range (0, len_ind):
        #print(style[i])
        css_dict(style[i])

    #print(ls) - sorted by "left px", then "top px"
    ls.sort(key=itemgetter('left','top'))
    #print(ls)

    # get class name from dict, and get the matching text using the
    # "NAME" of the CSS STYLE to match the CLASS NAME - remove oddities
    print("Next - let's match sorted names with CSS / class names")
    ls_len = len(ls)
    print(f"Length of FULL List ={ls_len}")

    ls_desc = []
    ls_suggp = []
    ls_sellp = []

    # ~~~~~~~~~~~~ write DESCRIPTION for Column 'A'

    for i in range (len(ls)):
        cn = (ls[i]['name']) # <<<
        cl = (ls[i]['left'])
        # ct = (ls[i]['top'])
        #print(i)
        if cl == 300: # get **DESCRIPTION** TEXT
            if len(cn) > 1: # only print if it represents valid class
                cn = cn.replace(".","")
                divclass = str(cn + " " + "body")
                ### print(divclass) # Use this variable with f-string to get each speaker description
                tx = r.html.xpath(f'//div[@class="{divclass}"]/p[@class="p0"]/span[@class="c0"]/text()')
                tx = [x.replace("\xa0", "") for x in tx]

                try:
                    if len(tx[0]) > 2:
                        ls_desc.append(tx)
                    # else:
                    #     ls_desc.append("*")
                except:
                    pass

    # ~~~~~~~~~~~~ write SELLING PRICE for Column 'B'
    for i in range (len(ls)):
        cn = (ls[i]['name'])
        cl = (ls[i]['left'])
        ct = (ls[i]['top'])
        if cl ==900: # GET **SELLING** PRICE
            if len(cn) > 1: # only print if it represents valid class
                cn = cn.replace(".","")
                divclass = str(cn + " " + "body")
                ### print(divclass) # Use this variable with f-string to get each speaker description
                tx = r.html.xpath(f'//div[@class="{divclass}"]/p[@class="p0"]/span[@class="c0"]/text()')
                tx = [x.replace("\xa0", "") for x in tx]

                try:
                    if len(tx[0]) > 2 and len(tx[0]) < 10:
                        ls_sellp.append(tx)

                except:
                    pass

    #~~~~~~~~~~~~~~~~ write SUGGESTED PRICE for Column 'C'
    for i in range (len(ls)):
        cn = (ls[i]['name'])
        cl = (ls[i]['left'])
        ct = (ls[i]['top'])
        if cl >= 1000 and cl <= 1140 and ct > 150: # GET **Suggested Retail Price** PRICE
            if len(cn) > 1: # only print if it represents valid class
                cn = cn.replace(".","")
                divclass = str(cn + " " + "body")
                ### print(divclass) # Use this variable with f-string to get each speaker description
                tx = r.html.xpath(f'//div[@class="{divclass}"]/p[@class="p0"]/span[@class="c0"]/text()')
                tx = [x.replace("\xa0", "") for x in tx]

                try:
                    if len(tx[0]) >= 0: #and len(tx[0]) < 14:
                        ls_suggp.append(tx)

                    else:
                        ls_suggp.append("*")

                except:
                    pass

    ls_suggp.append("*") # fix the 2 x blanks
    ls_suggp.append("*")
    #~~~~~~~~~~~~~~~~

    print(ls_desc)
    print(str(len(ls_desc)))
    print("__")

    print(ls_sellp)
    print(str(len(ls_sellp)))
    print("__")

    print(ls_suggp)
    print(str(len(ls_suggp)))
    print("__")

zipped = zip(ls_desc,ls_sellp,ls_suggp)
rows = list(zipped)
#
header = ['Description', 'Selling Price', 'Suggested Price']
#
with open('a1.csv', 'wt') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    csv_writer.writerows(rows)
#     for i in x:
#         #Write item to outcsv
#         writer.writerow([x[0], x[1], x[2]])
