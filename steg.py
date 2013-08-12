from PIL import Image

class StegImage():
    def __init__(self, img):
        self.img = img

    def encode(self, msg):
        pixels = self.img.getdata()
        num_pixels = self.img.size[0] * self.img.size[1]
        num_header_bits = 30
        max_bits = num_pixels * 3 - num_header_bits

        bits = self.getBits(msg)
        if len(bits) > max_bits:
            raise Exception('find a bigger photo, fool')
        
        new_pixels = []
        for i, (r, g, b) in enumerate(pixels):
            if len(bits) == 0:
                new_pixels.append((r, g, b))
                continue
            new_pixels.append([None, None, None])
            new_pixels[i][0] = (0xfe & r) | (0x01 & bits.pop(0))
            if len(bits) == 0:
                new_pixels[i][1] = g
                new_pixels[i][2] = b
                continue
            new_pixels[i][1] = (0xfe & g) | (0x01 & bits.pop(0))
            if len(bits) == 0:
                new_pixels[i][2] = b
                continue
            new_pixels[i][2] = (0xfe & b) | (0x01 & bits.pop(0))

        pixels = map(tuple, new_pixels)
        self.img.putdata(pixels)

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

    def toChars(bits):
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
        pixels = self.img.getdata()
        msg = []

        current_byte = []
        for i, (r, g, b) in enumerate(pixels):
            if i > 8 * 25:
                break

            current_byte.append(0x01 & r) 
            if len(current_byte) == 8:
                val = 0
                for j,bit in enumerate(current_byte):
                    val += bit * 2**(7-j)
                msg.append(chr(val))
                current_byte = []

            current_byte.append(0x01 & g)
            if len(current_byte) == 8:
                val = 0
                for j,bit in enumerate(current_byte):
                    val += bit * 2**(7-j)
                msg.append(chr(val))
                current_byte = []

            current_byte.append(0x01 & b)
            if len(current_byte) == 8:
                val = 0
                for j,bit in enumerate(current_byte):
                    val += bit * 2**(7-j)
                msg.append(chr(val))
                current_byte = []
        return ''.join(msg)


