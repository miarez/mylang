CC = gcc
CFLAGS = -Wall -Wextra -g

SRC_DIR = src
BUILD_DIR = build
TEST_DIR = tests

TARGET = $(BUILD_DIR)/c4
SRC = $(wildcard $(SRC_DIR)/*.c)

all: $(TARGET)

$(TARGET): $(SRC)
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -rf $(BUILD_DIR)
