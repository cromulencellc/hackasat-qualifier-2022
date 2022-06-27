BUILD_DIR ?= ./build
SRC_DIR ?= ./src
PRIV_DIR ?= ./priv

TARGET ?= small_hashes_anyways

CC := /opt/cross/bin/microblaze-linux-gcc
CXX := /opt/cross/bin/microblaze-linux-g++
STRIP := /opt/cross/bin/microblaze-linux-strip

CPPFLAGS := -MD
CFLAGS := -Wall -Werror
CXXFLAGS := -Wall -Werror -std=c++17 -O0
LDFLAGS := -std=c++17

SRCS := $(shell find $(SRC_DIR) -name "*.cpp")
OBJS := $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

$(BUILD_DIR)/$(TARGET): $(OBJS)
	$(CXX) $(filter-out ./build/XXXXX.o,$(OBJS)) -o $@ $(LDFLAGS)
	$(STRIP) $@

$(BUILD_DIR)/%.o:$(SRC_DIR)/%.cpp
	mkdir -p $(dir $@)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

.PHONY: clean run all $(BUILD_DIR)

all: $(BUILD_DIR)/$(TARGET)

run: $(BUILD_DIR)/$(TARGET)
	$<

clean:
	rm -rf $(BUILD_DIR)

-include $(DEPS)
