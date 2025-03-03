import SbW_Streamer

#Import the COM PORT
streamer=SbW_Streamer.SbW_Streamer('COM4',115200,1)
#Open the COM PORT
Status = streamer.Open()
print (Status)


############### Get_Set_SamplingFreq TESTING ################

#Read one frame
"""
R_S = streamer.Get_Set_SamplingFreq(1)
print(R_S)
"""

#Write one frame
"""
streamer.SamplingFreq = 12
W_S = streamer.Get_Set_SamplingFreq(0)
print(W_S)
"""

#Read & Write multiple frames
"""
for y in range(0,65536):
    
    for j in range(0,2):
        if j == 0 :
            streamer.SamplingFreq = y
            W_S = streamer.Get_Set_SamplingFreq(j)
            print('Sampling Frequency Register write:'+ str(W_S))
        else:
            R_S = streamer.Get_Set_SamplingFreq(j)
            print('Sampling Frequency Register read:',R_S)
"""

############### Get_Set_FrameLength TESTING ################

#Read one frame
"""
R_F= streamer.Get_Set_FrameLength(1)
print(R_F)
"""

#write one frame
"""
streamer.FrameLength = 12
W_F = streamer.Get_Set_FrameLength(0)
print(W_F)
"""

#Read & Write multiple frames
"""
for x in range(0,256):
    for i in range(0,2):
        if i == 0 :
            streamer.FrameLength = x
            W_F = streamer.Get_Set_FrameLength(i)
            print('Frame Length Register write:'+ str(W_F))
        else:
            R_F = streamer.Get_Set_FrameLength(i)
            print('Frame Length Register read:',R_F)
"""


pass