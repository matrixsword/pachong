import re,time
class MyRegex:
    def myFindall(self,sourstr):
        pattern = re.compile('"mp4_hd_url":"(.*?)"')
        return pattern.findall(sourstr)
        #return re.findall(pattern,sourstr)
#m=MyRegex()
# m.myFindall(open('a.txt','r',encoding='utf8').read())
