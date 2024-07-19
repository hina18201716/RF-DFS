# import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import time
import pyvisa as visa
# from tkinter import tix
import astropy

# CONSTANTS
RETURN_ERROR = 1
RETURN_SUCCESS = 0

class MotorControl: 
 
    def __init__(self, Azimuth, Elevation, userAzi = 0, userEle = 0, Azi_bound = [0,360], Ele_bound = [-90,20] ): 
        self.Azimuth    = Azimuth
        self.Elevation  = Elevation
        self.userAzi    = userAzi
        self.userEle    = userEle
        self.Azi_bound  = Azi_bound
        self.Ele_bound  = Ele_bound
        self.homeAzi    = 0
        self.homeEle    = 0
        self.port       = ''
        self.ser        = serial.Serial()
        self.OpenSerial()

        # commands 
        self.commandToSend  = ""
        self.breakCommand   = 'jog off x y' 
        self.commandGen     = 'jog abs'
        self.moveCommandX   = 'jog abs x ' 
        self.moveCommandY   = 'jog abs y '
        self.startCommand   = ['Prog 0', 'drive on x y']

        # error type
        self.errorType          = "" 
        self.errorMsg           = ""
        self.rangeError         = ["Range Error", "Input is out of Range \n Range: "]
        self.inputTypeError     = ["Input Type Error", "Inputs must be integers"]
        self.connectionError    = ["Connection Error", "Failed to connect/send command to controller"]
        self.eStopError         = ["Emargency Stop Error", "Failed to stop motor"]

    def errorPopup( self ):
        """Generate Error pop up window.
        """
        messagebox.showwarning( title= self.errorType , message= self.errorMsg )

    def sendCommand( self , command ):
        """Serial Communication, write in serial. Error pop up if fails. 
        """
        try: 
            
            # time.sleep(1)
            self.ser.write( str(command).encode('utf-8'))
            # time.sleep(1)
            self.readLine()
            # time.sleep(1)

            print("command sent \n")
        except:
            
            self.errorType = self.connectionError[0]
            self.errorMsg = self.connectionError[1]
            self.errorPopup()


    def readLine( self ):
        """Serial Commmunication, read until End Of Line charactor
        """
        msg = self.ser.readline()
        # message = msg.decode('utf-8') 
        print(msg)
        
    def is_convertible_to_integer(self, input_str):
        """
        Check if given string is convertivle to integer. (Positive int, Negative int, Zero) 

        Returns:
            True: String is convetible to integer
            False: String is not convertible to integer. 
        """
        try:
            int(input_str)
            return True
        except:
            return False
        

    def readUserInput( self ):
        """Check if both inputs are integers/NULL string. 
        Convert NULL string to current position values.
        If both inputs are integers/NULL string, call chechrange functioon, otherwise, error pop up. 
        """
        if self.userAzi == "":
            self.userAzi = str ( self.Azimuth )
        if self.userEle == "":
            self.userEle = str( self.Elevation )
        elif (self.is_convertible_to_integer(self.userAzi)) and (self.is_convertible_to_integer(self.userEle)):
            self.checkrange()
        else : 
            self.errorType = self.inputTypeError[0]
            self.errorMsg = self.inputTypeError[1]
            self.errorPopup()

    def checkrange( self ): 
        """Check if input value(s) are in range. Send command if both in range, error pop up if not. 
        """
        isInRange = True
        self.IntUserAzi = int(self.userAzi)
        self.IntUserEle = int(self.userEle)

        if self.IntUserAzi < self.Azi_bound[0] or self.IntUserAzi > self.Azi_bound[1]:
            isInRange = False
        if self.IntUserEle < self.Ele_bound[0] or self.IntUserEle > self.Ele_bound[1]:
            isInRange = False
        if isInRange:
            # self.commandToSend= self.moveCommandX + self.userAzi 
            # self.nextCommand = self.moveCommandY + self.userEle
            # self.commandToSend = self.commandGen + " x " + self.userAzi + " y " + self.userEle 
            self.sendCommand( self.commandGen + " x " + self.userAzi + " y " + self.userEle  )
            self.Azimuth = self.userAzi
            self.Elevation = self.userEle
        else: 
            self.errorType = self.rangeError[0]
            self.errorMsg = self.rangeError[1] + "Azimuth: " + str(self.Azi_bound[0]) + "-" + str(self.Azi_bound[1]) + "\n" + "Elevation: " +  str(self.Ele_bound[0]) + "-" + str(self.Ele_bound[1])
            self.errorPopup()
   
    def OpenSerial( self ):
        """Open new serial connection
        """
        if self.port != '':
           
            if self.ser.is_open:
                self.ser.close()
            try:    
                self.ser = serial.Serial(port= self.port, baudrate=9600 , bytesize= 8, parity='N', stopbits=1,xonxoff=0)
                time.sleep(1)
                # self.ser.write("\n")
                # self.ser.write( self.startCommand[0] )
                # # if self.readLine() = 
                # self.ser.write( self.startCommand[1] )
                # self.ser.write( "\n" ) 
                print( "communication to motor controller is ready" )
            except:
                 self.errorType = self.connectionError[0]
                 self.errorMsg = self.connectionError[1]
                 self.errorPopup()


    def CloseSerial( self ):
        if not(self.ser.is_open):
            self.sendCommand( '' )
            self.ser.close()


    def EmargencyStop( self ):
        self.commandToSend = self.breakCommand
        self.sendCommand( "jog off x y" )
     
    def Park( self ):
        # self.commandToSend = self.commandGen + " x " + str( self.homeAzi ) + " y " + str( self.homeEle )
        self.sendCommand( self.commandGen + " x " + str( self.homeAzi ) + " y " + str( self.homeEle ) )
    

    def freeInput( self ):
        def ReadandSend():

            line = inBox.get()
            self.sendCommand( line )
            update_text()
        
        def update_text(): 
            try:
                line = self.ser.readline()
                if line.decode != '':
                    self.returnLineBox.config(text = line.decode)
            except:
                self.errorType = self.connectionError[0]
                self.errorMsg = self.connectionError[1]
                self.errorPopup()

        freeWriting = tk.Tk() 
        freeWriting.title("Serial Communication")

        outputFrame     = tk.Frame( freeWriting )
        inputFrame      = tk.Frame( freeWriting )
        labelInput      = tk.Label( inputFrame, text= "Type Input: ")
        inBox           = tk.Entry( inputFrame , width= 50 )
        enterButton     = tk.Button( inputFrame , text = "Enter" , command = ReadandSend )
        self.returnLineBox   = tk.Label( outputFrame )

        labelInput.pack( padx = 10, pady = 5 )
        inBox.pack( side = 'left', padx = 10, pady = 5 )
        enterButton.pack( side = 'right' ,padx = 10, pady = 5)
        self.returnLineBox.pack( padx = 10, pady = 5 )

        freeWriting.after(1000, update_text)
        freeWriting.mainloop()
        
        
