import sys
from IdelmaApp import *
from SctMetaData import SctMetaData
from NonSerSctMetaDataQListWidgetItem import NonSerSctMetaDataQListWidgetItem


def bootApp():
    app = IdelmaApp(sys.argv)

    """-----     debug    -----"""
    # app.fetchBrdMetaDatasCmd()

    # app.newSectionDialog(SctMetaData(0, 3, 76, 1), NonSerSctMetaDataQListWidgetItem('First'))
    # app.newSectionDialog(SctMetaData(1, 6, 168, 0), NonSerSctMetaDataQListWidgetItem(''))
    # app.newSectionDialog(SctMetaData(2, 2, 29, 0), NonSerSctMetaDataQListWidgetItem('Name'))
    # app.newSectionDialog(SctMetaData(3, 5, 216, 1), NonSerSctMetaDataQListWidgetItem(''))
    # app.newSectionDialog(SctMetaData(4, 6, 125, 0), NonSerSctMetaDataQListWidgetItem('Subsequent'))
    # app.newSectionDialog(SctMetaData(5, 1, 193, 0), NonSerSctMetaDataQListWidgetItem('Tempus Fugit'))
    # app.newSectionDialog(SctMetaData(6, 4, 67, 1), NonSerSctMetaDataQListWidgetItem('Final'))
    """-----     debug    -----"""

    sys.exit(app.exec_())


if __name__ == '__main__':
    bootApp()
