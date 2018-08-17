// The program input will be at R14(starting address),R15(length of array).
// The program should sort the array starting at the address in R14 with length specified in R15.
// The sort is in descending order - the largest number at the head of the array.
// The array is allocated in the heap address 2048-16383.

@swapped // Boolean variable -> 1 if swap was occurred, 0 if not
M=0 // swapped = 0
@i
M=0 // i = 0
@R15
D=M
@n
M=D // n = R15
@R14
D=M
@arr
M=D // arr = RAM[R14]

(LOOP)
	@i
	D=M
	D=D+1
	@n
	D=D-M
	@RESET_LOOP
	D;JEQ // reset loop (i=0)
	
	@i
	D=M
	@arr
	D=M+D 
	@R0
	M=D // R0 = addr(arr[i])
	@R1
	M=D+1 // R1 = addr(arr[i+1])
	@R0
	A=M
	D=M // D = arr[i]
	@R1
	A=M
	D=D-M // D = arr[i] - arr[i+1]
	@SWAP
	D;JLT // SWAP(arr[i],arr[i+1])
	(CONTINUE_LOOP)
	@i
	M=M+1 // i++
	@LOOP
	0;JMP

(RESET_LOOP)
	@swapped
	D=M
	@END
	D;JEQ // Jump if swapped was not occurred
	@swapped
	M=0 // swapped = 0
	@i
	M=0 // i = 0
	@loop
	0;JMP

// Function thtat swaps RAM[RAM[R0]] with RAM[RAM[R1]], R0,R1 contain the addresses
(SWAP)
	@swapped
	M=1 // swapped = 1
	@R0
	A=M
	D=M
	@temp
	M=D // temp = RAM[RAM[R0]]
	@R1
	A=M
	D=M
	@R0
	A=M
	M=D // RAM[RAM[R0]] = RAM[RAM[R1]]
	@temp
	D=M
	@R1
	A=M
	M=D // RAM[RAM[R1]] = temp
	@CONTINUE_LOOP
	0;JMP
	
(END)
	