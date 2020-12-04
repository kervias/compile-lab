from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import *
import sys
from LL1GUI import Ui_MainWindow
import copy


class LL1(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(LL1, self).__init__(parent)
        self.setupUi(self)
        self.initGUI()
        self.initValue()


    def initValue(self): #初始化基本的变量
        #需要初始化默认文法
        self.GrammarL = [] #使用列表存储文法,每个产生式用字符串表示
        self.GrammarD = {} #使用字典存储文法,每个产生式用列表中的字符串表示
        self.VN = [] #存放非终结符

        self.VT = [] #存放终结符
        self.StartCh = '' #文法开始符号
        self.inputStr = ''#'i+i*i' #输入的串
        self.FIRSTD = {} #存储First集,使用Dict字典存储
        self.FOLLOWD = {} #存储Follow集,使用Dict字典存储
        self.LL1AnalyzeList = None #存储LL1分析表，需要考虑用什么数据结构
        self.procedure = [] #步骤

        self.OLDVN = []
        self.OLDVT = []
        self.OLDGrammarL = []
        self.OLDGrammarD = {}

        self.GrammarL = [ #实验测试文法
            'E->TG',
            'G->+TG|-TG',
            'G->ε',
            'T->FS',
            'S->*FS|/FS',
            'S->ε',
            'F->(E)',
            'F->i',
        ]

        tmp = copy.deepcopy(self.GrammarL)
        """
        tmp = [  #作业题中文法
            'E->TG',
            'G->+E|ε',
            'T->FJ',
            'J->T|ε',
            'F->PH',
            'H->*H|ε',
            'P->(E)|a|b|^',
        ]
        
        tmp = [ #间接左递归文法
            'S->Qc|c',
            'Q->Rb|b',
            'R->Sa|a'
        ]
        """
        self.GrammarPreHandler(tmp) #文法预处理
        self.updateFirstAndFollow() #更新FIRST集和FOLLOW集
        self.updateLL1Grammer() #更新LL1分析表
        self.showGrammer()
        self.restoreOLD() #备份当前文法

        self.updateProcess()
        print('*//*/'*10)
        print(self.GrammarD)
        print(self.FIRSTD)
        print(self.FOLLOWD)
        print(self.LL1AnalyzeList)
        print(self.procedure)

    def initGUI(self): #初始化GUI
        self.pushButton.clicked.connect(self.getGrammarChanged)
        self.lineEdit.textChanged.connect(self.getInputLineChanged)

    def restoreOLD(self):
        #备份旧的文法
        self.OLDGrammarD =  copy.deepcopy(self.GrammarD)
        self.OLDGrammarL =  copy.deepcopy(self.GrammarL)
        self.OLDVN =  copy.deepcopy(self.VN)
        self.OLDVT =  copy.deepcopy(self.VT)

    def loadOLD(self):
        #加载旧的文法
        self.GrammarL = copy.deepcopy(self.OLDGrammarL)
        self.GrammarD = copy.deepcopy(self.OLDGrammarD)
        self.VT = copy.deepcopy(self.OLDVT)
        self.VN = copy.deepcopy(self.OLDVN)

    def showToProcess(self): #将内部过程显示到tableWidget中
        obj = self.tableWidget
        obj.setRowCount(len(self.procedure))
        obj.setColumnCount = 4
        obj.setHorizontalHeaderLabels(['分析栈', '剩余输入串', '所用产生式', '动作'])

        rowNum = obj.rowCount()  # 获取行数
        columnNum = obj.columnCount()  # 获取列数
        for i in range(0, rowNum):  # 将所有格子清除内容
            for j in range(0, columnNum):
                obj.setItem(i, j, None)
        for i in range(0, rowNum):
            for j in range(0, columnNum):
                item = QtWidgets.QTableWidgetItem(self.procedure[i][j])
                obj.setItem(i, j, item)
                obj.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                if j == 0:
                    obj.item(i, j).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                if j == 1:
                    obj.item(i, j).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def showToLL1List(self): #将LL1分析表显示到tableWidget中
        obj = self.tableWidget_2
        obj.setColumnCount(len(self.LL1AnalyzeList[self.StartCh].keys()))
        obj.setRowCount(len(list(self.LL1AnalyzeList.keys())))

        obj.setHorizontalHeaderLabels(list(self.LL1AnalyzeList[self.StartCh].keys()))
        obj.setVerticalHeaderLabels(list(self.LL1AnalyzeList.keys()))


        rowNum = obj.rowCount()  # 获取行数
        columnNum = obj.columnCount()  # 获取列数
        for i in range(0, rowNum):  # 将所有格子清除内容
            for j in range(0, columnNum):
                obj.setItem(i, j, None)
        t1 = self.LL1AnalyzeList.keys()
        t2= self.LL1AnalyzeList[self.StartCh].keys()
        for i in range(0, rowNum):
            for j in range(0, columnNum):
                ii = list(t1)[i]
                jj = list(t2)[j]
                item = QtWidgets.QTableWidgetItem(self.LL1AnalyzeList[ii][jj])
                obj.setItem(i, j, item)
                obj.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def showFisrtAndFollow(self): #显示first集和follow集
        firstSETshow = ''
        for i in self.FIRSTD.items():
            firstSETshow += 'FIRST(' + i[0] + ') = {' + ','.join(i[1]) + '}\n'
        followSETshow = ''
        for i in self.FOLLOWD.items():
            followSETshow += 'FOLLOW(' + i[0] + ') = {' + ','.join(i[1]) + '}\n'
        outputStr = firstSETshow + '\n' + followSETshow
        self.textBrowser.setText(outputStr)

    def showGrammer(self): #显示文法
        showstr = '\n'.join(self.GrammarL)
        self.plainTextEdit.setPlainText(showstr)

    def isLL1(self): #判断文法是不是LL1
        for i in self.VN:
            tmp = self.GrammarD[i]
            tSetL = []
            if (len(tmp) > 1):
                for j in tmp:
                    if j[0] in self.VT:
                        tSetL.append(set(j[0]))
                    else:
                        tSetL.append(set(self.FIRSTD[j[0]]))

                print(tSetL)
                for j in range(1, len(tSetL)):
                    slist = list(range(0, len(tSetL)))
                    slist.remove(j)
                    for k in slist:
                        sete = tSetL[j] & tSetL[k]
                        if len(sete) != 0:
                            return False

        for i in self.VN:
            tmp = self.GrammarD[i]
            tstr = ''.join(tmp)
            if 'ε' in tstr:
                sets = set(self.FOLLOWD[i]) & set(self.FIRSTD[i])
                if len(sets) != 0:
                    return False
        return True


    def getGrammarChanged(self): #监听文法输入是否被改变,需绑定
        getStr = self.plainTextEdit.toPlainText()
        tmpGrammarL = getStr.split('\n')
        ret = self.GrammarPreHandler(tmpGrammarL)
        if  'success' in ret:
            ret1 = self.updateFirstAndFollow()
            if ret1 != None:
                QMessageBox.warning(self, '警告', '该文法含有左递归')
                self.loadOLD()
                tmp = copy.deepcopy(self.GrammarL)
                self.GrammarPreHandler(tmp)
                self.updateFirstAndFollow()
                self.updateLL1Grammer()  # 更新分析表
                self.showGrammer()
                return

            if self.isLL1() == False:
                QMessageBox.warning(self, '警告', '该文法不是LL1的')
                self.loadOLD()
                tmp = copy.deepcopy(self.GrammarL)
                self.GrammarPreHandler(tmp)
                self.updateFirstAndFollow()
                self.updateLL1Grammer()  # 更新分析表
                self.showGrammer()
                return

            self.updateFirstAndFollow()
            self.updateLL1Grammer() #更新分析表
            self.inputStr = ''
            self.lineEdit.setText('')
            self.updateProcess()
            self.restoreOLD()
        else:
            QMessageBox.warning(self, '警告', ret)
            self.loadOLD()
            tmp = copy.deepcopy(self.GrammarL)
            self.GrammarPreHandler(tmp)
            self.updateFirstAndFollow()
            self.updateLL1Grammer()  # 更新分析表
            self.showGrammer()

    def getInputLineChanged(self): #监听输入串是否发生改变，需绑定
        print('line changed')
        getStr = self.lineEdit.text() #获取输入内容
        getStr = getStr.replace('\t','')
        getStr = getStr.replace(' ','')
        getStr = getStr.replace('\n','') #消除空格、换行符、制表符
        print('sf'*10)
        self.inputStr = getStr
        self.updateProcess()


    def is_zh(self,s): #判断是否有中文字符,不能判断中文标点符号
        for c in s:
            if  u'\u4e00' <= c <= u'\u9fff':
                return True
        return False

    def GrammarPreHandler(self, tmpGrammarL): #对文法进行处理
        #1.对非法字符进行处理
        tmpstr = ''.join(tmpGrammarL)
          #(1). 判断是否有中文字符
        if self.is_zh(tmpstr):
            return 'Illegal Character:含有中文字符'
          #(2). 判断是否含有'#'
        if '#' in tmpstr:
            return "Illegal Character:'#'"

        #2. 处理一些符号
        tmpGrammarL1 = []
        for t in tmpGrammarL:
            t = t.replace('\t','') #消除制表符
            t = t.replace(' ','') #消除空格
            t = t.replace('\n','') #消除换行符
            if t != '': #处理空行
                tmpGrammarL1.append(str(t))
        tmpGrammarL = tmpGrammarL1

        #3. 处理没有产生式
        if len(tmpGrammarL) == 0:
            return '产生式为空'

        #4. 处理一些非法情况
        for t in tmpGrammarL:
            if not t[0].isupper():#处理第一个字符不是大写字符
                return '产生式第一个字母不是大写字母：' + str(t)
            if len(t) <= 3:
                return '产生式太短:' + str(t)
            if t[1] != '-' or t[2] != '>':
                return '产生式没有"->":' + str(t)

        #5. 检查是否每一个非终结符都有一个产生式
        tmpVn = list(set([i[0] for i in tmpGrammarL]))
        tmpstr = ''.join(tmpGrammarL)
        tmpSet = set(tmpstr)
        tmpVn2 = [i for i in tmpSet if i.isupper()]
        if len(tmpVn) != len(tmpVn2):
            tmpX = set(tmpVn2) - set(tmpVn)
            return '含有非终结符没有产生式：' + ''.join(list(tmpX))

        #6. 正式储存文法
            #6.1 储存非终结符,开始符号放在第一个，其余符号排序
        self.VN = sorted(tmpVn) #排序存储
        self.VN.remove(tmpGrammarL[0][0])
        self.VN.insert(0,tmpGrammarL[0][0])
        self.StartCh = tmpGrammarL[0][0]
            #6.2 储存终结符
        tmpstr = ''.join([i[3::] for i in tmpGrammarL])
        tmpSet = set(tmpstr)
        tmpSet = tmpSet - set(tmpVn)
        self.VT = tmpSet - {'|'}
        self.VT  = list(self.VT)
            #6.3 将首字符相同的大写字符合并,产生self.GrammarL和self.GrammarD
        self.GrammarD = {}
        for i in self.VN:
            self.GrammarD[i] = []
        for t in tmpGrammarL:
            tt = t[3::].split('|')
            self.GrammarD[t[0]].extend(tt)
            xxL = list(set(self.GrammarD[t[0]]))
            self.GrammarD[t[0]] = xxL #去除相同文法

        self.GrammarL = []
        for t in self.GrammarD.items():
            self.GrammarL.append(t[0] + '->' + '|'.join(t[1]))
        self.GrammarL = sorted(self.GrammarL)
        tt = ''
        for t in self.GrammarL:
            if t[0] == self.StartCh:
                tt = t
        self.GrammarL.remove(tt)
        self.GrammarL.insert(0,tt) #让初始文法在开头
        return 'success!'

    def FIRST(self, curCH, proL): #找FIRST集的递归调用
        if curCH[0] not in self.VN:
            return [curCH[0]]
        curCH = curCH[0]
        if len(self.FIRSTD[curCH]) != 0: #如果之前找过了，就返回之前的
            return self.FIRSTD[curCH]
        tmL = self.GrammarD[curCH]
        #print(proL)
        a = []
        for i in tmL:
            if i[0] in self.VT: #第一个是终结符
                a.append(i[0])
            elif i[0] in self.VN: #第一个是非终结符
                if i[0] in proL:
                    return '左递归'
                else:
                	tt = 0
                	while tt < len(i):
	                    proL.append(i[tt])
	                    res = self.FIRST(i[tt],proL)
	                    proL.remove(i[tt])
	                    if res == '左递归':
	                        return '左递归'
	                    else:
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
            if ret == '左递归':
                return '左递归'
            elif ret == '异常':
                print('异常')
            else:
                self.FIRSTD[i] = list(set(ret))


    def equalFollow(self,t1,t2):
        if len(t1) != len(t2):
            return False
        for i in list(t1.keys()):
            if set(t1[i]) != set(t2[i]):
                return False
        return True

    def findFOLLOW(self): #找出FOLLOW集
        self.FOLLOWD = {}
        for t in self.VN:
            self.FOLLOWD[t] = []

        tmpFOLLOWD = copy.deepcopy(self.FOLLOWD) #复制一份
        self.FOLLOWD[self.StartCh].append('#')
        while not self.equalFollow(tmpFOLLOWD,self.FOLLOWD):
            tmpFOLLOWD = copy.deepcopy(self.FOLLOWD) #复制一份
            for t in self.GrammarD.items():
                for j in t[1]:
                    for kk in range(0,len(j)):
                        if j[kk] in self.VT:
                            continue
                        curCH = j[kk]
                        if kk != len(j)-1:
                            kk += 1
                            nextCH = j[kk] #下一个字符
                            if nextCH in self.VN: #下一个字符是非终结符
                                st = 0
                                while 'ε' in self.FIRSTD[nextCH]:
                                    tmp = copy.deepcopy(self.FIRSTD[nextCH])
                                    tmp.remove('ε')
                                    self.FOLLOWD[curCH].extend(tmp)
                                    self.FOLLOWD[curCH] = list(set(self.FOLLOWD[curCH]))
                                    kk += 1
                                    if kk == len(j):
                                        break
                                    nextCH = j[kk]
                                    if nextCH in self.VT:
                                        tmp = set(self.FOLLOWD[curCH])
                                        tmp.add(nextCH)
                                        self.FOLLOWD[curCH] = list(tmp)
                                        st = 1
                                        break
                                if st != 1:
                                    if kk >= len(j):
                                        tmp = copy.deepcopy(self.FOLLOWD[t[0]])
                                        self.FOLLOWD[curCH].extend(tmp)
                                        self.FOLLOWD[curCH] = list(set(self.FOLLOWD[curCH]))
                                    else:
                                        tmp = copy.deepcopy(self.FIRSTD[nextCH])
                                        self.FOLLOWD[curCH].extend(tmp)
                                        self.FOLLOWD[curCH] = list(set(self.FOLLOWD[curCH]))
                            else:
                                tmp = set(self.FOLLOWD[curCH])
                                tmp.add(nextCH)
                                self.FOLLOWD[curCH] = list(tmp)
                        else:
                            tmp = copy.deepcopy(self.FOLLOWD[t[0]])
                            self.FOLLOWD[curCH].extend(tmp)
                            self.FOLLOWD[curCH] = list(set(self.FOLLOWD[curCH]))

    def updateFirstAndFollow(self):
        #1. 根据文法更新First集和Follow集
        #2. 调用self.showFisrtAndFollow()
        ret = self.findFIRST()

        if ret == '左递归':
            return ret
        print(self.FIRSTD)
        print('33'*10)
        self.findFOLLOW()
        print('44'*10)
        print(self.FOLLOWD)

        self.showFisrtAndFollow()
        return None


    def updateLL1Grammer(self): #更新LL1分析表
        self.LL1AnalyzeList = {}
        tmpVTADD = copy.deepcopy(self.VT)
        tmpVTADD.append('#')
        if 'ε' in tmpVTADD:
            tmpVTADD.remove('ε')
        for i in self.VN:
            self.LL1AnalyzeList[i] = {}
            for j in tmpVTADD:
                self.LL1AnalyzeList[i][j] = ''

        for i in self.VN:
            for j in tmpVTADD:
                if j in self.FIRSTD[i]: #如果终结符在FISRST集内
                    for k in self.GrammarD[i]:
                        if k[0] == 'ε':
                            continue
                        elif k[0] in self.VN:
                        	tt = 0
                        	while tt < len(k):
                        		if j in self.FIRSTD[k[tt]]:
                        		    self.LL1AnalyzeList[i][j] = i + '->' + k
                        		    break
                        		elif('ε' in self.FIRSTD[k[tt]]):
                        			tt += 1
                        elif k[0] in self.VT:
                            if j == k[0]:
                                self.LL1AnalyzeList[i][j] = i + '->' + k
                                break
                elif 'ε' in self.FIRSTD[i] and j in self.FOLLOWD[i]: #如果终结符在FOLLOW内
                    self.LL1AnalyzeList[i][j] = i + '->' + 'ε'
        for i in self.VN:
            sorted(self.LL1AnalyzeList[i])

        for i in self.LL1AnalyzeList.items():
            print(i)

        #1. 根据Fisrt集和Follow集合更新LL1法分析表
        self.showToLL1List()


    def updateProcess(self): #更新处理过程， ！！！！！！！！！
        self.procedure = []
        stackCH = [] #符号栈
        inputstr = self.inputStr
        if inputstr == '':
            self.procedure = []
            self.showToProcess()
            return

        inputstr += '#'
        stackCH.append('#')
        stackCH.append(self.StartCh)

        flag = True
        point = 0
        self.procedure.append([''.join(stackCH), inputstr[point::], '','初始化'])
        while flag and point < len(inputstr):
            X = stackCH.pop()
            if X in self.VT:
                if X == inputstr[point]:
                    point += 1
                    self.procedure.append([''.join(stackCH), inputstr[point::], '','GETNEXT[I]'])
                else:
                    break
            elif X == '#':
                if X == inputstr[point]:
                    flag = False
                    #self.procedure.append([''.join(stackCH), inputstr[point::], ''])
                else:
                    break
            elif inputstr[point] in list(self.LL1AnalyzeList[self.StartCh].keys()) and self.LL1AnalyzeList[X][inputstr[point]] != '':
                tmp = list(self.LL1AnalyzeList[X][inputstr[point]][3::])
                if tmp[0] == 'ε':
                    #stackCH.pop()
                    self.procedure.append([''.join(stackCH), inputstr[point::],self.LL1AnalyzeList[X][inputstr[point]],'POP'])
                else:
                    tmp.reverse()
                    for i in tmp:
                        stackCH.append(i)
                    self.procedure.append([''.join(stackCH), inputstr[point::],self.LL1AnalyzeList[X][inputstr[point]],'POP,PUSH(' + ''.join(tmp) + ')'])
            else:
                break

        if(flag == True):
            self.procedure.append([''.join(stackCH), inputstr[point::],'Error','Error'])

        for i in self.procedure:
            print(i)
        self.showToProcess()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    LL_1 = LL1()
    LL_1.setWindowTitle('LL(1)分析法')
    LL_1.show()
    sys.exit(app.exec_())  # 使用exit()或者点击关闭按钮退出QApplication