from BitHash import BitHash
from BitVector import BitVector
import math

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):  
        # use the equation to find the number of bits needed
        # when rounding to an int, round up so that there are more bits,
        # which makes it more accurate
        phi = 1 - (maxFalsePositive**(1 / numHashes))
        return math.ceil(numHashes / (1 - (phi)**(1 / numKeys)))
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes? 
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        self.__numBits = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        # initiliaze the BitVector based on the amount of __bitsNeeded
        self.__BitVector = BitVector(size = self.__numBits)
        # keep track of the number of bits set. This will be helpful later
        # when calculating the false positive rate
        self.__bitsSet = 0
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        # set the seed to 0
        hashLevel = 0
        
        # for each time that you hash
        for i in range(self.__numHashes):
            # remember the number that will be used as the next seed
            hashLevel = BitHash(key, hashLevel)
            # calculate the place where this key gets inserted into the BitVector
            placeHolder = hashLevel % self.__numBits
            
            # if the place where this key belongs is not set to 1
            if not self.__BitVector[placeHolder]:
                # set it to 1
                self.__BitVector[placeHolder] = 1
                # increment the number of bits set
                self.__bitsSet += 1
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        # set the seed to 0
        hashLevel = 0
        
        # for each time that you hash
        for i in range(self.__numHashes):
            # remember the number that will be used as the next seed            
            hashLevel = BitHash(key, hashLevel)
            
            # if that place in the BitVector is not set, return False
            if not self.__BitVector[hashLevel % self.__numBits]: return False
        
        # if it is set to 1, return True
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        # the amount of bits not set is the amount of bits minus the amount
        # of bits set
        zeros = self.__numBits - self.__bitsSet
        
        # the proportion of bits not set is the amount of bits not set
        # divided by the amount of bits
        proportionZeros = zeros / self.__numBits   
        
        # return the falsePositiveRate
        return (1 - proportionZeros)**self.__numHashes
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        # return the number of bits actually set
        return self.__bitsSet
        
            
def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
        
    # create the Bloom Filter
    bloom = BloomFilter(numKeys, numHashes, maxFalse)    

    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    fileInput = open("wordlist.txt")
    
    # for each of the keys
    for i in range(numKeys):
        # insert the key into the BitVector
        bloom.insert(fileInput.readline().strip())

    # close the file 
    fileInput.close()

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("falsePositiveRate:", bloom.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 

    wordsMissing = 0
    
    fileInput = open("wordlist.txt")
    
    # for each of the keys that we inserted
    for i in range(numKeys):
        # if it's not found, increment wordsMissing by 1
        if not bloom.find(fileInput.readline().strip()): wordsMissing += 1
	
    print("Words missing:", wordsMissing)
	
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    wordsThere = 0
    
    # for each of the keys that we inserted
    for i in range(numKeys):
        # if it's found, increment wordsThere by 1
        if bloom.find(fileInput.readline().strip()): wordsThere += 1
    
    # close the file
    fileInput.close()
        
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    print("Actual false positive rate:", wordsThere / numKeys)

    
if __name__ == '__main__':
    __main()