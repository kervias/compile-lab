from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import *
import sys
from lexcialGUI import Ui_MainWindow
from lexcialShowDialog import Ui_Dialog
from SetPara import Ui_DialogSet
import re


class lexcial(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(lexcial, self).__init__(parent)
        self.setupUi(self)
        self.initGUI()
        self.initValue()
        self.initProcess()
        self.DefaultValue()
        self.setWindowTitle('lexcial:词法分析器')

    def initGUI(self): #初始化所有GUI
        # 初始化各种绑定
        self.action_ShowKEY.triggered.connect(self.FshowKEY)  # 绑定显示关键字事件
        self.actionOP_Arithmetic.triggered.connect(self.FshowOP_Arithmetic)
        self.actionOP_Relation.triggered.connect(self.FshowOP_Relation)
        self.actionOP_Delimiter.triggered.connect(self.FshowDelimeter)
        self.actionShowAll.triggered.connect(self.FshowAll)
        self.plainTextEdit.textChanged.connect(self.InputChanged)
        self.actionsetRule.triggered.connect(self.FshowRule)
        self.actionShowDefault.triggered.connect(self.FshowDeRule)
        self.actionReDefault_2.triggered.connect(self.DefaultValue)
        self.loadPushButton.released.connect(self.loadFile)
        self.savePushButton.released.connect(self.saveFile)
        self.actionAbout.triggered.connect(self.FshowAbout)
        #self.actionHelp.triggered.connect(self.Fhelp)

        # 初始化显示关键字对话框
        self.DialogShowKEY = Ui_Dialog()
        self.DialogShowKEY.setWindowTitle('显示关键字')

        # 初始化显示算术运算符对话框
        self.DialogOPArithmetic = Ui_Dialog()
        self.DialogOPArithmetic.setWindowTitle('显示算术运算符')
        #self.DialogOPArithmetic..connect(self.DialogArithClose)

        # 初始化显示关系运算符对话框
        self.DialogOPRelation = Ui_Dialog()
        self.DialogOPRelation.setWindowTitle('显示关系运算符')

        # 初始化显示分界符对话框
        self.DialogDelimeter = Ui_Dialog()
        self.DialogDelimeter.setWindowTitle('显示分界符')

        # 初始化显示所有对话框
        self.DialogShowAll = Ui_Dialog()
        self.DialogShowAll.setWindowTitle('显示全部')
        self.DialogShowAll.tableWidget.horizontalHeader().setVisible(True)
        #self.DialogShowAll.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.DialogShowAll.tableWidget.setHorizontalHeaderLabels(['关键字','算术运算符','关系运算符','分界符'])

        #初始化设置对话框
        self.DialogSet = Ui_DialogSet()
        self.DialogSet.setWindowTitle('设置Rule')
        self.DialogSet.setWindowModality(Qt.ApplicationModal)

        #初始化显示默认对话框
        self.DialogDefa = Ui_Dialog()
        self.DialogDefa.setWindowTitle('显示默认')
        self.DialogDefa.tableWidget.horizontalHeader().setVisible(True)
        # self.DialogShowAll.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.DialogDefa.tableWidget.setHorizontalHeaderLabels(['关键字', '算术运算符', '关系运算符', '分界符'])

    def initValue(self):
        pass
        #默认关键字
        self.DeKEY = \
            [
                'if', 'else', 'while', 'signed','throw', 'union' ,'this', 'volatile',
                'int','char','double','unsigned','const','goto','virtual','struct',
                'for','float', 'break', 'auto', 'class', 'operator', 'case','bool'
                'do','long','typedef','static','friend','template','default','true',
                'new','void','return', 'enum','try', 'short', 'continue', 'sizeof','false',
                'switch', 'private', 'protected','asm','catch', 'delete', 'public',
            ]

        #默认算术运算符
        self.DeArith = \
            [
                '+','-','*','/','++','--'
            ]

        #默认关系运算符
        self.DeRelation = \
            [
                '<','=','>','<=','>='
            ]

        #默认分界符
        self.DeDelim = \
            [
                ';',',','(',')','[',']','{','}','"',"'"
            ]

        #初始化基本变量
        self.mode = '默认' #默认模式
        self.UserKEY = self.DeKEY
        self.UserArith = self.DeArith
        self.UserRelation = self.DeRelation
        self.UserDelim = self.DeDelim


        self.initProcess()
        self.typeDict = {
            '1':'关键字',
            '2':'分界符',
            '3':'算术运算符',
            '4':'关系运算符',
            '5':'常数',
            '6':'标识符',
        }


    def initProcess(self): #初始化处理过程的变量
        self.curPoint = 0;  # 当前指针
        self.finalI = 0; # 最末指针
        self.curRow = 1;  # 当前行
        self.curColumn = 1;  # 当前列
        self.cont  = ''
        self.printList  = [] #输出的表格
        self.identifierL = []  # 存放标识符
        self.constantL = []  # 存放常数

# ------ 【1. 以下是GUI相关函数 】 ----------
    def RefreshValue(self): #刷新每个GUI显示的内容
        self.label.setText(self.mode)
        # 初始化显示对话框
        self.setListToTableWidget(self.UserKEY, self.DialogShowKEY.tableWidget)
        self.setListToTableWidget(self.UserArith, self.DialogOPArithmetic.tableWidget)
        self.setListToTableWidget(self.UserRelation, self.DialogOPRelation.tableWidget)
        self.setListToTableWidget(self.UserDelim, self.DialogDelimeter.tableWidget)
        self.set4ListToTableWidget(self.UserKEY, self.UserArith, self.UserRelation, self.UserDelim,
                                   self.DialogShowAll.tableWidget)

        # 初始化设置对话框
        self.setDialogSet(self.UserKEY, self.UserArith, self.UserRelation, self.UserDelim, self.DialogSet)
        self.InputChanged()

    def DefaultValue(self): #刷新为默认规则
        self.mode = '默认'
        self.label.setText(self.mode)
        #初始化显示对话框
        self.setListToTableWidget(self.DeKEY, self.DialogShowKEY.tableWidget)
        self.setListToTableWidget(self.DeArith,self.DialogOPArithmetic.tableWidget)
        self.setListToTableWidget(self.DeRelation,self.DialogOPRelation.tableWidget)
        self.setListToTableWidget(self.DeDelim,self.DialogDelimeter.tableWidget)
        self.set4ListToTableWidget(self.DeKEY,self.DeArith,self.DeRelation,self.DeDelim,self.DialogShowAll.tableWidget)

        #初始化设置对话框
        self.setDialogSet(self.DeKEY,self.DeArith,self.DeRelation,self.DeDelim,self.DialogSet)

        #初始化显示默认对话框
        self.set4ListToTableWidget(self.DeKEY, self.DeArith, self.DeRelation, self.DeDelim,self.DialogDefa.tableWidget)

        #初始化User
        self.UserKEY = self.DeKEY
        self.UserArith = self.DeArith
        self.UserRelation = self.DeRelation
        self.UserDelim = self.DeDelim

    def FshowDeRule(self): #显示默认对话框
        self.DialogDefa.show()
        self.DialogDefa.exec()

    def setDialogSet(self,List1,List2,List3,List4,obj): #专门为DialogSet设计，显示特定内容
        #参数obj是tabwidget
        str1 = '\t'.join(List1)
        str2 = '\t'.join(List2)
        str3 = '\t'.join(List3)
        str4 = '\t'.join(List4)
        obj.textEdit1.clear()
        obj.textEdit1.append(str1)
        obj.textEdit2.clear()
        obj.textEdit2.append(str2)
        obj.textEdit3.clear()
        obj.textEdit3.append(str3)
        obj.textEdit4.clear()
        obj.textEdit4.append(str4)

    def FshowKEY(self):  #显示关键字
        self.RefreshValue()
        self.DialogShowKEY.show()

    def FshowOP_Arithmetic(self): #显示算术运算符
        self.RefreshValue()
        self.DialogOPArithmetic.show()
        self.DialogOPArithmetic.exec_()

    def FshowOP_Relation(self): #显示逻辑运算符
        self.DialogOPRelation.show()
        self.DialogOPRelation.exec_()

    def FshowDelimeter(self): #显示分界符
        self.RefreshValue()
        self.DialogDelimeter.show()
        self.DialogDelimeter.exec_()

    def FshowAll(self): #显示所有
        self.RefreshValue()
        self.DialogShowAll.show()
        self.DialogShowAll.exec_

    def FshowAbout(self):
        QMessageBox.about(self, u'关于', u"\nAuthor: HFUT-CST-Kervia!    \nMore: 编译原理词法分析器")

    def FshowRule(self): #显示规则
        self.DialogSet.show()
        if self.DialogSet.exec_() == QtWidgets.QDialog.Accepted:
            #print('此处应处理修改的规则')
            #此处应该检查是否相关内容被修改
            strlist = []
            strlist.append(self.DialogSet.textEdit1.toPlainText())
            strlist.append(self.DialogSet.textEdit2.toPlainText())
            strlist.append(self.DialogSet.textEdit3.toPlainText())
            strlist.append(self.DialogSet.textEdit4.toPlainText())
            self.ruleChanged(strlist) #调用是否改变函数，如果改变，该函数就对其进行相应修改


    def setListToTableWidget(self,List,obj): #将List列表显示到obj(QtableWidget)中,不适用于showall
        k = 0
        obj.setRowCount(round(len(List)/2)+20) #设置行数
        rowNum = obj.rowCount()  # 获取行数
        columnNum = obj.columnCount()  # 获取列数
        for i in range(0,rowNum):
            for j in range(0,columnNum):
                if k >= len(List):
                    obj.setItem(i, j, None)
                else:
                    item = QtWidgets.QTableWidgetItem(List[k])
                    obj.setItem(i,j,item)
                    obj.item(i,j).setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                k = k + 1

    def set4ListToTableWidget(self,List1,List2,List3,List4,obj):
        tmp = [len(List1), len(List2),len(List3),len(List4)]
        maxrows = max(tmp)
        L = [List1,List2,List3,List4]
        obj.setRowCount(maxrows+20) #设置最大行数
        rowNum = obj.rowCount()  # 获取行数
        columnNum = obj.columnCount()  # 获取列数
        for i in range(0, rowNum): #将所有格子清除内容
            for j in range(0, columnNum):
                obj.setItem(i, j, None)
        for j in range(0,columnNum):
            for i in range(0,len(L[j])):
                item = QtWidgets.QTableWidgetItem(L[j][i])
                obj.setItem(i, j, item)
                obj.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def FprintList(self,obj):
        obj.setRowCount(len(self.printList))  # 设置最大行数
        rowNum = obj.rowCount()  # 获取行数
        columnNum = obj.columnCount()  # 获取列数
        for i in range(0, rowNum):  # 将所有格子清除内容
            for j in range(0, columnNum):
                obj.setItem(i, j, None)
        for i in range(0, len(self.printList)):
            item = QtWidgets.QTableWidgetItem(str(self.printList[i][0]))
            obj.setItem(i, 0, item)
            obj.item(i, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            tmpstr = ''
            if self.printList[i][1][0] == 'Error':
                tmpstr = 'Error'
            else:
                tmpstr = '(' + str(self.printList[i][1][0]) + ',' + str(self.printList[i][1][1]) +')'

            item = QtWidgets.QTableWidgetItem(tmpstr)
            obj.setItem(i, 1, item)
            obj.item(i, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            item = QtWidgets.QTableWidgetItem(self.printList[i][2])
            obj.setItem(i, 2, item)
            obj.item(i, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            tmpstr = '(' + str(self.printList[i][3][0]) + ',' + str(self.printList[i][3][1]) + ')'
            item = QtWidgets.QTableWidgetItem(tmpstr)
            obj.setItem(i, 3, item)
            obj.item(i, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

# ------ 【2. 用户修改触发函数】 -----
    def ruleChanged(self,strList): #判断设置对话框得到的内容是否被修改，并对修改内容进行相关的设置
        t0 = re.split(' |\t|\n|\r',strList[0])
        self.UserKEY = sorted(list(set(t0)),key = t0.index)
        t1 = re.split(' |\t|\n|\r',strList[1])
        self.UserArith = sorted(list(set(t1)),key = t1.index)
        t2 = re.split(' |\t|\n|\r',strList[2])
        self.UserRelation = sorted(list(set(t2)),key = t2.index)
        t3 = re.split(' |\t|\n|\r',strList[3])
        self.UserDelim = sorted(list(set(t3)),key = t3.index)
        self.mode = '用户自定义'
        if '' in self.UserKEY:
            self.UserKEY.remove('')
        if '' in self.UserArith:
            self.UserArith.remove('')
        if '' in self.UserRelation:
            self.UserRelation.remove('')
        if '' in self.UserDelim:
            self.UserDelim.remove('')
        self.RefreshValue()


    def InputChanged(self):
        self.initProcess()
        self.cont = self.plainTextEdit.toPlainText() + '\n'
        self.preProcess()  #预处理
        self.finalI = len(self.cont)
        if(self.cont == ''):
            return
        self.mainProcess()
        print(self.printList)
        self.FprintList(self.tableWidget)

    def mainProcess(self): #主处理程序
        while self.curPoint < self.finalI:
            self.oneWordProcess()
        else:
            print('到达末尾')

    def preProcess(self): #预处理，消除注释
        #cont.replace('  ',' ')
        print('s/*/*')
        regex1 = re.compile(r'\/\/.*\n') #匹配 //
        self.cont = re.sub(regex1,'',self.cont)
        regex2 = re.compile('\/\*[\s\S]*\*\/\n') #匹配 /* ... */
        self.cont = re.sub(regex2, '',self.cont)
        regex3 = re.compile('\/\*[\s\S]*\*\/')  # 匹配 /* ... */
        self.cont = re.sub(regex3, '', self.cont)
        self.cont.replace('\t',' ') #替换制表符为空格
        #print(self.cont)
        print('s/*/*')

    def isnumber(self,num):
        regex = re.compile(r"^(-?\d+)(\.\d*)?$")
        if re.match(regex, num):
            return True
        else:
            return False

    def oneWordProcess(self): #向前处理一个单词
        if(self.curPoint >= self.finalI): #处理完毕，到了字符串的末尾
            print('已经到达末尾')
            return
        elif self.cont[self.curPoint] == '\n': #处理换行
            self.curRow += 1
            self.curColumn = 1
            self.curPoint += 1
            #self.oneWordProcess()
            return
        elif self.cont[self.curPoint].isalpha(): #判断是否是字母
            tmpstr = ''
            while self.cont[self.curPoint].isalpha() or self.cont[self.curPoint].isdigit(): #得到一个word
                tmpstr = tmpstr + self.cont[self.curPoint]
                self.curPoint += 1

            if tmpstr in self.UserKEY: #查询是否在关键字表中
                tmp = [tmpstr, ['1',self.UserKEY.index(tmpstr)],'关键字',[self.curRow,self.curColumn]]
                self.printList.append(tmp)
                self.curColumn += 1
                return
            elif tmpstr in self.identifierL: #查询是否在标识符表中
                tmp = [tmpstr, ['6',self.identifierL.index(tmpstr)],'标识符',[self.curRow,self.curColumn]]
                self.printList.append(tmp)
                self.curColumn +=1
                return
            else: #添加到标识符表中
                tmp = [tmpstr, ['6', len(self.identifierL)], '标识符', [self.curRow, self.curColumn]]
                self.printList.append(tmp)
                self.identifierL.append(tmpstr)
                self.curColumn += 1
                return
        elif self.cont[self.curPoint].isdigit(): #判断是否是数字
            tmpstr = ''
            while self.cont[self.curPoint].isalpha() or self.cont[self.curPoint].isdigit() or self.cont[self.curPoint] == '.':
                tmpstr = tmpstr + self.cont[self.curPoint]
                self.curPoint += 1
            if tmpstr.isdigit() or self.isnumber(tmpstr): #是数字
                if tmpstr in self.constantL: #之前有过
                    tmp = [tmpstr, ['5', self.constantL.index(tmpstr)], '常数', [self.curRow, self.curColumn]]
                    self.printList.append(tmp)
                    self.curColumn += 1
                    return
                else:
                    tmp = [tmpstr, ['5', len(self.constantL)], '常数', [self.curRow, self.curColumn]]
                    self.printList.append(tmp)
                    self.constantL.append(tmpstr)
                    self.curColumn += 1
                    return
            else:
                tmp = [tmpstr, ['Error'], 'Error', [self.curRow, self.curColumn]]
                self.printList.append(tmp)
                self.curColumn += 1
                return
        elif self.cont[self.curPoint] in self.UserDelim: #判断是否在分界符表内
            tmp = [self.cont[self.curPoint],['2',self.UserDelim.index(self.cont[self.curPoint])],'分界符',[self.curRow, self.curColumn]]
            self.printList.append(tmp)
            self.curColumn += 1
            self.curPoint += 1
            return
        elif self.cont[self.curPoint] in [tt[0] for tt in self.UserArith]: #判断是否为算术运算符
            tmpstr = ''
            while not (self.cont[self.curPoint].isalpha() or self.cont[self.curPoint].isdigit() or self.cont[self.curPoint] in self.UserDelim or self.cont[self.curPoint] in [tt[0] for tt in self.UserRelation] or self.cont[self.curPoint].isspace()):
                tmpstr += self.cont[self.curPoint]
                self.curPoint += 1

            if tmpstr in self.UserArith: #是算术运算符
                tmp = [tmpstr, ['3', self.UserArith.index(tmpstr)],'算术运算符', [self.curRow, self.curColumn]]
                self.printList.append(tmp)
                self.curColumn += 1
                return
            else: #报错
                tmp = [tmpstr, ['Error'], 'Error', [self.curRow, self.curColumn]]
                self.printList.append(tmp)
                self.curColumn += 1
                return
        elif self.cont[self.curPoint] in [tt[0] for tt in self.UserRelation]: #判断是否为关系运算符
            tmpstr = ''
            while not (self.cont[self.curPoint].isalpha() or self.cont[self.curPoint].isdigit() or self.cont[
                self.curPoint] in self.UserDelim or self.cont[self.curPoint] in [tt[0] for tt in self.UserArith] or
                       self.cont[self.curPoint].isspace()):
                tmpstr += self.cont[self.curPoint]
                self.curPoint += 1
            if tmpstr in self.UserRelation:  # 是关系运算符
                tmp = [tmpstr, ['4', self.UserRelation.index(tmpstr)], '关系运算符', [self.curRow, self.curColumn]]
                self.printList.append(tmp)
                self.curColumn += 1
                return
            else:  # 报错
                tmp = [tmpstr, ['Error'], 'Error', [self.curRow, self.curColumn]]
                self.printList.append(tmp)
                self.curColumn += 1
                return
        elif self.cont[self.curPoint].isspace(): #处理空格
            self.curPoint += 1
            #self.oneWordProcess()
            return
        else: #报错
            tmpstr = self.cont[self.curPoint]
            tmp = [tmpstr, ['Error'], 'Error', [self.curRow, self.curColumn]]
            self.printList.append(tmp)
            self.curColumn += 1
            self.curPoint += 1
            return

# ----- 【3. 文件操作】 -------
    def loadFile(self): #导入文件，分析处理
        pass
        filename = QFileDialog.getOpenFileName(self, 'open file', './','All Files (*)')
        print(filename)
        if filename[0] == '':
            return
        try:
            with open(filename[0], 'r+',encoding='UTF-8') as f:
                my_txt = f.read()
                self.plainTextEdit.setPlainText(my_txt)
                self.InputChanged()
        except:
            QMessageBox.warning(self, '警告', '文件无法打开！')

    def saveFile(self): #保存文件
        """
        1. 保存标识符到Identifier.txt
        2. 保存常量到constant.txt
        3. 所有文件均保存到当前目录
        """
        with open('Identifier.txt','w',encoding='utf-8') as f:
            print(self.identifierL)
            f.write('指针'+'\t'+'关键字'+'\n')
            for i in range(0,len(self.identifierL)):
                f.write(str(i) + '\t' + self.identifierL[i]+'\n')

        with open('Constant.txt','w',encoding='utf-8') as f:
            print(self.constantL)
            f.write('指针' + '\t' + '关键字'+'\n')
            for i in range(0,len(self.constantL)):
                f.write(str(i) + '\t' + self.constantL[i]+'\n')
        QMessageBox.information(self,'提示','文件保存成功!\n标识符：Identifier.txt\n常量：Constant.txt\n所有文件均在当前目录下！\n当前目录：'+sys.path[0])



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    Lex = lexcial()
    Lex.show()
    sys.exit(app.exec_())  # 使用exit()或者点击关闭按钮退出QApplication
