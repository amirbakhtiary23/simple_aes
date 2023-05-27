#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 12:48:50 2023

@author: amir
"""
import numpy as np
from copy import deepcopy
sub_matrix=[
    [4,2,5,11],
    [15,14,13,0],
    [6,7,12,8],
    [1,10,9,3]
    ]
bits=[]
with open ("encrypted.txt","r") as file :
    txt=file.readlines()
for j in txt:
    tmp=list(j)
    tmp.pop()
    bits.append(int("".join(tmp)))
class Decryption :
    
    def __init__(self,text,keys,sub_matrix):
        self.sub_matrix=sub_matrix
        self.keys=keys
        #self.bits=self.__adjust__(txt)#calling adjust to adjust the last block size
        self.blocks=self.__creatingBlocks__(txt)
        #self.sub=self.__shiftColumns__(self.blocks)
    def Decrypt(self):
        return self.decrypt(self.blocks, self.keys)
    def decrypt(self,blocks,keys):

        for j in reversed(range(1,11)):
            if j==10:tmp=self.__XOR__(deepcopy(blocks),keys,j)
            else : tmp=self.__XOR__(tmp,keys,j)
            tmp=self.__shiftColumns__(tmp)
            tmp=self.__shiftRows__(tmp)
            tmp=self.__SUB__(tmp, sub_matrix)
            #print (keys[j])
        #print (tmp)
        tmp=self.__XOR__(tmp, keys, 0)
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
        xor_output=deepcopy(text_array)
        for arr in enumerate(text_array):
            for i in range(4):
                for j in range(4):
                    xor_output[arr[0]][i][j]=np.bitwise_xor(int(arr[1][i][j]),int(keys_array[index][i][j]))
            #print (type(j),type(keys_array[index]))
            #xor_output.append(list(np.bitwise_xor(j,keys_array[index])))
        
        return xor_output      
    
    def __SUB__(self,text_array,sub_matrix):
        sub_matrix_=deepcopy(text_array)
        for index,value in enumerate(text_array):
            for i in range(4):
                for j in range(4):
                    sub_matrix_[index][sub_matrix[i][j]//4][sub_matrix[i][j]%4]=value[i][j]
        return sub_matrix_
            
    def __shiftRows__(self,array):
        array_=deepcopy(array)
        for j in array_:
            for i in range(4) :
                #print (j[i],self.__move__(j[i],i))
                j[i]=self.__move__(j[i],4-i)
                #print (j[i])
        return array_
    def __shiftColumns__(self,array):
        array_=deepcopy(array)
        for j in array_:
            for i in range(1,4):
                temp=self.__move__([j[0][i],j[1][i],j[2][i],j[3][i]],4-i)
                for x in range(4):
                    j[x][i]=temp[x]
        return array_
        
    def __move__(self,arr, n):
        return [arr[(idx-n) % len(arr)] for idx,_ in enumerate(arr)]
            




class Key :
    
    def __init__(self,keys):
        self.round_keys=keys
        self.round_keys_bytes=[]
        for j in self.round_keys:
            self.round_keys_bytes.append(bytes(j,"ascii"))
        self.bits=[]
        for j in self.round_keys_bytes:
            for i in j:
                self.bits.append(i)
        
        
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
with open ("keys.txt") as file:
    keys=file.read()

x=Key(eval(keys))
#print (x.key_blocks)


y=Decryption(bits,x.key_blocks,sub_matrix)
deciphered=y.Decrypt()
for j in deciphered:
    for i in range(4):
        for f in range(4):
            print (chr(j[i][f]),end='')
