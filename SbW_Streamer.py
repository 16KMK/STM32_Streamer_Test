import serial
import time
import numpy as np # as means that instead of numpy , we can type np


Streamer_CMD_Set = {
#   'Name of CMD':(CMD_ID,Dlen)
    'Get_Set_Sampling_Freq':(0x1,2),
    'Get_Set_Frame_Length':(0x2,1),
    'Get_Set_Stream_ON':(0x3,1)
}


class SbW_Streamer:
    #communication params (specific to the com port)
    COM_Name:str
    BaudRate:int
    Timeout:float
    port:serial.Serial

    #class params (specific to the implementation)
    SamplingFreq=np.uint16(0)
    FrameLength=np.uint8(0)
    StreamON=np.uint8(0)


    def __init__(self,COM_port:str,baudRate:int,Timeout:float):
        self.COM_Name = COM_port
        self.BaudRate = baudRate
        self.Timeout =Timeout
    
    def Open(self)->bool:
        try:
            #initialize and open port
            self.port = serial.Serial(self.COM_Name,  baudrate=self.BaudRate,timeout=self.Timeout)
            return True

        except Exception as e:
            return False
    
    #deals with data of frame only without CRC Registers
    def CRC (self,data:list[np.uint8], len:np.uint16)->np.uint16:
        CRC_Result:np.uint16 =0
        for i in range(0,len) :
            CRC_Result += data[i]
        return CRC_Result
    
#user functions
    def Get_Set_SamplingFreq(self,R_W:bool):
        CMD = Streamer_CMD_Set['Get_Set_Sampling_Freq'][0]
        Data_Length = Streamer_CMD_Set['Get_Set_Sampling_Freq'][1]

        Request_Len = 5 if R_W == True else 5+Data_Length
        Reply_Len = 5 + Data_Length if R_W == True else 5

        Frame = np.zeros(Request_Len , dtype=np.uint8)
        Frame[0] = 0x55 #SOF
        Frame[1] = CMD | (0b10000000 if R_W == True else 0)
        Frame[2] = 0 if R_W == True else Data_Length #data length
        # in case of write mode, the data field needs to be filled
        if R_W == False:
            Frame[3] = np.uint8(self.SamplingFreq & 0xFF) 
            Frame[4] = np.uint8(self.SamplingFreq>>8) 
        Checksum = self.CRC(Frame,Request_Len-2)
        Frame[Request_Len-2] = np.uint8(Checksum&0xff)
        Frame[Request_Len-1] = np.uint8(Checksum>>8)

        try:
            self.port.write(Frame)
            Data_in = list(self.port.read(Reply_Len)) 

            #check if the requested num of bytes was recieved
            if(len(Data_in)==Reply_Len):
                #compute the frame checksum
                Checksum_Calc = self.CRC(Data_in,len(Data_in)-2)
                #construct the frame internal checksum
                Checksum = Data_in[Reply_Len-1] | (Data_in[Reply_Len-2]<<8)
                if Checksum == Checksum_Calc:
                    if R_W == False:
                        self.SamplingFreq = np.uint16(Data_in[4] | (Data_in[3]<<8))
                        return Frame
                    else:
                        return Data_in
                else: return False
            else :return False
        except Exception as e:
            print(e)
            return False
    
    def Get_Set_FrameLength(self,R_W:bool):

        CMD = Streamer_CMD_Set['Get_Set_Frame_Length'][0]
        Data_Length = Streamer_CMD_Set['Get_Set_Frame_Length'][1]

        Request_Len = 5 if R_W == True else 5+Data_Length
        Reply_Len = 5 + Data_Length if R_W == True else 5

        Frame = np.zeros(Request_Len , dtype=np.uint8)

        Frame[0] = 0x55 #SOF
        Frame[1] = CMD | (0b10000000 if R_W == True else 0)
        Frame[2] = 0 if R_W == True else Data_Length #data length

        # in case of write mode, the data field needs to be filled
        if R_W == False:
            Frame[3] = self.FrameLength
        Checksum = self.CRC(Frame,Request_Len-2)
        Frame[Request_Len-2] = np.uint8(Checksum&0xff) #0xff= 0b1111 1111
        Frame[Request_Len-1] = np.uint8(Checksum>>8) 

        try:
            self.port.write(Frame)
            Data_Frame = list(self.port.read(Reply_Len)) 
            #check if the requested num of bytes was recieved
            if(len(Data_Frame)==Reply_Len):
                #compute the frame checksum
                Checksum_Calc = self.CRC(Data_Frame,len(Data_Frame)-2)
                #construct the frame internal checksum
                Checksum = Data_Frame[Reply_Len-1] | (Data_Frame[Reply_Len-2]<<8)
                if Checksum == Checksum_Calc:
                    if R_W == False:
                        self.FrameLength = Data_Frame[3]
                        return Frame
                    else:
                        return Data_Frame
                else: return False
            else :return False
        except Exception as e:
            print(e)
            return False