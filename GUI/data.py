from functools import reduce
import os.path
 
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
        done = False
        try:
            filename = str(self.dataList[0][0])[0:10]+ ".txt"
        except:
            print("No data to output")
            done = True

        if done is False:
            if os.path.isfile( filename ):
                print( "Updating a File ... " )     
                with open( filename , 'a' ) as f: 
                    for vec in self.dataList:
                        line = reduce(lambda x,y : str(x) + self.delim + str(y), vec)
                        f.write(line)
                        f.write("\n")   
            else: 
                print( "Making File ... " ) 
                with open( filename , 'w' ) as f:
                    for vec in self.dataList:
                        line = reduce(lambda x,y : str(x) + self.delim + str(y), vec)
                        f.write(line)
                        f.write("\n")   
            
            self.dataList = []


######## example ##########################            
# user = DataManagement()
# user.add(['august1st', 00, 00 ])
# user.add(['august1st', 10, 00 ])
# user.add(['august1st', 20, 00 ])
# user.add(['august1st', 30, 00 ])
# user.printData()

# user.add(['august1st', 40, 00 ])
# user.add(['august1st', 50, 00 ])
# user.add(['august1st', 60, 00 ])
# user.printData()

#############################################

