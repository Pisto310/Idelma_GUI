import sys
from IdelmaApp import *


def bootApp():
    app = IdelmaApp(sys.argv)

    """-----     debug    -----"""
    app.fetchBrdInfosCmd()

    app.sectionCreation('First', 15, False)
    app.configBrdBttnStateTrig()

    app.sectionCreation('Next', 8, False)
    app.configBrdBttnStateTrig()

    app.sectionCreation('Section 2', 20, True)
    app.configBrdBttnStateTrig()
    """-----     debug    -----"""

    sys.exit(app.exec_())


if __name__ == '__main__':
    bootApp()
