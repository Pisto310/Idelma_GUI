import sys
from IdelmaApp import *
from SctMetaData import SctMetaData
from NonSerSctMetaDataQListWidgetItem import NonSerSctMetaDataQListWidgetItem


def bootApp():
    app = IdelmaApp(sys.argv)

    """-----     debug    -----"""
    app.fetchBrdMetaDatasCmd()

    # app.sectionCreation(SctMetaData(0, 3, 76, 1), NonSerSctMetaDataQListWidgetItem('First'))
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(SctMetaData(1, 6, 168, 0), NonSerSctMetaDataQListWidgetItem('Section 1'))
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(SctMetaData(2, 2, 29, 0), NonSerSctMetaDataQListWidgetItem('Name'))
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(SctMetaData(3, 5, 216, 1), NonSerSctMetaDataQListWidgetItem('Section 3'))
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(SctMetaData(4, 6, 125, 0), NonSerSctMetaData('Subsequent'))
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(SctMetaData(5, 1, 193, 0), NonSerSctMetaData('Tempus Fugit'))
    # app.configBrdBttnStateTrig()
    #
    # app.sectionCreation(SctMetaData(6, 4, 67, 1), NonSerSctMetaData('Final'))
    # app.configBrdBttnStateTrig()
    """-----     debug    -----"""

    sys.exit(app.exec_())


if __name__ == '__main__':
    bootApp()
