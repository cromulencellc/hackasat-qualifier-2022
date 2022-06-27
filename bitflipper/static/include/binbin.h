#ifndef _BINBIN__
#define _BINBIN__

// Debugging
#define DEBUG 0
#if DEBUG
    #define LOG printf
#else
    #define LOG(...) while(0){}
#endif

#define LOG_ERR(...) fprintf(stderr, __VA_ARGS__)

// Print a byte in binary.
#define U16_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c"
#define U16_TO_BINARY(byte)  \
  (byte & 0x8000 ? '1' : '0'), \
  (byte & 0x4000 ? '1' : '0'), \
  (byte & 0x2000 ? '1' : '0'), \
  (byte & 0x1000 ? '1' : '0'), \
  (byte & 0x0800 ? '1' : '0'), \
  (byte & 0x0400 ? '1' : '0'), \
  (byte & 0x0200 ? '1' : '0'), \
  (byte & 0x0100 ? '1' : '0'), \
  (byte & 0x0080 ? '1' : '0'), \
  (byte & 0x0040 ? '1' : '0'), \
  (byte & 0x0020 ? '1' : '0'), \
  (byte & 0x0010 ? '1' : '0'), \
  (byte & 0x0008 ? '1' : '0'), \
  (byte & 0x0004 ? '1' : '0'), \
  (byte & 0x0002 ? '1' : '0'), \
  (byte & 0x0001 ? '1' : '0')

#define U16_COUNT_ONES(byte) \
  (byte & 0x8000 ? 1 : 0)+ \
  (byte & 0x4000 ? 1 : 0)+ \
  (byte & 0x2000 ? 1 : 0)+ \
  (byte & 0x1000 ? 1 : 0)+ \
  (byte & 0x0800 ? 1 : 0)+ \
  (byte & 0x0400 ? 1 : 0)+ \
  (byte & 0x0200 ? 1 : 0)+ \
  (byte & 0x0100 ? 1 : 0)+ \
  (byte & 0x0080 ? 1 : 0)+ \
  (byte & 0x0040 ? 1 : 0)+ \
  (byte & 0x0020 ? 1 : 0)+ \
  (byte & 0x0010 ? 1 : 0)+ \
  (byte & 0x0008 ? 1 : 0)+ \
  (byte & 0x0004 ? 1 : 0)+ \
  (byte & 0x0002 ? 1 : 0)+ \
  (byte & 0x0001 ? 1 : 0)

#define U16_COUNT_ZEROS(byte) \
  (byte & 0x8000 ? 0 : 1)+ \
  (byte & 0x4000 ? 0 : 1)+ \
  (byte & 0x2000 ? 0 : 1)+ \
  (byte & 0x1000 ? 0 : 1)+ \
  (byte & 0x0800 ? 0 : 1)+ \
  (byte & 0x0400 ? 0 : 1)+ \
  (byte & 0x0200 ? 0 : 1)+ \
  (byte & 0x0100 ? 0 : 1)+ \
  (byte & 0x0080 ? 0 : 1)+ \
  (byte & 0x0040 ? 0 : 1)+ \
  (byte & 0x0020 ? 0 : 1)+ \
  (byte & 0x0010 ? 0 : 1)+ \
  (byte & 0x0008 ? 0 : 1)+ \
  (byte & 0x0004 ? 0 : 1)+ \
  (byte & 0x0002 ? 0 : 1)+ \
  (byte & 0x0001 ? 0 : 1)

#endif // _BINBIN__