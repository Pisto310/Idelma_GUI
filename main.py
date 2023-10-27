import sys
from IdelmaApp import *


def bootApp():
    app = IdelmaApp(sys.argv)

    """-----     debug    -----"""
    # app.fetchBrdMetaDatasCmd()
    #
    # app.sectionCreation(0, 5, 'First', False)
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(1, 2, 'Next', False)
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(2, 4, 'Section 2', True)
    # app.configBrdBttnStateTrig()
    """-----     debug    -----"""

    sys.exit(app.exec_())


if __name__ == '__main__':
    bootApp()
