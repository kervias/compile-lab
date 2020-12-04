from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import copy
from LR1GUI import Ui_MainWindow
import string

class LR1(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(LR1, self).__init__(parent)
        self.setupUi(self)
        self.initGUI()
        self.initValue()

# ******* 1. 以下内容：初始化必要的变量、函数等 ********
    def initGUI(self): # 初始化GUI
        # 1. 初始化LR1分析表
        vtNum = 6 #需要设置
        vnNum = 4 #需要设置
        statusNum = 1; #需要设置
        self.tableWidget.setRowCount(statusNum+2)  # 需要设置
        self.tableWidget.setColumnCount(vtNum+1+vnNum)  # 需要设置
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSpan(0,0,2,1)
        self.tableWidget.setSpan(0,1,1,vtNum)
        self.tableWidget.setSpan(0,vtNum+1,1,vnNum)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tableWidget.horizontalHeader().setStretchLastSection(True);
        #self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)


        item = QtWidgets.QTableWidgetItem('状态')
        self.tableWidget.setItem(0,0,item)
        self.tableWidget.item(0, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = QtGui.QFont("等线", 12, QtGui.QFont.Bold)
        self.tableWidget.item(0, 0).setFont(font)
        item = QtWidgets.QTableWidgetItem('ACTION')
        self.tableWidget.setItem(0, 1, item)
        self.tableWidget.item(0, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.item(0, 1).setFont(font)
        item = QtWidgets.QTableWidgetItem('GOTO')
        self.tableWidget.setItem(0,vtNum+1, item)
        self.tableWidget.item(0, vtNum+1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.item(0,vtNum+1).setFont(font)

        # 2. 初始化LR1过程表
        #self.tableWidget2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget2.horizontalHeader().setStretchLastSection(True);
        self.tableWidget2.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget2.setHorizontalHeaderLabels(['状态栈', '符号栈', '输入串', '动作说明'])
        self.tableWidget2.setRowCount(3)  # 需要设置

        # 3. 初始化控件绑定事件
        self.lineEdit.textChanged.connect(self.inputLineChanged)
        self.pushButton.clicked.connect(self.grammarChanged)

    def initValue(self): #初始化必要变量
        self.GrammarL = []  # 使用列表存储文法,每个产生式用字符串表示
        self.GrammarL2 = []
        self.GrammarD = {}  # 使用字典存储文法,每个产生式用列表中的字符串表示
        self.VN = []  # 存放非终结符
        self.VT = []  # 存放终结符
        self.StartCh = ''  # 文法开始符号
        self.inputStr = ''#'i+i*i'  # 'i+i*i' #输入的串
        self.statusList = {} #状态表存储
        self.LR1AnalyzeList = {}
        self.procedure = []

        self.OLDVN = []
        self.OLDVT = []
        self.OLDGrammarL = []
        self.OLDGrammarD = {}
        self.GrammarLcc = [
            'S->BB',
            'B->aB',
            'B->b'
        ]
        self.GrammarL = [  # 实验测试文法
            'E->E+T',
            'E->T',
            'T->T*F',
            'T->F',
            'F->(E)',
            'F->i',
        ]
        self.GrammarLcc = [
            'S->L=R',
            'S->R',
            'L->*R',
            'L->i',
            'R->L',
        ]

        #以下调用处理过程，最终建立出LR1分析表
        tmp = copy.deepcopy(self.GrammarL)
        self.grammarPreHandler(tmp)
        print(self.VT)
        print(self.VN)
        self.findFIRST()
        print(self.FIRSTD)
        self.generateItemSet()
        self.generateLR1List()
        self.Fprocedure()
        self.showGrammer()
        #备份现有文法
        self.restoreOLD()

    def restoreOLD(self): # 备份旧的文法
        self.OLDstartCh = self.StartCh
        self.OLDGrammarD = copy.deepcopy(self.GrammarD)
        self.OLDGrammarD.pop(self.StartCh)
        self.OLDGrammarL = copy.deepcopy(self.GrammarL)
        self.OLDGrammarL.pop(0)
        self.OLDVN = copy.deepcopy(self.VN)
        self.OLDVT = copy.deepcopy(self.VT)

    def loadOLD(self): # 加载旧的文法
        self.GrammarL = copy.deepcopy(self.OLDGrammarL)
        self.GrammarD = copy.deepcopy(self.OLDGrammarD)
        self.VT = copy.deepcopy(self.OLDVT)
        self.VN = copy.deepcopy(self.OLDVN)

# ********* 2. 以下内容：将内部数据显示到GUI中  **************
    def showGrammer(self): #显示文法
        showstr = '\n'.join(self.GrammarL2)
        self.plainTextEdit.setPlainText(showstr)

    def showLR1List(self): #显示LR1分析表
        headers1 = list(self.ActionD['0'].keys())
        headers2 = list(self.GotoD['0'].keys())
        headers2.remove(self.StartCh)
        vtNum = len(headers1)  # 需要设置
        vnNum = len(headers2)  # 需要设置
        statusNum = len(self.statusList);  # 需要设置
        self.tableWidget.setRowCount(statusNum + 2)  # 需要设置
        self.tableWidget.setColumnCount(vtNum + 1 + vnNum)  # 需要设置
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()
        obj = self.tableWidget

        for i in range(2,rowCount):
            for j in range(0,columnCount):
                obj.setItem(i,j,None)

        headers1.sort(reverse=True)
        headers2.sort()
        headers = headers1 + headers2
        for i in range(1,columnCount):
            item = QtWidgets.QTableWidgetItem(headers[i-1])
            obj.setItem(1, i, item)
            obj.item(1, i).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        for i in range(2,rowCount):
            for j in range(0,vtNum+1):
                if(j == 0):
                    item = QtWidgets.QTableWidgetItem(str(i-2))
                else:
                    x = str(i-2)
                    y = headers1[j-1]
                    item = QtWidgets.QTableWidgetItem(str(self.ActionD[x][y]))
                obj.setItem(i,j,item)
                obj.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            for j in range(vtNum+1,vtNum+vnNum+1):
                x = str(i-2)
                y = headers2[j-vtNum-1]
                #print(x + '\t' + str(y))
                #print(str(i) + '\t' + str(j))
                item = QtWidgets.QTableWidgetItem(str(self.GotoD[x][y]))
                obj.setItem(i,j,item)
                obj.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def showProcedure(self): #显示处理过程
        obj = self.tableWidget2
        obj.setRowCount(len(self.procedure))
        rowNum = obj.rowCount()
        columnNum = obj.columnCount()
        for i in range(0,rowNum):
            for j in range(0,columnNum):
                item = QtWidgets.QTableWidgetItem(self.procedure[i][j+1])
                obj.setItem(i,j,item)
                obj.item(i,j).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                if j == 2:
                    obj.item(i, j).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    # ********* 3. 以下内容：当输入发生改变时的操作 ***************
    def inputLineChanged(self): #输入串改变
        getStr = self.lineEdit.text()  # 获取输入内容
        getStr = getStr.replace('\t', '')
        getStr = getStr.replace(' ', '')
        getStr = getStr.replace('\n', '')  # 消除空格、换行符、制表符
        self.inputStr = getStr
        self.Fprocedure()

    def grammarChanged(self): #文法改变
        getStr = self.plainTextEdit.toPlainText()
        tmpGrammarL = getStr.split('\n')
        ret = self.grammarPreHandler(tmpGrammarL)
        print(self.GrammarL2)
        print(self.GrammarL)
        if 'success' in ret:
            self.findFIRST()
            self.inputStr = ''
            self.lineEdit.setText('')
            self.generateItemSet()
            self.generateLR1List()
            self.Fprocedure()
            self.showGrammer()
            self.restoreOLD()
        else:
            QMessageBox.warning(self, '警告', ret)
            self.loadOLD()
            tmp = copy.deepcopy(self.GrammarL)
            self.grammarPreHandler(tmp)
            self.findFIRST()
            self.generateItemSet()
            self.generateLR1List()
            self.Fprocedure()
            self.showGrammer()


# ********* 4. 以下内容：对文法进行处理(预处理、存储文法、构造LR1分析表的过程) ***********
    def is_zh(self, s):  # 判断是否有中文字符,不能判断中文标点符号
        for c in s:
            if u'\u4e00' <= c <= u'\u9fff':
                return True
        return False

    def grammarPreHandler(self, tmpGrammarL):  # 对文法进行预处理
        # 1.对非法字符进行处理
        tmpstr = ''.join(tmpGrammarL)
        # (1). 判断是否有中文字符
        if self.is_zh(tmpstr):
            return 'Illegal Character:含有中文字符'
        # (2). 判断是否含有'#'
        if '#' in tmpstr:
            return "Illegal Character:'#'"

        # 2. 处理一些符号
        tmpGrammarL1 = []
        for t in tmpGrammarL:
            t = t.replace('\t', '')  # 消除制表符
            t = t.replace(' ', '')  # 消除空格
            t = t.replace('\n', '')  # 消除换行符
            if t != '':  # 处理空行
                tmpGrammarL1.append(str(t))
        tmpGrammarL = tmpGrammarL1

        # 3. 处理没有产生式
        if len(tmpGrammarL) == 0:
            return '产生式为空'

        # 4. 处理一些非法情况
        for t in tmpGrammarL:
            if not t[0].isupper():  # 处理第一个字符不是大写字符
                return '产生式第一个字母不是大写字母：' + str(t)
            if len(t) <= 3:
                return '产生式太短:' + str(t)
            if t[1] != '-' or t[2] != '>':
                return '产生式没有"->":' + str(t)

        # 5. 检查是否每一个非终结符都有一个产生式
        tmpVn = list(set([i[0] for i in tmpGrammarL]))
        tmpstr = ''.join(tmpGrammarL)
        tmpSet = set(tmpstr)
        tmpVn2 = [i for i in tmpSet if i.isupper()]
        if len(tmpVn) != len(tmpVn2):
            tmpX = set(tmpVn2) - set(tmpVn)
            return '含有非终结符没有产生式：' + ''.join(list(tmpX))

        # 生成拓广文法
        setA = set(string.ascii_uppercase) #生成26个大写字母，列表形式
        tmps = sorted(list(setA - set(tmpVn)))
        tmpVn.append(tmps[0])
        tmpGrammarL.insert(0,tmps[0]+'->'+tmpGrammarL[0][0])

        # 6. 正式储存文法
        # 6.1 储存非终结符,开始符号放在第一个，其余符号排序
        self.VN = tmpVn # 排序存储
        self.VN.remove(tmpGrammarL[0][0])
        self.VN.insert(0, tmpGrammarL[0][0])
        self.StartCh = tmpGrammarL[0][0]
        # 6.2 储存终结符
        tmpstr = ''.join([i[3::] for i in tmpGrammarL])
        tmpSet = set(tmpstr)
        tmpSet = tmpSet - set(tmpVn)
        self.VT = tmpSet - {'|'}
        #self.VT = sorted(list(self.VT),reverse = True)
        # 6.3 将首字符相同的大写字符合并,产生self.GrammarL和self.GrammarD
        self.GrammarD = {}
        for i in self.VN:
            self.GrammarD[i] = []
        for t in tmpGrammarL:
            tt = t[3::].split('|')
            self.GrammarD[t[0]].extend(tt)
            xxL = list(set(self.GrammarD[t[0]]))
            self.GrammarD[t[0]] = xxL  # 去除相同文法

        self.GrammarL = []
        for t in self.GrammarD.items():
            self.GrammarL.append(t[0] + '->' + '|'.join(t[1]))
        self.GrammarL = sorted(self.GrammarL)
        tt = ''
        for t in self.GrammarL:
            if t[0] == self.StartCh:
                tt = t
        self.GrammarL.remove(tt)
        self.GrammarL.insert(0, tt)  # 让初始文法在开头

        self.GrammarL2 = []
        for i in self.GrammarD.items():
            for j in i[1]:
                self.GrammarL2.append(i[0] + '->' + j)

        return 'success!'

    def FIRST(self, curCH, proL): #找FIRST集的递归调用
        if curCH[0] not in self.VN:
            return [curCH[0]]
        curCH = curCH[0]

        if len(self.FIRSTD[curCH]) != 0: #如果之前找过了，就返回之前的(只针对非终结符)
            return self.FIRSTD[curCH]
        tmL = self.GrammarD[curCH]
        #print(proL)
        a = []
        for i in tmL:
            if i[0] in self.VT: #第一个是终结符
                a.append(i[0])
            elif i[0] in self.VN: #第一个是非终结符
                if i[0] in proL:
                    continue
                else:
                    tt = 0
                    while tt < len(i):
                        proL.append(i[tt])
                        res = self.FIRST(i[tt],proL)
                        proL.remove(i[tt])
                        a.extend(res)
                        if 'ε' not in res:
                            break
                        tt += 1
            else:
                print('异常')
        self.FIRSTD[curCH] = sorted(list(set(a)))
        return  self.FIRSTD[curCH]

    def findFIRST(self): #找出FISRST集
        self.FIRSTD = {}
        for t in self.VN:
            self.FIRSTD[t] = []
        for i in self.VN:
            ret = self.FIRST(i,[i])
            if ret == '异常':
                print('异常')
            else:
                self.FIRSTD[i] = list(set(ret))
        return None

    def LR1Closure(self,statusD):
        while True:
            tmpStatusD = copy.deepcopy(statusD)
            for x1 in tmpStatusD.items():
                tmpstr = x1[0]
                ind =tmpstr.index('.') #找到小数点的索引
                ind += 1
                if ind < len(tmpstr):
                    if tmpstr[ind] in self.VN: #下一个是非终结符
                        for Query in self.GrammarD[tmpstr[ind]]:
                            if Query == 'ε':
                                Query = ''
                            generateQuery = tmpstr[ind] + '->.' + Query
                            fisrtstr = ''
                            firstSet = set()
                            #print(tmpstr)
                            if (ind + 1) == len(tmpstr):
                                firstSet = x1[1]
                            else:
                                if tmpstr[ind+1] in self.VN:
                                    tt = ind+1
                                    flag = False
                                    while tt < len(tmpstr):
                                        sett =  set(self.FIRSTD[tmpstr[tt]])
                                        if 'ε' in sett:
                                            sett -= {'ε'}
                                        else:
                                            flag = True
                                            firstSet |= sett
                                            break
                                        firstSet |= sett
                                        tt += 1
                                    #firstSet = set(self.FIRSTD[tmpstr[ind+1]])
                                    if flag == False:
                                        firstSet |= x1[1]
                                    #firstSet = set(self.FIRSTD[tmpstr[ind+1::]])
                                    #if 'ε' in self.FIRSTD[tmpstr[-1]]:
                                    	#firstSet |= x1[1]
                                else:
                                    firstSet.add(tmpstr[ind+1])
                            if generateQuery in list(statusD.keys()):
                                statusD[generateQuery] |= firstSet
                            else:
                                statusD[generateQuery] = firstSet
            if tmpStatusD == statusD:
                break

        return statusD

    def LR1GOTO(self,I,x): # I是项目集，x是一个文法符号
        J = {}
        for item in I.items():
            ind = item[0].index('.')
            if ind == (len(item[0]) - 1):
                #J.update(self.LR1Closure({item[0]:copy.deepcopy(item[1])}))
                continue
            else:
                if item[0][ind+1] != x:
                    continue
                tmpL = list(item[0])
                tmpL.remove('.')
                tmpL.insert(ind+1,'.')
                tmpstr = ''.join(tmpL)
                dic = {}
                dic[tmpstr] = item[1]
                J.update(self.LR1Closure(dic))
        return J

    def generateItemSet(self): #生成项目集
        self.statusList = {}
        print(self.GrammarL)
        print(self.GrammarL2)
        print(self.GrammarD)

        tmpstr = self.GrammarL[0]
        tmpstr = tmpstr[0:3] + '.' + tmpstr[3::]
        self.statusList['I0'] = self.LR1Closure({tmpstr:{'#'}}) #初始化状态,I0
        print(self.statusList['I0'])
        print('*'*10)

        while True:
            tmpStatusList = copy.deepcopy(self.statusList)
            for item in tmpStatusList.items(): #item是一个项目集
                for vn in self.VN: #文法符号中的非终结符
                    ret = self.LR1GOTO(copy.deepcopy(item[1]), vn)
                    if len(ret) != 0 and ret not in list(self.statusList.values()):
                        II = 'I' + str(len(self.statusList))
                        self.statusList[II] = ret
                for vt in self.VT: #文法符号中的终结符
                    ret = self.LR1GOTO(copy.deepcopy(item[1]), vt)
                    if len(ret) != 0 and ret not in list(self.statusList.values()):
                        II = 'I' + str(len(self.statusList))
                        self.statusList[II] = ret

            if tmpStatusList == self.statusList:
                break

        for i in self.statusList.items():
            print(i)

    def generateLR1List(self): #生成LR1分析表
        print(self.FIRSTD)
        self.LR1AnalyzeList = {}
        self.ActionD = {}
        self.GotoD = {}
        for j in range(0,len(self.statusList)):
            self.ActionD[str(j)] = {}
            self.GotoD[str(j)] = {}
            for i in set(self.VT)|{'#'}:
                self.ActionD[str(j)][i] = ''
            for i in self.VN:
                self.GotoD[str(j)][i] = ''

        ii = 0
        for item in self.statusList.items():
            for i in item[1].items():
                ind = i[0].index('.')
                if ind == len(i[0]) - 1: #归约
                    if i[0][0] != self.StartCh:
                        str1 = i[0][0:-1]
                        if str1[-1] == '>':
                            str1 += 'ε'
                        ind2 = self.GrammarL2.index(str1) + 1
                        for k in i[1]:
                            self.ActionD[str(ii)][k] = 'r' + str(ind2)
                    else:
                        for k in i[1]:
                            self.ActionD[str(ii)][k] = 'acc'
            for i in set(self.VT)|{'#'}: #Action
                ret = self.LR1GOTO(copy.deepcopy(item[1]),i)
                if len(ret) != 0:
                    tmp = list(self.statusList.values())
                    ind = tmp.index(ret)
                    self.ActionD[str(ii)][i] = 'S' + str(ind)
            for i in self.VN: #Goto
                ret = self.LR1GOTO(copy.deepcopy(item[1]), i)
                if len(ret) != 0:
                    tmp = list(self.statusList.values())
                    ind = tmp.index(ret)
                    self.GotoD[str(ii)][i] = ind
            ii += 1

        print('/'*10)
        print(self.GotoD)
        print(self.ActionD)
        self.showLR1List()

# ********* 5. 以下内容：对输入串进行模拟LR1分析 ********************
    def Fprocedure(self):
        self.procedure = []
        if self.inputStr == '':
            self.showProcedure()
            return
        stackStatus = [] #状态栈
        stackSymbol = [] #符号栈
        inputL = self.inputStr #输入串
        inputL += '#'
        point = 0

        ii = 1 #步骤
        stackStatus.append(str(0))
        stackSymbol.append('#')
        flag = True
        while flag:
            statusTop = stackStatus[-1]
            if inputL[point] not in set(self.VN)|set(self.VT)|set('#'):
                self.procedure.append([str(ii), ' '.join(stackStatus), ''.join(stackSymbol), inputL[point::], 'Error'])
                break
            cmd = self.ActionD[statusTop][inputL[point]]
            if 'S' in cmd: #状态跳转
                self.procedure.append([str(ii), ' '.join(stackStatus), ''.join(stackSymbol), inputL[point::],'ACTION['+statusTop+','+inputL[point]+']='+cmd+',状态'+cmd[1]+'入栈'])
                stackStatus.append(cmd[1::])
                stackSymbol.append(inputL[point])
                point += 1
                ii += 1
            elif 'r' in cmd:#归约
                rn = self.GrammarL2[int(cmd[1])-1]
                self.procedure.append([str(ii),' '.join(stackStatus), ''.join(stackSymbol), inputL[point::]]) #cmd+':'+rn+'归约'+'GOTO('+))
                if rn[-1] != 'ε':
                	stackStatus = stackStatus[0:(-1-(len(rn[3::])-1))] #出栈
                	stackSymbol = stackSymbol[0:(-1-(len(rn[3::])-1))] #出栈
                stackSymbol.append(rn[0])
                statusTop = stackStatus[-1]
                cmd2 = self.GotoD[statusTop][rn[0]]
                if cmd2 != '':
                    stackStatus.append(str(cmd2))
                    ii += 1
                    self.procedure[-1].extend([cmd+': '+rn+'归约,'+'GOTO('+stackStatus[-2]+','+rn[0]+')'+'='+str(cmd2)+'入栈'])
                else:
                    ii += 1
                    self.procedure[-1].extend(['ERROR','ERROR'])
                    break
            elif 'acc' in cmd:
                self.procedure.append([str(ii), ' '.join(stackStatus), ''.join(stackSymbol), inputL[point::],'Acc:分析成功'])
                flag = False
            else:
                self.procedure.append([str(ii), ' '.join(stackStatus), ''.join(stackSymbol), inputL[point::],'Error'])
                break
        """
        print('++'*10)
        for i in self.procedure:
            print(i)
        """

        self.showProcedure()

# ******** 【 主函数 】 ********
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    LR_1 = LR1()
    LR_1.setWindowTitle('LR(1)分析法')
    LR_1.show()
    sys.exit(app.exec_())  # 使用exit()或者点击关闭按钮退出QApplication
