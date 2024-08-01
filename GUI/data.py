from functools import reduce
 
class DataManagement():
    '''this class contain functions to manage data logging and updating'''
    dataList    = [] # list of data
    data        = [] # time, azimuth, elevation 
    delim = '\t'

    def add( self, newData ):
        self.dataList.append(newData)

    def delete( self, oldData ):
        self.dataList.remove(oldData)
    
    def printData(self):
        filename = str(self.dataList[0][0])+ ".txt"
        with open( filename , 'w') as f:
           for vec in self.dataList:
             line = reduce(lambda x,y : str(x) + self.delim + str(y), vec)
             print(line)
             f.write(line)
             f.write("\n")   

######## example ##########################            
user = DataManagement()
user.add(['august1st', 00, 00 ])
user.add(['august1st', 10, 00 ])
user.add(['august1st', 20, 00 ])
user.add(['august1st', 30, 00 ])
user.printData()
#############################################

