#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
#   |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|    #
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#

'''        Scraping the impossible?         '''
'''        Thanks to Code Monkey King       '''

# ROUND, ITEM GETTER, VARIABLE IN XPATH PREDICATE #

from requests_html import HTMLSession
import json
from operator import itemgetter
#
#
ls = []
# Make a List of dictionaries (CSS Name, left value, top value)
def css_dict(style):
    dct = {}
    try:
        # css name
        dct['name'] = style.split("{")[0].replace("\n","").strip()
        # left px
        left = style.split("left")[1].replace("\n","").replace(":","").strip().split(";")[0].replace("px","")
        dct['left'] = round((int(left)),-2) # left = round more
        # top px
        top = style.split("left")[1].replace("\n","").replace(":","").strip().split(";")[1].split("top")[1].strip().replace("px","")
        dct['top'] = round((int(top)),-1) # top = round less
        ls.append(dct)
    except:
        pass

# main
if __name__ == "__main__":

    session = HTMLSession()
    url='http://audioeden.com/useddemo-gear/4525583102'

    r = session.get(url)

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
    print(f"Length of List ={ls_len}")
    for i in range(ls_len):
        cn = (ls[i]['name'])
        cl = (ls[i]['left'])
        ct = (ls[i]['top'])
        if len(cn) > 1: # only print if it represents valid class
            if cl ==   300:
                ### print(cn, cl, ct)
                cn = cn.replace(".","")
                divclass = str(cn + " " + "body")
                ### print(divclass) # Use this variable with f-string to get each speaker description
                tx = r.html.xpath(f'//div[@class="{divclass}"]/p[@class="p0"]/span[@class="c0"]/text()')
                tx = [x.replace("\xa0", "") for x in tx]
                print(tx)
    #
    print (f"{cn} Decriptions of the Used/Demo Gear!")
    #
