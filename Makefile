# The following can be added to CFLAGS for various things
CFLAGS = -g -O2 -std=c89 
CC = gcc
LIBS = 

ALLFILES = Makefile cdgram.y cdlex.l cdecl.c cdecl.1 testset.txt testset_expected_output.txt testset_cpp_expected_output.txt
BINDIR = /usr/bin
MANDIR = /usr/man/man1
CATDIR = /usr/man/cat1
INSTALL = install -c
INSTALL_DATA = install -c -m 644

EMCC_OPTIONS = -sEXPORTED_FUNCTIONS=_run_from_js -sEXPORTED_RUNTIME_METHODS=ccall,cwrap -sENVIRONMENT=web -sWASM=0 -sINVOKE_RUN=0 -sMALLOC=emmalloc

# Ensure flex and bison are installed manually before running make (do this once manually)
# This should NOT be in the normal build process!

# Make sure that c++decl exists before symlink creation
cdecl: c++decl
	@echo "Checking if c++decl exists"
	if [ -f c++decl ]; then \
		echo "c++decl exists. Creating symlink."; \
		ln -sf c++decl cdecl; \
		chmod +x cdecl; \
	else \
		echo "Error: c++decl binary not found!"; \
		exit 1; \
	fi

# Build the c++decl executable
c++decl: cdgram.c cdlex.c cdecl.c
	@echo "Building c++decl"
	$(CC) $(CFLAGS) -o c++decl cdecl.c $(LIBS)
	@echo "Removing old cdecl"
	rm -f cdecl

# Process Lex and Yacc files
cdlex.c: cdlex.l
	lex cdlex.l && mv lex.yy.c cdlex.c

cdgram.c: cdgram.y
	yacc cdgram.y && mv y.tab.c cdgram.c

# Run tests
test: cdecl
	@./cdecl < testset | diff -U 3 - test_expected_output.txt \
		|| ( echo "** Test failed **" && false ) \
		&& echo "Tests passed"

test_cpp: c++decl
	./c++decl < testset++

# Install the cdecl binary
install: cdecl
	$(INSTALL) cdecl $(BINDIR)
	ln -sf cdecl $(BINDIR)/c++decl
	$(INSTALL_DATA) cdecl.1 $(MANDIR)
	$(INSTALL_DATA) c++decl.1 $(MANDIR)

# Clean up files
clean:
	rm -f cdgram.c cdlex.c cdecl y.output c++decl cdecl.js cdecl.js.mem cdecl.wasm

clobber: clean
	rm -f $(BINDIR)/cdecl $(BINDIR)/c++decl
	rm -f $(MANDIR)/cdecl.1 $(MANDIR)/c++decl.1
	rm -f $(CATDIR)/cdecl.1.gz

# Create cpio and shar archives
cdecl.cpio: $(ALLFILES)
	ls $(ALLFILES) | cpio -ocv > cdecl.cpio

cdecl.shar: $(ALLFILES)
	shar $(ALLFILES) > cdecl.shar

# Optional target for Emscripten (if using WebAssembly)
.PHONY: cdecl_emscripten
cdecl_emscripten: cdgram.c cdlex.c cdecl.c
	docker run \
		--rm   \
		-v ${PWD}:/src \
		-u $(id -u):$(id -g) \
		emscripten/emsdk \
		make cdecl.js
