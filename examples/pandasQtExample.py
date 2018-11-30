import numpy as np
import pandas as pd
from pandas.sandbox.qtpandas import DataFrameModel, DataFrameWidget
from PySide import QtGui, QtCore

# Or if you use PyQt4:
# from PyQt4 import QtGui, QtCore

class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.widget = DataFrameWidget(pd.DataFrame([]))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.widget)
        self.setLayout(vbox)


if __name__ == '__main__':
    import sys
    
    df = pd.DataFrame(
        np.arange(9).reshape(3, 3),
        columns=['foo', 'bar', 'baz']
    )
    # Initialize the application
    app = QtGui.QApplication(sys.argv)
    mw = MainWidget()
    mw.widget.setDataFrame(df)
    mw.show()
    app.exec_()

    df.