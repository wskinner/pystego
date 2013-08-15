# A script for encoding messages in images. 
## Usage
```bash
    bash-3.2$ echo "super secret message" > msg.txt
    bash-3.2$ cat msg.txt | ./steg.py kitty.png
    bash-3.2$ ls
    kitty-enc.png kitty.png msg.txt   steg.py
    bash-3.2$ ./steg.py -d kitty-enc.png
    super secret message
    bash-3.2$ 
```
## Notes
This is obiously not at all secure... if you want security, encrypt the data before
encoding it in the image. 
Currently, only uncompressed formats like PNG are supported.
