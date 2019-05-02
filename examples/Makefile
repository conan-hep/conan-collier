MKFILE  := $(abspath $(lastword $(MAKEFILE_LIST)))

include conanbuildinfo.mak

CUR_DIR := $(shell pwd)
SRC_DIR := $(patsubst %/,%,$(dir $(MKFILE)))
OBJ_DIR := obj
BIN_DIR := bin

$(info CUR_DIR = $(CUR_DIR))
$(info SRC_DIR = $(SRC_DIR))
$(info OBJ_DIR = $(OBJ_DIR))
$(info BIN_DIR = $(BIN_DIR))

SRC = $(SRC_DIR)/test_collier.cpp
OBJ = $(OBJ_DIR)/test_make.o
EXE = $(BIN_DIR)/test_make

CXXFLAGS += $(CONAN_CXXFLAGS)
CPPFLAGS += $(addprefix -I, $(CONAN_INCLUDE_DIRS))
CPPFLAGS += $(addprefix -D, $(CONAN_DEFINES))
LDFLAGS  += $(addprefix -L, $(CONAN_LIB_DIRS))
LDLIBS   += $(addprefix -l, $(CONAN_LIBS) gfortran)

all: $(EXE)
	@true

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(OBJ): $(SRC) | $(OBJ_DIR)
	$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

$(EXE): $(OBJ) | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS) $(LDLIBS)

.PHONY: all
