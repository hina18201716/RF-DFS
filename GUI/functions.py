import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import time
import serial
import serial.tools.list_ports
import io 

class MotorControl: 

    def __init__(self, Azimuth, Elevation, userAzi = 0, userEle = 0, Azi_bound = [0,360], Ele_bound = [0,180] ): 
        self.Azimuth = Azimuth
        self.Elevation = Elevation
        self.userAzi = userAzi
        self.userEle = userEle
        self.Azi_bound = Azi_bound
        self.Ele_bound = Ele_bound
        self.port = ''
       
        self.ser = serial.Serial(port= 'COM4', baudrate=9600 )

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
            # popup error message
            print ("Input must be integers")
            self.InputTypeError()

    def InputTypeError( self ):
        messagebox.showwarning( title= "Inout Error" , message= "Input must be numbers")

    def RangeError( self ):
        range = "Azimuth: " + str(self.Azi_bound[0]) + "-" + str(self.Azi_bound[1]) + "\n" + "Elevation: " +  str(self.Ele_bound[0]) + "-" + str(self.Ele_bound[1])
        messagebox.showwarning( title= "Range error", message= "Input must be in range \n" + range ) 

        
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
            print ("send commend to arduino")
            self.moveAntenna()
        else: 
            # error popup
            print("range error")
            self.RangeError()

    def moveAntenna( self ):
        # commandX = 'jog abs x ' + self.userAzi
        # self.ser.write( commandX.encode('utf-8'))
        # line1 = self.ser.readline()
        # data1 = line1.decode('utf-8')
        # print( data1 ) 


        commandY = 'jog abs y '
        self.ser.write( commandY.encode('utf-8'))
        line2 = self.ser.readline()
        data2 = line2.decode('utf-8')
        print( data2 ) 

        self.Azimuth = self.userAzi
        self.Elevation = self.userEle
        print ( "position updated")

    def portConnection( self ):
        print( "port was changed to " + self.port)
        if self.ser.isOpen():
            self.ser.close()
        self.ser = serial.Serial(port= str( self.port ), baudrate=9600 )



class Newwindow():
    def __init__(self):
 
        self.root = tk.Tk()
        self.root.geometry('400x300')
        self.root.title('DFS-control')
        
        # box of asi ele information 
        self.positions = tk.LabelFrame( self.root  , text = "Antenna Position" )
        self.positions.grid( row = 1 , column = 0 , padx = 20 , pady = 10)
        self.quickButton = tk.Frame( self.root  )
        self.quickButton.grid( row = 1, column= 1 , padx = 20 , pady = 10)

        # port selection
        ports = list( serial.tools.list_ports.comports() ) 
        self.port_selection = ttk.Combobox( self.root , values = ports )
        self.port_selection.grid(row = 0, column= 0 , padx = 20 , pady = 10)

        # emargency stop creation
        self.EmargencyStop = tk.Button( self.quickButton, text = "Emargency Stop", font = ('Arial', 16 ) , bg = 'red', fg = 'white' , command= self.Estop )
        self.EmargencyStop.pack()

        # park button creation
        self.Park = tk.Button( self.quickButton, text = "Park", font = ('Arial', 16) , bg = 'blue', fg = 'white' , command = self.park )
        self.Park.pack()

        # azi,ele input boxes creation
        self.boxFrame = tk.Frame( self.positions )
        self.boxFrame.pack()

        # create motor from class "Motorcontrol"
        self.motor = MotorControl( 0 , 90 )

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

        # exit button creation
        self.exitbutton = tk.Button( self.positions , text = "Exit" , command = quit )
        self.exitbutton.pack()

        self.root.mainloop()

    def Estop(self):
        print( " Emargency button was pushed ")
        # send serial command to stop moving antenna (JOG OFF)
    
    def park( self ):
        print( "Park antenna to 0:0 position" )
        # send serial command to move antenna to home ( JOG HOME / JOG abs x 0 & JOG abs y 0 )
 
    def input(self):
        # show user values in terminal
        print("---------------------------------")
        print( "Here are user inputs" )
        print( "Azimuth: ",  self.inputAzimuth.get() )
        print( "Elevation: ", self.inputElevation.get() )
        print ( "COM: ", self.port_selection.get() )

        # update user value in motor class
        self.motor.userAzi = self.inputAzimuth.get()
        self.motor.userEle = self.inputElevation.get()
        self.motor.readinput()

    # change port if current port is different from user input 
    # place this fanctionality in portConnection in motor class
        if self.motor.port != self.port_selection.get()[:4]: 
            portName = self.port_selection.get()
            self.motor.port = portName[:4]
            self.motor.portConnection()
            print("switching port")
        
    def quit(self):
        self.root.destroy()
