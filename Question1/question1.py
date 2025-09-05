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
        x = alphalow.index(ch)                      # Find position of character in lowercase alphabet
        if x < 13:                                  # Check if character is in the lower half (a–m)
            enc = alphalow[(x + shift1 * shift2) % 26]  # Apply forward shift using product rule
            return enc, '0'                         # Return encrypted char with marker for low-half
        else:
            enc = alphalow[(x - (shift1 + shift2)) % 26] # Apply backward shift using sum rule
            return enc, '1'                         # Return encrypted char with marker for high-half

    # It looks after uppercase
    elif ch.isupper():
        x = alphahigh.index(ch)                     # Find position of character in uppercase alphabet
        if x < 13:                                  # Check if character is in the lower half (A–M)
            enc = alphahigh[(x - shift1) % 26]      # Apply backward shift using first shift only
            return enc, '0'                         # Return encrypted char with marker for low-half
        else:
            enc = alphahigh[(x + shift2 * shift2) % 26] # Apply forward shift using square of second shift
            return enc, '1'                         # Return encrypted char with marker for high-half

    # only alphabetic characters are changed, others (non-alphabetic characters are not changed)
    else:
        return ch, None


#This is a function to decrypt the encrpyted character
def decrypt_with_marker(enc_ch, marker, shift1, shift2):

    # Handle lowercase decryption
    if enc_ch.islower():
        y = alphalow.index(enc_ch)                  # Find position of encrypted char
        if marker == '0':                           # If original was from low-half
            return alphalow[(y - (shift1 * shift2)) % 26]  # Undo forward shift
        else:                                       # If original was from high-half
            return alphalow[(y + (shift1 + shift2)) % 26]  # Undo backward shift

    # It looks after uppercase decryption
    else:
        y = alphahigh.index(enc_ch)                 # Find position of encrypted char
        if marker == '0':                           # If original was from low-half
            return alphahigh[(y + shift1) % 26]     # Undo backward shift
        else:                                       # If original was from high-half
            return alphahigh[(y - (shift2 * shift2)) % 26] # Undo forward shift


# This is a function that asks the user for the first and second input value
def read_raw():
    shift1 = int(input("input #1: "))
    shift2 = int(input("input #2: "))

# creating a empty list to store markers value
    markers = []                                  

    # Open the raw text file for reading and the encrypted text file for writing
    with open("raw_text.txt", "r") as fr, open("encrypted_text.txt", "w") as fe:
        for line in fr:                             # Process each line in the raw file
            for ch in line:                         # Process each character in the line
                if ch.isalpha():                    # Encrypt only alphabetic characters
                    enc, marker = encrypt_char(ch, shift1, shift2) # Encrypt character
                    fe.write(enc)                   # Write encrypted character to output file
                    markers.append(marker)          # Store marker in memory list
                else:
                    fe.write(ch)                    # Write non-alphabetic characters unchanged

    # Call decryption immediately, passing the collected markers
    read_encrypted(shift1, shift2, markers)

#This function reads the encrpyted file
def read_encrypted(shift1, shift2, markers):
    marker_idx = 0                                  # Track current position in markers list

    with open("encrypted_text.txt", "r") as fe, open("decrypted_text.txt", "w") as fd:
        for line in fe:                             # Process each line in encrypted file
            for ch in line:                         # Process each character in the line
                if ch.isalpha():                    # Decrypt only alphabetic characters
                    marker = markers[marker_idx]    # Retrieve corresponding marker
                    marker_idx += 1                 # Move to next marker
                    fd.write(decrypt_with_marker(ch, marker, shift1, shift2)) # Write decrypted char
                else:
                    fd.write(ch)                    # Write non-alphabetic characters unchanged

read_raw()