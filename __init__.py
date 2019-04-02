from 主页 import *
import sys


if  __name__ =='__main__':
    app = QApplication(sys.argv)
    ui = zhuye()
    ui.show()
    sys.exit(app.exec_())  # 系统退出