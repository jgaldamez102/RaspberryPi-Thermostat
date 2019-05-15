#randomly generate 100 numbers
#for each of the three digits of the desired temp add three consecutive digits to each respective number and send the start location of the first digit to the pi
#the pi will also generate this list and use it to decrypt the temp data
def LFSRencrypt():
    seed = [1,0,0,1,1,0,1,0]
    keys=[]
    #develop 20 keys
    for n in range(100):
        seedStr = '0b'
        for i in range(len(seed)):
            seedStr+=str(seed[i])
        keys.append(int(seedStr,0))
        newBit = seed[2]^seed[7]
        seed.pop(0)
        seed.append(newBit)
    return keys
