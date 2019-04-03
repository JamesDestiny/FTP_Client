from UI.FTP客户端 import *
from PyQt5.QtCore import *
from  PyQt5.QtWidgets import *
from PyQt5.Qt import *
from ftplib import FTP
import configparser
from Ftp_clicent import ftp_clicent
from PyQt5.QtWidgets import QFileSystemModel
class zhuye(QDialog,Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self,parent=None)
        self.setupUi(self)
        self.pushButton_2.setEnabled(False)#当还未连接FTP服务器时，将不可利用的按钮全部变成不可以选
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.label_4.setText('')
        self.Set_file_Tree()

    #定义获取文件的绝对路径来复制到文本输入框中，用来文件上传
    def getfilepath(self):
        try:
            file_path = QFileDialog.getOpenFileName(self,'浏览','D:/Desktop/FTP_Server')
            return file_path[0]#返回文件的绝对路径
        except Exception as e:
            QMessageBox.information(self,"错误",str(e))
    #定义按钮浏览目录的函数
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        try:
            self.lineEdit_2.setText(str(self.getfilepath()))
        except Exception as e:
            QMessageBox.information(self,"错误",str(e))

    #定义连接FTP服务器的按钮的函数
    @pyqtSlot()
    def on_pushButton_clicked(self):
        try:
            if self.lineEdit.text()=='' or self.lineEdit_3.text()=='':
                QMessageBox.information(self,"错误","IP,端口号输入不能为空！")
            else:
                self.client = ftp_clicent(self.lineEdit.text(), int(self.lineEdit_3.text()))
                if self.client.login_withUser()==1:
                    self.label_4.setText('已连接， 服务器返回信息：'+str(self.client.getmess()))
                    self.pushButton.setEnabled(False)
                    self.pushButton_6.setEnabled(False)
                    self.pushButton_2.setEnabled(True)  # 当连接FTP服务器时，将不可利用的按钮全部变成可以选
                    self.pushButton_3.setEnabled(True)
                    self.pushButton_4.setEnabled(True)
                    self.get_tree_file(self.client.getdirwith(),'\\',self.root)
                else:
                    QMessageBox.information(self,'错误','连接失败！')
        except Exception as e:
            QMessageBox.information(self,"错误",str(e))

    #定义断开FTP服务器的按钮的函数
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        try:
            if self.client:
                try:
                    self.client.close_client()
                    QMessageBox.information(self,'提示',"已断开与FTP服务器的连接！")
                    self.pushButton_2.setEnabled(False)
                    self.pushButton_6.setEnabled(True)
                    self.pushButton.setEnabled(True)
                    self.pushButton_3.setEnabled(False)
                    self.pushButton_4.setEnabled(False)
                    self.label_4.setText('')
                    self.treeWidget.clear()
                    self.Set_file_Tree()
                except Exception as e:
                    QMessageBox.information(self,'错误',str(e))
            elif self.client2:
                try:
                    self.client2.close_client()
                    QMessageBox.information(self,'提示',"已断开与FTP服务器的连接！")
                    self.pushButton_2.setEnabled(False)
                    self.pushButton_6.setEnabled(True)
                    self.pushButton.setEnabled(True)
                    self.pushButton_3.setEnabled(False)
                    self.pushButton_4.setEnabled(False)
                    self.label_4.setText('')
                    self.treeWidget.clear()
                    self.Set_file_Tree()
                except Exception as e:
                    QMessageBox.information(self,'错误',str(e))
        except Exception as e:
            QMessageBox.information(self,"错误",str(e))


    #定义上传文件的按钮的函数
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        try:
            if self.lineEdit_2.text()=='':
                QMessageBox.information(self,'错误','输入不能为空！')
            else:
                if self.client:
                    status = self.client.upload(self.lineEdit_2.text(),self.lineEdit_2.text())
                    if status==1:
                        QMessageBox.information(self,'提示','上传成功！')
                    else:
                        QMessageBox.information(self,'提示','上传失败！')
                elif self.client2:
                    status = self.client2.upload(self.lineEdit_2.text(), self.lineEdit_2.text())
                    if status == 1:
                        QMessageBox.information(self, '提示', '上传成功！')
                    else:
                        QMessageBox.information(self, '提示', '上传失败！')
        except Exception as e:
            QMessageBox.information(self,"错误",str(e))

    #定义下载文件的按钮的函数
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        try:
            if self.treeWidget.currentItem():
                if self.from_file_getPath('file_path')!='':
                    item = self.treeWidget.currentItem().text(1)#获取tree中当前被选中的某一行的值
                    if self.client:
                        status = self.client.download(item)#为服务器文件的绝对路径，从文件目录树的点击中获取
                        if status ==1:
                            QMessageBox.information(self,'提示','下载成功！')
                        else:
                            QMessageBox.information(self,'提示','下载失败！')
                    elif self.client2:
                        status = self.client2.download(item)  # 为服务器文件的绝对路径，从文件目录树的点击中获取
                        if status == 1:
                            QMessageBox.information(self, '提示', '下载成功！')
                        else:
                            QMessageBox.information(self, '提示', '下载失败！')
                else:
                    QMessageBox.information(self,'提示','还未设置下载文件的保存路径！')
            else:
                QMessageBox.information(self,'警告','未选择要下载的服务器文件！')
        except Exception as e:
            QMessageBox.information(self,'错误',str(e))

    #定义保存用户连接信息的按钮函数
    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        try:
            if self.lineEdit_4.text()=='' or self.lineEdit_5.text()=='':
                QMessageBox.information(self,"提示","输入用户名或者密码不能为空！")
            else:
                config = configparser.ConfigParser()
                config.add_section('User_info')
                config.set('User_info','user',str(self.lineEdit_4.text()))
                config.set('User_info','password',str(self.lineEdit_5.text()))
                with open('User_info.ini','w') as conf:
                    config.write(conf)
                QMessageBox.information(self,'提示','连接信息保存成功！')
                self.lineEdit_4.setText('')
                self.lineEdit_5.setText('')
        except Exception as e:
            QMessageBox.information(self,"错误",str(e))

    #定义匿名连接的按钮函数
    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        try:
            if self.lineEdit.text()=='' or self.lineEdit_3.text()=='':
                QMessageBox.information(self,"错误","IP,端口号输入不能为空！")
            else:
                self.client2 = ftp_clicent(self.lineEdit.text(), int(self.lineEdit_3.text()))
                if self.client2.login_withoutUser()==1:
                    self.label_4.setText('已连接， 服务器返回信息：'+str(self.client2.getmesswithout()))
                    self.pushButton.setEnabled(False)
                    self.pushButton_6.setEnabled(False)
                    self.pushButton_2.setEnabled(True)  # 当连接FTP服务器时，将不可利用的按钮全部变成可以选
                    self.pushButton_3.setEnabled(True)
                    self.pushButton_4.setEnabled(True)
                    self.get_tree_file_without(self.client2.getdirwith(), '\\', self.root)
                else:
                    QMessageBox.information(self,'错误',"连接失败！")
        except Exception as e:
            QMessageBox.information(self,"错误",str(e))

        # 定义从Path_info配置文件中获取连接信息的函数
    def from_file_getPath(self, strings):
            try:
                config = configparser.ConfigParser()
                config.read('Path_info.ini')
                return config.get('Path_info', strings)
            except Exception as e:
                print(str(e))
    #保存下载存储路径的函数
    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        try:
            if self.lineEdit_6.text()=='':
                QMessageBox.information(self,'警告','输入不能为空!')
            else:
                config = configparser.ConfigParser()
                config.add_section('Path_info')
                config.set('Path_info', 'file_path', str(self.lineEdit_6.text()))
                with open('Path_info.ini', 'w') as conf:
                    config.write(conf)
                QMessageBox.information(self, '提示', '下载路径信息保存成功！')
                self.lineEdit_6.setText('')
        except Exception as e:
            QMessageBox.information(self,'错误',str(e))
    #设定浏览按键，返回文件浏览目录的函数
    def setBrowerPath(self):
        try:
            download_path = QFileDialog.getExistingDirectory(self,'浏览','D:/Desktop/FTP_Server')
            return download_path
        except Exception as e:
            QMessageBox.information(self,'错误',str(e))
    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        try:
            file_path = self.setBrowerPath()
            self.lineEdit_6.setText(str(file_path))
        except Exception as e:
            QMessageBox.information(self,'错误',str(e))
    #判断是文件还是文件夹
    def isdir(self,strings):
        try:
            if self.client and self.client.indir(strings)==1:
                return 1
            elif  self.client2 and self.client2.indir(strings)==1:
                return 1
            else:
                return 0
        except:
            return 0

    #定义递归函数获取一个固定路径下的带有绝对路径的文件内容,并将其打印成文件浏览器的桌面显示
    def get_tree_file(self,path,string,node):
        try:
            for i in path:
                if self.isdir(i):#新建一个新的节点来存储文件夹
                    child = QTreeWidgetItem(node)
                    child.setText(0,str(i))
                    self.client.change_get(i)
                    self.get_tree_file(self.client.getdirwith(),string+str(i)+'\\',child)
                else:
                    new_file_child = QTreeWidgetItem(node)
                    new_file_child.setText(0,str(i))
                    new_file_child.setText(1,string+str(i))
                    #print(string+str(i))
            self.treeWidget.expandAll()
        except Exception as e:
            QMessageBox.information(self,'错误',str(e))


    #定义匿名连接服务器时的文件递归显示函数
    def get_tree_file_without(self,path,string,node):
        try:
            for i in path:
                if self.isdir(i):#新建一个新的节点来存储文件夹
                    child = QTreeWidgetItem(node)
                    child.setText(0,str(i))
                    self.client2.change_get(i)
                    self.get_tree_file(self.client2.getdirwith(),string+str(i)+'\\',child)
                else:
                    new_file_child = QTreeWidgetItem(node)
                    new_file_child.setText(0,str(i))
                    new_file_child.setText(1,string+str(i))
                    #print(string+str(i))
            self.treeWidget.expandAll()
        except Exception as e:
            QMessageBox.information(self,'错误',str(e))

    def Set_file_Tree(self):
        try:
            self.treeWidget.setColumnCount(2)
            self.treeWidget.setColumnWidth(0,300)
            self.treeWidget.setHeaderLabels(['服务器文件名','文件绝对路径'])
            self.root = QTreeWidgetItem(self.treeWidget)
            self.root.setText(0,'根目录')

        except Exception as e:
            QMessageBox.information(self,'错误',str(e))