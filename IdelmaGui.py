from IdelmaMainWin import IdelmaMainWin
from PxlMetaDataQTableWidgetItem import PxlMetaDataQTableWidgetItem


class IdelmaGui(IdelmaMainWin):
    """
    DESCRIPTION
    """
    def __init__(self):
        super().__init__()

        self.setTableWidget()
        self.disableBrdProgBttns()
        self.disableListWidgetBttns()

    def setTableWidget(self):
        self.pxlsMapTable.setColumnCount(len(PxlMetaDataQTableWidgetItem.columnLabels))
        self.pxlsMapTable.setHorizontalHeaderLabels(PxlMetaDataQTableWidgetItem.columnLabels)
        # self.pxlsMapTable.setRowCount(5)
        # self.pxlsMapTable.setVerticalHeaderLabels(['1', '1', '1', '1', '1'])

    def enableListWidgetBttns(self):
        self.sctDeleteButton.setEnabled(True)
        self.sctEditButton.setEnabled(True)

    def disableListWidgetBttns(self):
        self.sctDeleteButton.setEnabled(False)
        self.sctEditButton.setEnabled(False)

    def disableBrdProgBttns(self):
        self.configButton.setEnabled(False)
        self.saveButton.setEnabled(False)

    def updtSnNumLabel(self, text: str):
        self.snNumberLabel.setText(text)

    def updtFwVerLabel(self, text: str):
        self.fwVerLabel.setText(text)

    def updtSctsInfo(self, text: str):
        self.sctsLabel.setText(text)

    def updtPxlsInfo(self, text: str):
        self.pxlsLabel.setText(text)
