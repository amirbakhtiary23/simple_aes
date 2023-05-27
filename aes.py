#AES128 implementation
#the text should be placed in a file called text.txt 

from copy import deepcopy
import numpy as np
import vigenere as vgn
sub_matrix=[
    [4,2,5,11],
    [15,14,13,0],
    [6,7,12,8],
    [1,10,9,3]
    ]
column_constant=[
    []]
"""
preprocessing
"""
test=["abcsdfghjklpoiuyt","abcsdfghjklpoiuyt","abcsdfghjklpoiuyt","abcsdfghjklpoiuyt",
      "abcsdfghjklpoiuyt","abcsdfghjklpoiuyt","abcsdfghjklpoiuyt","abcsdfghjklpoiuyt"
      "abcsdfghjklpoiuyt","abcsdfghjklpoiuyt","abcsdfghjklpoiuyt"]
round_keys=[]
primary_key=vgn.gen_key()
round_keys_keys=vgn.generate_keys()
for j in round_keys_keys:
    round_keys.append(vgn.vigenere_encrypt(primary_key, j).lower())

with open ("text.txt","r") as file :
    txt=bytes(file.read(), 'ascii')
primary_key=vgn.gen_key()
round_keys_keys=vgn.generate_keys()
class Key :
    
    def __init__(self,length=128):
        self.round_keys=[]
        self.round_keys_bytes=[]
        for j in round_keys_keys:
            temp=vgn.vigenere_encrypt(primary_key, j).lower()
            self.round_keys.append(temp)
            self.round_keys_bytes.append(bytes(temp,"ascii"))
        #print (len(self.round_keys_bytes))
        self.bits=[]
        for j in self.round_keys_bytes:
            for i in j:
                self.bits.append(int(i))
        
        
        self.key_blocks=self.__creatingBlocks__(self.bits)
    def __creatingBlocks__(self,bits):
        #a method to create enough 16 bytes block "matrix"
        blocks=[]
        steps=len(bits)//16
        for j in range(steps):
            blocks.append([])
        for step in range(steps):
            #bits[step*16:step+16]
            for j in range(4):

                blocks[step].append(bits[step*16:step*16+16][j*4:j*4+4])
        return blocks



class Encryption :
    
    def __init__(self,text,keys,sub_matrix):
        self.sub_matrix=sub_matrix
        self.keys=keys
        bits=[]
        for j in txt :
            bits.append(j)
        self.bits=self.__adjust__(bits)#calling adjust to adjust the last block size
        self.blocks=self.__creatingBlocks__(self.bits)

        #self.sub=self.__shiftColumns__(self.blocks)
    def Encrypt(self):
        return self.encrypt(self.blocks, self.keys)
    def encrypt(self,blocks,keys):
        #encrypted_blocks=[]
        tmp=self.__XOR__(blocks, keys, 0)
        
        for j in range(1,11):
            tmp=self.__SUB__(tmp, sub_matrix)
            tmp=self.__shiftRows__(tmp)
            tmp=self.__shiftColumns__(tmp)
            tmp=self.__XOR__(tmp,keys,j)
            #print (keys[j])
        return tmp
        
    def __adjust__(self,bits):
        #this method is defined so the amount of bytes divided by 8 equal zero
        #32 is the ascii value for space, so we add spaces at the end of the text
        bits_=deepcopy(bits)
        for j in range(16-len(bits_)%16):
            bits_.append(32)
        return bits_
    
    def __creatingBlocks__(self,bits):
        #a method to create enough 16 bytes block "matrix"
        blocks=[]
        steps=len(bits)//16
        for j in range(steps):
            blocks.append([])
        for step in range(steps):
            #bits[step*16:step+16]
            for j in range(4):

                blocks[step].append(bits[step*16:step*16+16][j*4:j*4+4])
        return blocks
    def __XOR__(self,text_array,keys_array,index):
        xor_output=[]
        for j in text_array:
            
            xor_output.append(list(np.bitwise_xor(j,keys_array[index])))
        return xor_output      
    
    def __SUB__(self,text_array,sub_matrix):
        sub_matrix_=deepcopy(text_array)
        for index,value in enumerate(text_array):
            for i in range(4):
                for j in range(4):
                    sub_matrix_[index][i][j]=value[sub_matrix[i][j]//4][sub_matrix[i][j]%4]
        return sub_matrix_
            
    def __shiftRows__(self,array):
        array_=deepcopy(array)
        for j in array_:
            for i in range(4) :
                #print (j[i],self.__move__(j[i],i))
                j[i]=self.__move__(j[i],i)
                #print (j[i])
        return array_
    def __shiftColumns__(self,array):
        array_=deepcopy(array)
        for j in array_:
            for i in range(1,4):
                temp=self.__move__([j[0][i],j[1][i],j[2][i],j[3][i]],i)
                for x in range(4):
                    j[x][i]=temp[x]
        return array_
        
    def __move__(self,arr, n):
        return [arr[(idx-n) % len(arr)] for idx,_ in enumerate(arr)]
            
    
x=Key()    
y=Encryption(txt,x.key_blocks,sub_matrix)
z=y.Encrypt()
encrypted_text=""
for i in z:
    for j in i:
        for f in j:
            encrypted_text=encrypted_text+str(f)+"\n"
with open ("encrypted.txt","w") as file:
    file.write(encrypted_text)
#print (y.blocks)
with open ("keys.txt","w") as file:
    file.write(str(x.round_keys))
