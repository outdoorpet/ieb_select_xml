from PyQt4 import QtGui
from obspy.clients.fdsn import Client
from obspy.core.event import Catalog
from obspy.clients.fdsn.header import FDSNException
import pandas as pd
import os


class MainWindow(QtGui.QWidget):
    """
    Main Window for metadata map GUI
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()

    def setupUi(self):
        open_ieb_button = QtGui.QPushButton('Open IEB Output', self)
        open_ieb_button.released.connect(self.open_ieb)
        open_ieb_button.resize(open_ieb_button.sizeHint())
        open_ieb_button.move(50,50)

        self.setGeometry(300, 300, 250, 150)


    def open_ieb(self):
        self.ieb_filename = str(QtGui.QFileDialog.getOpenFileName(
            parent=self, caption="Choose File",
            directory=os.path.expanduser("~"),
            filter="Text Files (*.txt)"))
        if not self.ieb_filename:
            return

        # open the text file containing earthquakes with pandas
        self.ieb_events = pd.read_table(self.ieb_filename, header=0)

        print(self.ieb_events)

        self.make_xml()

    def make_xml(self):
        client = Client("IRIS")
        cat = Catalog() # empty earthquake catalogue
        print('')

        # Method to retrieve events from IRIS based on event ID and create an xml file
        for event_id in self.ieb_events['IRIS ID']:
            try:
                print('Requesting Information for event: '+ str(event_id))
                IRIS_event = client.get_events(eventid=int(event_id))[0]
                cat.append(IRIS_event)
            except FDSNException:
                print('')
                print('Error!!: No Event Information for '+ str(event_id))


        print('')
        print("Resulting Earthquake Catalogue:")
        print(cat)
        new_filename = os.path.splitext(self.ieb_filename)[0]+'.xml'
        cat.write(filename=new_filename, format="QUAKEML")





if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = MainWindow()
    w.raise_()
    app.exec_()