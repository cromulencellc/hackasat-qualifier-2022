SRC_DIR := src
OBJ_DIR := obj
BIN_DIR := bin

# Excutable name
EXE := $(BIN_DIR)/bitflipper
# Source files in /src/ folder
SRC := $(wildcard $(SRC_DIR)/*.c)
OBJ := $(SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# C++ flags and Windows compiler
CFLAGS=-Wall -Wextra -Werror
CROSS=sparc64-linux-gnu-
CXFLAGS=-Iinclude
CC := $(CROSS)gcc-10
LDLIBS := -lm
ARCHFLAGS := -static -mcpu=leon3v7 -m32 

# Targets
.PHONY: all clean

all: $(EXE)

$(EXE): $(OBJ) | $(BIN_DIR)
	$(CC) $(ARCHFLAGS) $^ $(LDLIBS) -o $@
	cp $(SRC_DIR)/hardest_rotations.nums $(BIN_DIR)/

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(ARCHFLAGS) $(CFLAGS) $(CXFLAGS) -c $< -o $@

$(BIN_DIR) $(OBJ_DIR):
	mkdir -p $@

clean:
	@$(RM) -rv $(BIN_DIR) $(OBJ_DIR)

-include $(OBJ:.o=.d)