#######################################################################################################################################
    # def MotorSetting( self ):
    #     settingWindow = tk.Tk()
    #     settingWindow.geometry('400x200')
    #     settingWindow.title('MotorSetting')

    #     # home is 1x2 (azimuth, elevation)
    #     home = []
    #     # bounds is 2x2 (lower and upper bound for each direction)
    #     bounds = []
      
    #     frame = tk.Frame( settingWindow )
    #     currName = tk.Label( frame, text = "Curent Default" )
    #     newName = tk.Label( frame, text = "New Default" )
    #     currAzi = tk.Label( frame, text = str( self.homeAzi ))
    #     currEle = tk.Label( frame, text = str( self.homeEle ))
    #     labelAzi = tk.Label( frame, text = "Azimuth ")
    #     labelEle = tk.Label( frame, text = " Elevatin ")
    #     newhomeAzi = tk.Entry( frame, width = 10 )
    #     newhomeEle = tk.Entry( frame, width = 10 )

    #     currName.grid(row = 0, column = 1, padx = 5, pady = 5)
    #     newName.grid(row = 0, column = 2, padx = 5, pady = 5)
        
    #     labelAzi.grid(row = 1, column = 0, padx = 5, pady = 5)
    #     currAzi.grid(row = 1, column = 1, padx = 5, pady = 5)
    #     newhomeAzi.grid(row = 1, column = 2, padx = 5, pady = 5)

    #     labelEle.grid(row = 2, column = 0, padx = 5, pady = 5)
    #     currEle.grid(row = 2, column = 1, padx = 5, pady = 5)
    #     newhomeEle.grid(row = 2, column = 2, padx = 5, pady = 5)
    #     frame.pack()

    #     enterButton = tk.Button( settingWindow, text = "Enter", command = self.updateValues )
    #     enterButton.pack()
    #     settingWindow.mainloop()

    #     # home = [newhomeAzi.get(),newhomeEle.get()]
    
    # def updateValues( self ):
    #     try:
    #         self.homeAzi = self.MotorSetting.newhomeAzi.get()
    #         # self.homeAzi = self.MotorSetting[0]
    #         # self.homeEle = self.MotorSetting[1]
    #         print( self.homeAzi , self.homeEle )
    #     except: 
    #         messagebox.showwarning( title = "Default update error", message= "Failed to update default value" )
        
