import sys
from IdelmaApp import *


def bootApp():
    app = IdelmaApp(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':

    bootApp()
