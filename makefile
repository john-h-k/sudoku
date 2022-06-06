PY_CFLAGS  := $(shell python3-config --cflags)
PY_LDFLAGS := $(shell python3-config --ldflags)
PY_INCLUDE := $(shell python3-config --includes)

# the compiler to use
CC = gcc

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS = 
  
#files to link:
LFLAGS =
  
# the name to use for both the target source file, and the output file:
TARGET = solver
  
all: $(TARGET)
 
$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -O3 -mcpu=apple-m1 -o $(TARGET) $(TARGET).c $(LFLAGS)