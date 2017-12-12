# read file into byte array
file="/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/t10k-labels.idx1-ubyte"
bytes=[]
byte=None
with open(file, "rb") as f:
    while byte != b"":
        # Do stuff with byte.
        byte = f.read(1)
        bytes.append(byte)
# parse first bits
bytesSequence=b"".join(bytes[0:4])
number=int.from_bytes(bytesSequence, byteorder='big')
print("number="+str(number))
