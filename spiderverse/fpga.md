# Secure FPGA Configuration Document

This document describes how to use the configuration engine of this *very secure* FPGA.

##  Bit File Structure

### Unencrypted Data Structure

| Name  | Bytes | Description |
| ------| ------ | ----------- |
| Header| 16 | Bitfile header - all bit files must have this header
| Encryption Start Command | 4 | Starts the FPGA encryption engine | 
| Encrypted Data | N | AES-256 IV followed by encrypted blocks of data |
| Footer | 16 | Bitfile footer - all bit files must have this footer to be valid

As shown in the table above all the data in the bitfile is in the encrypted data section that is variable length.

The unencrypted portions of the file are **fixed format** and required to load.
### Encrypted Data Structure


The following table describes the structure of the encrypted section of the data file. Once decrypted the data should have the following format:

| Name | Bytes | Description |
| ---- | ----- | ----------- |
| HMAC Key | 16| Key for HMAC|
| Commands | N | Commands to configure the FPGA |
| HMAC Tag | 64 | ASCII representation of HMAC-SHA256 tag. |

The commands section is a set of commands sequentially ordered in the binary. Valid commands are described in the next section.

### Command words

The command words in the commands section of the encrypted data must follow one of the following formats. 

**Write Command**
| Byte Number |  Description |
| ----------- |  ----------- |
| 0           |  Action. Must be 0x01 to write |
| 1  |Config register address to write |
| 2-3         |  Length of data (N) to write as a UINT16 | 
| 4-(N+4) | Data bytes of length N |

**Read Command**
| Byte Number | Description |
| ----------- | ------------|
| 0 | Action. Must be 0x10 to read |
| 1 | Configuration register to read |

**No-op Command**
| Byte Number | Description |
| ----------- | ----------- |
| 0 | Must be 0x11 to signal no-op |


## Configuration Engine 

There are 8 registers available for the user to read/write in the #Command words section of the bit file
| Register | Address | R/W | Description |
| ------   | ------  | --- | ----------- |
| CONFIG   | 0x1     | W   | Configuration mode for FPGA|
| FABRIC   | 0x2     | W   | FPGA fabric data gets written here|
| NV_MEM   | 0x3 | W | Data stored in non-volatile memory used by the fpga fabric gets written here|
| STATUS   | 0x4     | R/W | Displays the current status of the FPGA |
| FABRIC_ADDR | 0x5  | R/W | The current write position into fabric. Read this to see where you are. Write it to move next write to a different position in fabric |
| NV_ADDR     | 0x6  | R/W | The current write position into non-volatile memory. Read this to see where you are. Write it to move next write to a different position in fabric| 
| RESERVED_1  | 0x7  | N/A | Reserved |
| RESERVED_2  | 0x8  | N/A | Reserved | 

### Configuration Mode Options

There are two implemented options for the configuration mode to write to the CONFIG register
| Value | Description |
| ----- | ----------- |
| 0x66696C65 | Immediately load the bitstream that is stored in flash. |
| 0x6A746167 | The user will supply a bitstream over JTAG |