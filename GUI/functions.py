# import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class MotorControl: 

    def __init__(self, Azimuth, Elevation, userAzi = 0, userEle = 0, Azi_bound = [0,360], Ele_bound = [0,180] ): 
        self.Azimuth = Azimuth
        self.Elevation = Elevation
        self.userAzi = userAzi
        self.userEle = userEle
        self.Azi_bound = Azi_bound
        self.Ele_bound = Ele_bound
        self.homeAzi = 0
        self.homeEle = 90
        self.breakCommand = 'jog off x y'
        self.port = ''
        self.ser = serial.Serial()
        self.portConnection() 

# check input type, if both 
    def readinput( self ):
        #  branck set to be current value
        if self.userAzi == "":
            self.userAzi = self.Azimuth
        if self.userEle == "":
            self.userEle = self.Elevation

        # digit -> check range / not digit -> error pop up
        elif ((self.userAzi).isdigit()) and ((self.userEle).isdigit()):
           self.checkrange()
        else : 
            self.InputTypeErrorPopup()

# chack range of input , popup error message if inout is out of range
    def checkrange( self ): 
        isInRange = True
        self.IntUserAzi = int(self.userAzi)
        self.IntUserEle = int(self.userEle)

        if self.IntUserAzi < self.Azi_bound[0] or self.IntUserAzi > self.Azi_bound[1]:
            isInRange = False
        if self.IntUserEle < self.Ele_bound[0] or self.IntUserEle > self.Ele_bound[1]:
            isInRange = False

        # move antenna / error popup window
        if isInRange:
            try:
                self.moveAntenna()
            except: 
                messagebox.showwarning( title = "commanderror" , message = "Failed to connect" )
        else: 
            self.RangeErrorPopup()

    
    def InputTypeErrorPopup( self ):
        messagebox.showwarning( title= "Inout Error" , message= "Input must be numbers")

    def RangeErrorPopup( self ):
        range = "Azimuth: " + str(self.Azi_bound[0]) + "-" + str(self.Azi_bound[1]) + "\n" + "Elevation: " +  str(self.Ele_bound[0]) + "-" + str(self.Ele_bound[1])
        messagebox.showwarning( title= "Range error", message= "Input must be in range \n" + range ) 

    def moveAntenna( self ):

        commandY = 'jog abs y '
        self.ser.write( commandY.encode('utf-8'))
        line2 = self.ser.readline()
        data2 = line2.decode('utf-8')
        print( data2 ) 

        self.Azimuth = self.userAzi
        self.Elevation = self.userEle
        print ( "position updated")

    def motorErrorMessage( self ):
        msg = self.ser.readline()
        if msg.decode('utf-8') != "": 
            return msg.decode('utf-8')

    def portConnection( self ):

        if self.port != '':
            # print( "port was changed to " + self.port)
            if self.ser.isOpen():
                self.ser.close()

            try:    
                self.ser = serial.Serial(port= str( self.port ), baudrate=9600 )
            except:
                 messagebox.showerror( title = "Port Open Error", message = "Failed to open port connection")    

    def EmargencyStop( self ):
        try:
            self.ser.write( self.breakCommand.encode('utf-8') ) 
            eline = self.ser.readline()
            edata = eline.decode('utf-8')
            print( edata ) 
        except:
            messagebox.showerror( title="Emargency Stop Error", message= "failed to stop")


    def MotorSetting( self ):
        settingWindow = tk.Tk()
        settingWindow.geometry('400x200')
        settingWindow.title('MotorSetting')

        # home is 1x2 (azimuth, elevation)
        home = []
        # bounds is 2x2 (lower and upper bound for each direction)
        bounds = []
      
        frame = tk.Frame( settingWindow )
        currName = tk.Label( frame, text = "Curent Default" )
        newName = tk.Label( frame, text = "New Default" )
        currAzi = tk.Label( frame, text = str( self.homeAzi ))
        currEle = tk.Label( frame, text = str( self.homeEle ))
        labelAzi = tk.Label( frame, text = "Azimuth ")
        labelEle = tk.Label( frame, text = " Elevatin ")
        newhomeAzi = tk.Entry( frame, width = 10 )
        newhomeEle = tk.Entry( frame, width = 10 )

        currName.grid(row = 0, column = 1, padx = 5, pady = 5)
        newName.grid(row = 0, column = 2, padx = 5, pady = 5)
        
        labelAzi.grid(row = 1, column = 0, padx = 5, pady = 5)
        currAzi.grid(row = 1, column = 1, padx = 5, pady = 5)
        newhomeAzi.grid(row = 1, column = 2, padx = 5, pady = 5)

        labelEle.grid(row = 2, column = 0, padx = 5, pady = 5)
        currEle.grid(row = 2, column = 1, padx = 5, pady = 5)
        newhomeEle.grid(row = 2, column = 2, padx = 5, pady = 5)
        frame.pack()

        enterButton = tk.Button( settingWindow, text = "Enter", command = self.updateValues )
        enterButton.pack()
        settingWindow.mainloop()

        # home = [newhomeAzi.get(),newhomeEle.get()]
    
    def updateValues( self ):
        try:
            self.homeAzi = self.MotorSetting.newhomeAzi.get()
            # self.homeAzi = self.MotorSetting[0]
            # self.homeEle = self.MotorSetting[1]
            print( self.homeAzi , self.homeEle )
        except: 
            messagebox.showwarning( title = "Default update error", message= "Failed to update default value" )
        

