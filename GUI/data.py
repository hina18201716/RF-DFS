class DataManagement():
    '''this class contain functions to manage data logging and updating'''
    dataList    = [] # list of data
    data        = [] # date, azimuth, elevation 

    def __init__( self, userData ):
        self.dataList = [userData]

    def addNewData( self, date, azimuth, elevation ):
        userData = [date, azimuth, elevation]
        self.dataList.append( userData )

    def add( self, newData ):
        self.dataList.append(newData)

    def delete( self, oldData ):
        self.dataList.remove(oldData)

    def __str__( self ):
        """"print all information"""
        return 

