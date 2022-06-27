# Stego

First, extract the data from the provided image with steghide. This points you to a Github repo containing 4 commands. 

Provide the correct command mnemonic (PLAYBACK_FILE) to the satellite imaging system and get some base64 encoded binary data in return.

From the header, notice that it's a JPG file. Run steghide again on the file and extract an MD5 hash.

Crack the hash and you have the password, provide that password to the imaging system and you get the flag!