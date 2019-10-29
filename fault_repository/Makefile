CC=gcc
CFILES = $(wildcard c_src/*.c)
COBJ = $(patsubst %.c, %, $(notdir $(CFILES)))


all: $(COBJ)

$(COBJ): $(CFILES)
	$(CC) -o $@ $<

%.o: %.c
	$(CC) $(CFLAGS) $^ -o $@