########################################################################################################################################
class VisaControl():
    def __init__(self):
        self.instr = ''

    def openRsrcManager(self):
        """Opens the VISA resource manager on the default backend (NI-VISA). If the VISA library cannot be found, a path must be passed to pyvisa.highlevel.ResourceManager() constructor

        Returns:
            0: On success
            1: On error
        """
        print('Initializing VISA Resource Manager...')
        self.rm = visa.ResourceManager()
        if self.isError():
            print('Could not open a session to the resource manager, error code:', hex(self.rm.last_status))
            return RETURN_ERROR     
        return RETURN_SUCCESS
    
    def connectToRsrc(self):
        """Opens a session to the resource ID located in self.instr

        Returns:
            0: On success
            1: On error
        """
        if self.instr != '':
            print('Connecting to resource: ' + self.instr)
            viConnected = self.rm.open_resource(self.instr)
            if self.isError():
                print('Could not open a session to ' + self.instr)
                print('Error Code:' + self.rm.last_status)
                return RETURN_ERROR
            return RETURN_SUCCESS
        
    def isError(self):
        """Checks the last status code returned from an operation at the opened resource manager (self.rm)

        Returns:
            0: On success or warning (Operation succeeded)
            1: On error
        """
        if self.rm.last_status < 0:
            return RETURN_ERROR
        else:
            print('Success code:', hex(self.rm.last_status))
            return RETURN_SUCCESS

