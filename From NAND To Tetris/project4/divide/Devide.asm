// The program input will be at R13,R14 while the result R13/R14 will be store at R15.
// The remainder should be discarded.
// You may assume both numbers are positive.
// The program should have a running time logarithmic with respect to the input.
// Negative numbers are not permitted

@R15
M=0 // R15 = 0
@R13
D=M 
@REMAINDER
M=D // REMAINDER = R13
@R14
D=M
@PRODUCT
M=D // PRODUCT = R14
@1
D=A
@TERM
M=D // TERM = 1
@1111111111111111
@MAXTERM
M=A // MAXTERM = 1111111111111111
(WHILE)
	@TERM
	D=M
	@MAXTERM
	D=D-M
	@WHILE2
	D;JGE // BREAK ON TERM < MAXTERM
	@PRODUCT
	D=M
	@REMAINDER
	D=D-M
	@WHILE2
	D;JGE // BREAK PRODUCT<REMAINDER
	@PRODUCT
	M=M<< // PRODUCT *= 2
	@TERM
	M=M<< // TERM *= 2
	@WHILE
	0;JMP 

(WHILE2)
	@TERM
	D=M
	D=D-1
	@END
	D;JLT // JUMP IF TERM < 1

	@PRODUCT
	D=M
	@REMAINDER
	D=D-M
	@IF
	D;JLE
	(CONTINUE)
		@PRODUCT
		M=M>> // PRODUCT /= 2
		@TERM
		M=M>> // TERM /= 2
	@WHILE2
	0;JMP
	
(IF)
	@TERM
	D=M
	@R15
	M=M+D
	@PRODUCT
	D=M
	@REMAINDER
	M=M-D
	@CONTINUE
	0;JMP // RETURN
	
	
(END)
	