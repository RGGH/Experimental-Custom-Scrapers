from requests_html import HTMLSession
import json
from operator import itemgetter
#
#
ls = []
# Method makes a LIST of DICTIONARIES (Keys : CSS Name, left value, top value)
def css_dict(style):
    dct = {}
    try:
        # css name
        dct['name'] = style.split("{")[0].replace("\n","").strip()
        # left px
        left = style.split("left")[1].replace("\n","").replace(":","").strip().split(";")[0].replace("px","")
        dct['left'] = round((int(left)),-2) # left = round more  ## ROUND !
        # top px
        top = style.split("left")[1].replace("\n","").replace(":","").strip().split(";")[1].split("top")[1].strip().replace("px","")
        dct['top'] = round((int(top)),-1) # top = round less ## ROUND !
        ls.append(dct)
    except:
        pass

# MAIN

if __name__ == "__main__":

    session = HTMLSession()
    url='http://audioeden.com/useddemo-gear/4525583102'

    r = session.get(url)
    
    # Get the <style></style> html (css)
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
    ls.sort(key=itemgetter('left','top')) # !! ITEM GETTER !!
    #print(ls)

    # get class name FROM list of dictionaries, and then use the matching text,
    # i.e make selector with a CLASS variable == "NAME" of the CSS STYLE match the CLASS NAME - ! remove oddities
    print("Next - let's match sorted names with CSS / class names")
    ls_len = len(ls)
    print(f"Length of List ={ls_len}")
    for i in range(ls_len):
        cn = (ls[i]['name'])
        cl = (ls[i]['left'])
        ct = (ls[i]['top'])
        if len(cn) > 1: # only print if it represents valid class
            if cl ==   300:
                print(cn, cl, ct)
                cn = cn.replace(".","")
                divclass = str(cn + " " + "body")
                print(divclass) # Use this variable with f-string to get each speaker description !! FSTRING in XPATH !!
                tx = r.html.xpath(f'//div[@class="{divclass}"]/p[@class="p0"]/span[@class="c0"]/text()')
                print(tx)
    #
    print (f"{cn} Decriptions of the Used/Demo Gear!")
    #

