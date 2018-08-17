// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(RUNNING)
	@24576 // keyboard address
	D=M
	@PUT_ZERO
	D;JEQ
	@PUT_ONES
	0;JMP
	(CONTINUE)
		@PAINT_SCRREN
		0;JMP // Paint screen 
	@RUNNING
	0;JMP
		
(PUT_ONES)
	@R0
	M=-1 // R0 = 1111111111111111
	@CONTINUE
	0;JMP

(PUT_ZERO)
	@R0
	M=0 // R0 = 0
	@CONTINUE
	0;JMP

// Fill screen with the color in RAM[0] (-1 OR 0)
(PAINT_SCRREN)
	@SCREEN
	D=A
	@addr
	M=D // addr = 16384 (screen's base address)
	
	(LOOP)
		@addr
		D=M
		@24576
		D=D-A // D = D-24576
		@RUNNING
		D;JGE // if addr >= 24576
		
		@R0
		D=M
		@addr
		A=M
		M=D // RAM[addr] = RAM[0]
		
		@addr
		M=M+1 // addr = addr + 1
		@LOOP
		0;JMP