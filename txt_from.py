import re
class txtfrom:
    def __init__(self):
        self.alls = []
        self.py = []
        self.shell = []
        self.p = []
        self.pyif = False
        self.shellif = False
        self.pif = False
    def txtp(self):
        with open('txt/2.txt','r+',encoding='utf-8') as f:
            txt = f.read().split('\n')

        for i in txt:
            match = re.search(r'<(.*?)>', i)
            #python代码判断
            try:
                label = match.group(1)
            except:
                label = None
            if match:
                if label == 'py':
                    self.py.append(i.replace('<py>',''))
                    self.pyif = True
                #-------------------------------------------------------------------
                #shell代码判断
                elif match and label == 'shell':
                    self.shell.append(i.replace('<shell>',''))
                    self.shellif = True
                #-------------------------------------------------------------------
            elif not match and self.pif == True:
                self.alls.append([['p'],self.p])
                self.pif = False
                self.p = []
                self.alls.append([['p'],[i]])
            elif self.pif == False:
                if self.pyif == False and self.shellif == False and self.pyif == False and not match:
                    self.p.append(i)
                    self.pif = True
                elif label != 'py' and self.pyif == True:
                    self.alls.append([['py'],self.py])
                    self.pyif = False
                    self.py = []
                    self.p.append(i)
                elif label != 'shell' and self.shellif == True:
                    self.alls.append([['shell'],self.shell])
                    self.shellif = False
                    self.shell = []
                    self.p.append(i)
            else:
                 self.alls.append([['p'],[i]])
            print('python',self.py)
            print('p',self.p)
            print('sheel',self.shell)
        # for a in self.alls:
        #     print(a,'\n')
        # return self.alls
        # return self.alls
        # return self.alls
if __name__ == '__main__':
    t = txtfrom()
    print(t.txtp())