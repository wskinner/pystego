from PIL import Image

class StegImage():
    def __init__(self, img, compression=1):
        self.img = img
        self.bit_index = 0
        self.compression = compression
        self.pixel_modulus = compression * 3
        self.pixels = map(list, img.getdata())
        self.num_header_pixels = 10

    def encode(self, msg):
        self.bit_index = 0
        pixels = self.img.getdata()
        num_pixels = self.img.size[0] * self.img.size[1]
        max_bits = num_pixels * 3 - self.num_header_pixels * 3

        msg_bits = self.getBits(msg)
        if len(msg_bits) > max_bits:
            raise Exception('find a bigger photo, fool')
        
        length = len(msg)*8
        len_bits = self.getNBits(length, self.num_header_pixels*3)
        for bit in len_bits:
            self.setNextBit(bit)
        for bit in msg_bits:
            self.setNextBit(bit)

        self.bit_index = 0

    def setNextBit(self, bit):
        pix = self.bit_index / self.pixel_modulus
        rem = self.bit_index % self.pixel_modulus
        col = rem / self.compression
        b = rem % self.compression
        mask = (0xff - 2**b) & self.pixels[pix][col]
        self.pixels[pix][col] = mask | (bit * 2**b)
        self.bit_index += 1

    def getNextBit(self):
        pix = self.bit_index / self.pixel_modulus
        rem = self.bit_index % self.pixel_modulus
        col = rem / self.compression
        b = rem % self.compression
        mask = 2**b
        bit = self.pixels[pix][col] & mask
        self.bit_index += 1
        return bit >> b
              
    def bitsToInt(self, bits):
        bits.reverse()
        val = 0
        for i in xrange(len(bits)):
            val += bits[i] * 2**i
        return val

    def getNBits(self, num, n):
        n -= 1
        bits = []
        while n >= 0:
            if num & 2**n:
                bits.append(True)
            else:
                bits.append(False)
            n -= 1
        return bits

    def getBits(self, msg):
        bits = []
        for c in msg:
            byte = []
            for i in reversed(range(8)):
                if ord(c) & 2**i > 0:
                    bits.append(True)
                    byte.append(1)
                else:
                    bits.append(False)
                    byte.append(0)
        return bits

    def bitsToChars(self, bits):
        msg = []
        current_byte = []
        for b in bits:
            current_byte.append(b)
            if len(current_byte) == 8:
                val = 0
                for j,bit in enumerate(current_byte):
                    val += bit * 2**(7-j)
                msg.append(chr(val))
                current_byte = []
        return ''.join(msg)

    def decode(self):
        self.bit_index = 0
        msg_bits = []
        length_bits = []

        for i in xrange(self.num_header_pixels * 3):
            length_bits.append(self.getNextBit())
        length = self.bitsToInt(length_bits)
        print 'length_bits', length_bits, length

        for i in xrange(length):
            msg_bits.append(self.getNextBit())
        self.bit_index = 0
        return self.bitsToChars(msg_bits)

    def save(self, name):
        new_img = Image.new(self.img.mode, self.img.size)
        new_img.putdata(map(tuple, self.pixels))
        new_img.save(name)

    def open(self, name):
        self.img = Image.open(name)
        self.pixels = map(list, self.img.getdata())

