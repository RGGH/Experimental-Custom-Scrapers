from requests_html import HTMLSession
import json
from operator import itemgetter
#
url='http://audioeden.com/useddemo-gear/4525583102'
session = HTMLSession()
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
#
r = session.get(url)
style = r.html.xpath("//style/text()")
#
# put CSS into list
style = "".join(style)
style = style.split("}")

len_ind = (len(style))
for i in range (0, len_ind):
    #print(style[i])
    css_dict(style[i])

#print(ls) - sorted by "left px", then "top px"
ls.sort(key=itemgetter('left'))
print(ls)

# next get matching div class name and get its text #
