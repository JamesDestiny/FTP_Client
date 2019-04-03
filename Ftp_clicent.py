from ftplib import FTP#从标准库中导入FTP包
import configparser
import re#引用正则表达式，来切割文件名
class ftp_clicent():
    def __init__(self,server_ip,server_port):
        self.user = self.from_file_getUser('user')
        self.password = self.from_file_getUser('password')
        self.server_ip = server_ip
        self.server_port = server_port

    #定义匿名登录函数
    def login_withoutUser(self):
        try:
            self.ftp2 = FTP()
            self.ftp2.connect(host=self.server_ip,port=self.server_port)
            self.ftp2.login()
            return 1
        except Exception as e:
            print(str(e))
            return 0

    #定义实名登录函数
    def login_withUser(self):
        try:
            self.ftp = FTP()
            self.ftp.connect(host=self.server_ip,port=self.server_port)
            self.ftp.login(user=self.user,passwd=self.password)
            return 1
        except Exception as e:
            print(str(e))
            return 0

    #定义返回登录后目录的函数
    def getdirwith(self):
        try:
            if self.ftp:
                return self.ftp.nlst()
        except Exception as e:
            print(str(e))

    def getdirwithout(self):
        try:
            if self.ftp2:
                return self.ftp2.nlst()
        except Exception as e:
            print(str(e))

    #返回服务器连接信息
    def getmess(self):
        try:
            return self.ftp.getwelcome()
        except Exception as e:
            print(str(e))

    #定义改变当前目录，并且获取新的目录下的文件
    def change_get(self,strings):
        try:
            if self.ftp and self.indir(strings):
                self.ftp.cwd('/'+strings)
                return self.ftp.nlst()
        except Exception as e:
            print(str(e))

    def change_get_without(self,strings):
        try:
            if self.ftp2 and self.indir(strings):
                self.ftp2.cwd('/'+strings)
                return self.ftp2.nlst()
        except Exception as e:
            print(str(e))

    def getmesswithout(self):
        try:
            return self.ftp2.getwelcome()
        except Exception as e:
            print(str(e))
    #定义从User_info配置文件中获取连接信息的函数
    def from_file_getUser(self,strings):
        config = configparser.ConfigParser()
        config.read('User_info.ini')
        return config.get('User_info',strings)

    #定义从Path_info配置文件中获取连接信息的函数
    def from_file_getPath(self,strings):
        try:
            config = configparser.ConfigParser()
            config.read('Path_info.ini')
            return config.get('Path_info',strings)
        except Exception as e:
            print(str(e))

    #定义关闭连接的函数
    def close_client(self):
        try:
            if self.ftp:
                self.ftp.quit()
            elif self.ftp2:
                self.ftp2.quit()
        except Exception as e:
            print(str(e))

    #判断在当前的连接下，指定文件为文件或者是文件夹
    def indir(self,strings):
        try:
            if self.ftp and self.ftp.cwd('/'+strings):
                    return 1
            elif self.ftp2 and self.ftp2.cwd('/'+strings):
                return 1
            else:
                return 0
        except:
            return 0

    #定义登录下下载文件的函数,固定设置存储文件夹在桌面的FTP_Server文件夹中
    def download(self,remotepath):
        try:
            str1 = re.findall(r'[^/:*?"<>|\r\n]+$', remotepath)
            str2=str(self.from_file_getPath('file_path')).replace('/','\\')
            path=str2+'\\'+str(str1[0]).replace('\\','-')
            if self.ftp:
                buffersize = 102400
                fp= open(path,'wb')
                self.ftp.retrbinary('RETR '+str1[0],fp.write,buffersize)
                return 1
            elif self.ftp2:
                buffersize2 = 102400
                fp2 =open(path,'wb')
                self.ftp2.retrbinary('RETR '+str1[0],fp2.write,buffersize2)
                return 1
            else:
                return 0
        except Exception as e:
            print(str(e))

    #定义登录下上传文件的函数
    def upload(self,remotepath,localpath):
        try:
            #print(remotepath)
            str1= re.findall(r'[^/:*?"<>|\r\n]+$',remotepath)
            #print(str1)
            if self.ftp:
                self.ftp.cwd('/')
                fp = open(localpath,'rb')
                self.ftp.storbinary("STOR "+str1[0],fp)
                return 1
            elif self.ftp2:
                self.ftp2.cwd('/')
                fp2 = open(localpath,'rb')
                self.ftp2.storbinary("STOR "+str1[0],fp2)
                return 1
            else:
                return 0
        except Exception as e:
            print(str(e))