class FrontEnd():
    def __init__(self):
        """Initializes the top level tkinter interface
        """
        self.root = tk.Tk()
        self.root.title('DFS-control')

        tabControl = ttk.Notebook(self.root) 
  
        self.tab1 = ttk.Frame(tabControl) 
        self.tab2 = ttk.Frame(tabControl) 

        tabControl.add(self.tab1, text ='Tab 1') 
        tabControl.add(self.tab2, text ='Tab 2') 
        tabControl.pack(expand = 1, fill ="both") 

        self.serialInterface()
        # self.scpiInterface()
        # self.PythonInterface()
        self.root.after(1000, self.update_time )
        self.root.mainloop()

    def scpiInterface(self):
        """Generates the SCPI communication interface on the developer's tab of choice at tabSelect
        """

        tabSelect = self.tab2           # Select which tab this interface should be placed
        vi = VisaControl()
        vi.openRsrcManager()
        instruments = vi.rm.list_resources()

        # Instrument selection panel
        ttk.Label(tabSelect, text = "Select a SCPI instrument:", 
          font = ("Times New Roman", 10)).grid(column = 0, 
          row = 0, padx = 10, pady = 25) 
        def updateInstruments():
            instruments = vi.rm.list_resources()
        self.instrSelection = ttk.Combobox(tabSelect, values = instruments, width=60, postcommand = lambda:updateInstruments())
        self.instrSelection.grid(row = 0, column = 1, padx = 20 , pady = 10)
        self.selectButton = tk.Button(tabSelect, text = "Confirm", command = lambda:print(self.instSelection.get()))
        self.selectButton.grid(row = 0, column = 3)

        # Check if the current instrument ID is equivalent to the string in the combobox instrSelection
        if vi.instr != self.instrSelection.get():     
            vi.instr = self.instrSelection.get()
            vi.connectToRsrc()
    
    # def PythonInterface( self ):
    #     """Generates the python console window 
    #     """ 
    #     pyWindow = tix.Tk()
    #     pyWindow.mainloop()

    def serialInterface(self):
        """Generates the serial communication interface on the developer's tab of choice at tabSelect
        """

        tabSelect = self.tab1   # Select which tab this interface should be placed

        # create motor from class "Motorcontrol"
        self.motor = MotorControl( 0 , 0 )
        
        # port selection
        ports                   = list( serial.tools.list_ports.comports() ) 
        self.port_selection     = ttk.Combobox( tabSelect , values = ports )
        self.port_selection.grid(row = 0, column= 0 , padx = 20 , pady = 10)

        # time label 
        self.clock_label = tk.Label( tabSelect, font= ('Arial', 14))
        self.clock_label.grid( row= 0, column= 1, padx = 20 , pady = 10 )

        # box for asi ele information 
        self.positions      = tk.LabelFrame( tabSelect, text = "Antenna Position" )
        self.quickButton    = tk.Frame( tabSelect )
        self.positions.grid( row = 1, column = 0 , padx = 20 , pady = 10)
        self.quickButton.grid( row = 1, column= 1 , padx = 20 , pady = 10)


        # buttons : estop, park, free writing window, close
        self.EmargencyStop      = tk.Button( self.quickButton, text = "Emargency Stop", font = ('Arial', 16 ) , bg = 'red', fg = 'white' , command= self.Estop )
        self.Park               = tk.Button( self.quickButton, text = "Park", font = ('Arial', 16) , bg = 'blue', fg = 'white' , command = self.park )
        self.openFreeWriting    = tk.Button( self.quickButton, text = "Open Free Writing" ,font = ('Arial', 16 ), command= self.freewriting )
        # self.motorSettingButton = tk.Button( self.quickButton , text = "Motor Setting", font = ('Arial', 16 ), command = self.motor.MotorSetting )
        self.close              = tk.Button( self.quickButton, text = "Close window",font = ('Arial', 16 ), command = self.closeWin )
        
        self.EmargencyStop.pack()
        self.Park.pack( pady = 10 )
        self.openFreeWriting.pack( pady = 10 )
        # self.motorSettingButton.pack( pady = 10)
        self.close.pack( pady = 20 )

        # azi,ele input boxes creation
        self.boxFrame           = tk.Frame( self.positions )
        self.boxFrame.pack( pady = 10)

        self.azimuth_label      = tk.Label( self.boxFrame , text = "Azimuth" )
        self.elevation_label    = tk.Label( self.boxFrame , text = "Elevation")
        # self.current_azimuth = tk.Label( self.boxFrame, text = self.motor.Azimuth )
        # self.current_elevation = tk.Label( self.boxFrame, text = self.motor.Elevation )
        self.inputAzimuth       = tk.Entry( self.boxFrame, width= 10 )
        self.inputElevation     = tk.Entry( self.boxFrame, width= 10 )

        self.azimuth_label.grid( row = 0, column = 0, padx = 10 )
        self.elevation_label.grid( row = 1, column = 0, padx = 10 )
        # self.current_azimuth.grid( row = 0, column = 1, padx = 10 )
        # self.current_elevation.grid( row = 1, column = 1, padx = 10 )
        self.inputAzimuth.grid( row = 0, column = 2, padx = 10 )
        self.inputElevation.grid( row = 1, column = 2, padx = 10 )

        # enter button creation
        self.printbutton        = tk.Button( self.positions, text = "Enter", command = self.input )
        self.printbutton.pack( padx = 20, pady = 10, side = 'right' )

    def update_time( self ):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_time)


    def closeWin( self ):
        self.motor.CloseSerial()
        self.root.destroy()


    def freewriting(self):
        """Frexible serial communication Window
        """
        if self.motor.port != self.port_selection.get()[:4]: 
            portName = self.port_selection.get()
            self.motor.port = portName[:4]
            self.motor.OpenSerial()

        self.motor.freeInput()

    def Estop(self):
        
        if self.motor.port != self.port_selection.get()[:4]: 
            portName = self.port_selection.get()
            self.motor.port = portName[:4]
            self.motor.OpenSerial()
       
        self.motor.EmargencyStop()
    
    def park( self ):
        if self.motor.port != self.port_selection.get()[:4]: 
            portName = self.port_selection.get()
            self.motor.port = portName[:4]
            self.motor.OpenSerial()
        self.motor.Park()

    def input(self):
    
        if self.motor.port != self.port_selection.get()[:4]: 
            portName = self.port_selection.get()
            self.motor.port = portName[:4]
            self.motor.OpenSerial()

        self.motor.userAzi = self.inputAzimuth.get()
        self.motor.userEle = self.inputElevation.get()
        self.motor.readUserInput()      


    def quit(self):
        self.root.destroy()


