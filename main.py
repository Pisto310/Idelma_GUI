import sys
from IdelmaApp import *
from SctMetaData import SctMetaData
from NonSerSctMetaData import NonSerSctMetaData


def bootApp():
    app = IdelmaApp(sys.argv)

    """-----     debug    -----"""
    app.fetchBrdMetaDatasCmd()

    app.sectionCreation(SctMetaData(0, 14, 76, 1), NonSerSctMetaData('First'))
    app.configBrdBttnStateTrig()

    app.sectionCreation(SctMetaData(1, 23, 168, 0), NonSerSctMetaData('Section 1'))
    app.configBrdBttnStateTrig()

    app.sectionCreation(SctMetaData(2, 6, 29, 0), NonSerSctMetaData('Name'))
    app.configBrdBttnStateTrig()

    app.sectionCreation(SctMetaData(3, 35, 216, 1), NonSerSctMetaData('Section 3'))
    app.configBrdBttnStateTrig()
    """-----     debug    -----"""

    sys.exit(app.exec_())


if __name__ == '__main__':
    bootApp()
