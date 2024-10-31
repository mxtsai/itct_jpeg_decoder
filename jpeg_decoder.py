from struct import unpack, calcsize

class JPEG_Decoder():

    def __init__(self, file_path):

        self.file_path = file_path

        self.data_type = ">H"
        self.byte_array = self.read_bytes()
        self.headers = self.load_header()
    
    def read_bytes(self):
        """reads the bytes of the file into an array"""
        f = open(self.file_path, "rb")
        return f.read()
    
    def load_header(self):
        """returns the list of headers to scan for and the scanning order (as per JPEG standard)"""

        headers = {
            "start_of_image": b'\xFF\xD8',
            "application": b'\xFF\xE0',
            "quantization": b'\xFF\xDB',
            "start_of_frame": b'\xFF\xC0',
            "huffman": b'\xFF\xC4',
            "start_of_scan": b'\xFF\xDA',
            "end_of_image": b'\xFF\xD9'
        }

        headers_hex = {k: unpack(self.data_type, v)[0] for k, v in headers.items()}

        return headers_hex


    def scan_byte_array(self):
        """scans the byte array for the headers"""

        idx_pointer = 0
        read_image_data = False
        
        while idx_pointer < len(self.byte_array):
            
            _item_id = self.byte_array[idx_pointer:idx_pointer+2]  # read the current item in byte array
            _item_id_hex = unpack(self.data_type, _item_id)[0]  # convert the item to hex

            if read_image_data:
                # if we are reading the image data, we will read till the end of the file, no header, so no +2
                _item_len = len(self.byte_array[idx_pointer:-2])
                read_image_data = False

                print(f"Reading Image Data at index {idx_pointer} with length {_item_len} --> {idx_pointer+_item_len}")

            else:

                _item_len = 2   # default length of the header
                for _header, _header_hex in self.headers.items():

                    if _item_id_hex != _header_hex:
                        continue    # skip process if no header match

                    # start reading the image data on next length jump if 'start_of_scan' header is found
                    read_image_data = True if _header == "start_of_scan" else False  
                    
                    if _header not in ["start_of_image", "end_of_image"]:
                        
                        # get length of item (next 2 bytes after the header)
                        _item_len_byte = self.byte_array[idx_pointer+2:idx_pointer+4]
                        _item_len += unpack(self.data_type, _item_len_byte)[0]
                    
                    print(f"Header: {_header} at index {idx_pointer} with length {_item_len} --> {idx_pointer+_item_len}")
                    break

            idx_pointer += _item_len
        

if __name__ == "__main__":

    image_list = [
        # "./data/gig-sn01.jpg", 
        # "./data/gig-sn08.jpg", 
        # "./data/monalisa.jpg", 
        "./data/teatime.jpg"
    ]

    for image in image_list:
        decoder = JPEG_Decoder(image)
        # print(len(decoder.byte_array))
        # starter = decoder.byte_array[:2]
        # print(starter)
        # print(unpack(">H", starter))
        # print(calcsize(starter))
        print()
        decoder.scan_byte_array()

    # code = b"\x00\x43"
    # print(unpack(">H", code)[0])