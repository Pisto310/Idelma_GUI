import sys
from IdelmaApp import *


def bootApp():
    app = IdelmaApp(sys.argv)

    """-----     debug    -----"""
    app.fetchBrdInfosCmd()

    app.sectionCreation('First', 5, False)
    app.configBrdBttnStateTrig()

    app.sectionCreation('Next', 2, False)
    app.configBrdBttnStateTrig()

    app.sectionCreation('Section 2', 6, True)
    app.configBrdBttnStateTrig()
    """-----     debug    -----"""

    sys.exit(app.exec_())


if __name__ == '__main__':
    bootApp()