class Newwindow():
    def __init__(self):
 
        self.root = tk.Tk()
        self.root.geometry('500x300')
        self.root.title('DFS-control')

         # create motor from class "Motorcontrol"
        self.motor = MotorControl( 0 , 90 )
        
        # box for asi ele information 
        self.positions = tk.LabelFrame( self.root, text = "Antenna Position" )
        self.positions.grid( row = 1, column = 0 , padx = 20 , pady = 10)
        self.quickButton = tk.Frame( self.root  )
        self.quickButton.grid( row = 1, column= 1 , padx = 20 , pady = 10)

        # port selection
        ports = list( serial.tools.list_ports.comports() ) 
        self.port_selection = ttk.Combobox( self.root , values = ports )
        self.port_selection.grid(row = 0, column= 0 , padx = 20 , pady = 10)

        # emargency stop button creation
        self.EmargencyStop = tk.Button( self.quickButton, text = "Emargency Stop", font = ('Arial', 16 ) , bg = 'red', fg = 'white' , command= self.Estop )
        self.EmargencyStop.pack()

        # park button creation
        self.Park = tk.Button( self.quickButton, text = "Park", font = ('Arial', 16) , bg = 'blue', fg = 'white' , command = self.park )
        self.Park.pack( pady = 10 )

        # azi,ele input boxes creation
        self.boxFrame = tk.Frame( self.positions )
        self.boxFrame.pack( pady = 10)

        # show motor setting button creation
        self.motorSettingButton = tk.Button( self.quickButton , text = "Motor Setting", font = ('Arial', 16 ), command = self.motor.MotorSetting )
        self.motorSettingButton.pack( pady = 10)


        # motorMessage = self.motor.motorErrorMessage() 
        # if motorMessage != "":
        #     messagebox.showinfo( title = "Message from Motor Controller ", message= motorMessage )


        self.azimuth_label = tk.Label( self.boxFrame , text = "Azimuth" )
        self.elevation_label = tk.Label( self.boxFrame , text = "Elevation")
        # self.current_azimuth = tk.Label( self.boxFrame, text = self.motor.Azimuth )
        # self.current_elevation = tk.Label( self.boxFrame, text = self.motor.Elevation )
        self.inputAzimuth = tk.Entry( self.boxFrame, width= 10 )
        self.inputElevation = tk.Entry( self.boxFrame, width= 10 )

        self.azimuth_label.grid( row = 0, column = 0 )
        self.elevation_label.grid( row = 1, column = 0 )
        # self.current_azimuth.grid( row = 0, column = 1, padx = 10 )
        # self.current_elevation.grid( row = 1, column = 1, padx = 10 )
        self.inputAzimuth.grid( row = 0, column = 2, padx = 5 )
        self.inputElevation.grid( row = 1, column = 2, padx = 5 )

        # enter button creation
        self.printbutton = tk.Button( self.positions, text = "Enter", command = self.input )
        self.printbutton.pack( padx = 20, pady = 10, side = tk.LEFT )

        self.root.mainloop()

    def Estop(self):
         # change port if current port is different from user input 
        if self.motor.port != self.port_selection.get()[:4]: 
            portName = self.port_selection.get()
            self.motor.port = portName[:4]
            self.motor.portConnection()
        # send serial command to stop moving antenna (JOG OFF)
        self.motor.EmargencyStop()
    
    def park( self ):
        print( "Park antenna to default position" )
        # send serial command to move antenna to home ( JOG HOME / JOG abs x 0 & JOG abs y 0 )
        # set default parameter 
        self.motor.userAzi = "0"
        self.motor.userEle = "0"
        # self.motor.readinput()


    def input(self):

    # change port if current port is different from user input 
        if self.motor.port != self.port_selection.get()[:4]: 
            portName = self.port_selection.get()
            self.motor.port = portName[:4]
            self.motor.portConnection()

        # update user value in motor class
        self.motor.userAzi = self.inputAzimuth.get()
        self.motor.userEle = self.inputElevation.get()
        self.motor.readinput()      


    def quit(self):
        self.root.destroy()


