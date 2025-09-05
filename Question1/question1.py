"""
Group name: CAS15
Group member1: Atulya Subedi, Student ID: S394148
Group member2: Oliver Charles Cole, Student ID: S368184
Group member3: Megh RakeshKumar Brahmbhatt, Student ID: S394095
"""    
    

"""This is an algorithm that reads a file named "raw_text.txt"
and encrypts its content using a simple encryption method based
on the logic provided on assignment
"""
alphalow  = "abcdefghijklmnopqrstuvwxyz"
# Define the uppercase alphabet string
alphahigh = alphalow.upper()

# This is a function to encrypt every single character
def encrypt_char(ch, shift1, shift2):
    """Return (encrypted_char, marker) where marker is '0' for low-half, '1' for high-half."""

    #It looks after lowercase
    if ch.islower():
        x = alphalow.index(ch)                     
        if x < 13:                                  
            enc = alphalow[(x + shift1 * shift2) % 26]  
            return enc, '0'                        
        else:
            enc = alphalow[(x - (shift1 + shift2)) % 26] 
            return enc, '1'                         

    # It looks after uppercase
    elif ch.isupper():
        x = alphahigh.index(ch)                     # Find position of character in uppercase alphabet
        if x < 13:                                  
            enc = alphahigh[(x - shift1) % 26]      
            return enc, '0'                         
        else:
            enc = alphahigh[(x + shift2 * shift2) % 26] 
            return enc, '1'                         

    # only alphabetic characters are changed, others (non-alphabetic characters are not changed)
    else:
        return ch, None


#This is a function to decrypt the encrpyted character
def decrypt_with_marker(enc_ch, marker, shift1, shift2):

    # Handle lowercase decryption
    if enc_ch.islower():
        y = alphalow.index(enc_ch)                  
        if marker == '0':                           
            return alphalow[(y - (shift1 * shift2)) % 26]  
        else:                                      
            return alphalow[(y + (shift1 + shift2)) % 26]  

    # It looks after uppercase decryption
    else:
        y = alphahigh.index(enc_ch)                 
        if marker == '0':                           
            return alphahigh[(y + shift1) % 26]     
        else:                                       
            return alphahigh[(y - (shift2 * shift2)) % 26] 


# This is a function that asks the user for the first and second input value
def read_raw():
    shift1 = int(input("input shift1 value: "))
    shift2 = int(input("input shift2 value: "))

# creating a empty list to store markers value
    markers = []                                  

    # Open the raw text file for reading and the encrypted text file for writing
    with open("raw_text.txt", "r") as fr, open("encrypted_text.txt", "w") as fe:
        for line in fr:                             
            for ch in line:                         
                if ch.isalpha():                    
                    enc, marker = encrypt_char(ch, shift1, shift2) # Encrypt character
                    fe.write(enc)                   
                    markers.append(marker)          
                else:
                    fe.write(ch)                    

    # Call decryption immediately, passing the collected markers
    print("The decryption was successful")
    read_encrypted(shift1, shift2, markers)

#This function reads the encrpyted file
def read_encrypted(shift1, shift2, markers):
    marker_idx = 0                                  

    with open("encrypted_text.txt", "r") as fe, open("decrypted_text.txt", "w") as fd:
        for line in fe:                             
            for ch in line:                         
                if ch.isalpha():                    
                    marker = markers[marker_idx]    
                    marker_idx += 1                 
                    fd.write(decrypt_with_marker(ch, marker, shift1, shift2)) 
                else:
                    fd.write(ch)                   

read_raw()

