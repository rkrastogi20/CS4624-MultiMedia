import sys
from re import match

def compress(inputString):
	"""compression algorithm:
		- The input is a string, and the output is a compressed string.
		- A valid input consists of zero or more upper case english letters A-Z.
		- Any run of two or more of the same character converted to two of that character plus a number indicating how many repeated runs were compressed. 
		- Only one digit used at a time.
		Examples:
		    A --> A
		    AA --> AA0
		    AAA --> AA1
		    AAAAAAAAAAAA --> AA9A
		    AAAAAAAAAAAAA --> AA9AA0
	"""
	outputString = ''
	lastChar = ''
	charIndex = 0
	maxIndex = len(inputString)

	while charIndex < maxIndex:

		nextChar = inputString[charIndex]
		assert(match('[A-Z]', nextChar))
		outputString += nextChar
		charIndex += 1

		if(nextChar == lastChar): # fastforward charIndex through the duplicated characters
			count = 0 # counts duplicate characters compressed
			while((charIndex+count<maxIndex) and (inputString[charIndex+count]==lastChar) and (count<9)):
				count += 1
			charIndex += count
			nextChar = str(count)
			outputString += nextChar
		lastChar = nextChar

	return outputString

def decompress(inputString):
	"""Counterpart to compress -- undoes compression
		inputString=: decompress(compress(inputString))
	"""
	outputString = ''
	lastChar = ''
	charIndex = 0
	maxIndex = len(inputString)

	while charIndex < maxIndex:
		nextChar = inputString[charIndex]

		if(match('[A-Z]', nextChar)):
			outputString += nextChar
		else:
			assert(match('[0-9]',nextChar) and charIndex>1 and match('[A-Z]', lastChar) and (lastChar==inputString[charIndex-2]))
			for i in range(int(nextChar)): outputString += lastChar

		charIndex += 1
		lastChar = nextChar

	return outputString

def main(compress_decompress='compress'):
        #        """ parameter: <compress|decompress> to indicate which algorithm to call 
        #	                reads from standard input and prints to standard output"""

        exi = 0
        while (exi == 0): # read to EOF
                print("1) \t compress")
                print("2) \t decompress")
                print("3) \t Quit from program")
                cho = int ( input("please enter your choice <1-3> : ") )
                print(" ")
                
                if cho == 3 :
                        exi = 1
                        return
                        
                elif cho == 1:
                        fn = compress
                        
                elif cho == 2:
                        fn = decompress
                        
                try:
                        inputString = sys.stdin.readline()
                        
                except KeyboardInterrupt:
                        break
                
                if not inputString:
                        break
                
                # strip off '\n'
                if inputString[len(inputString)-1] == '\n':
                        inputString = inputString[:len(inputString)-1]
                        
                # augment input with chosen algorithm
                outputString = fn(inputString)		
                print(outputString)
                print(' ')
                
        return

if __name__ == '__main__':
        if len(sys.argv) > 1:
                main(sys.argv[1])
        else:
                main()
