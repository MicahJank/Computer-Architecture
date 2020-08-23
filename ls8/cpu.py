"""CPU functionality."""

import sys
import time

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pc is the program counter and keeps track of where we are in the 
        self.pc = 0
        self.ram = [0x00] * 0xFF # <-- stores 256 bytes
        self.running = True

        self.reg = [0] * 8 # <-- total of 8 registers

        # register 7 is reserved for the stack pointer and the initial place where the SP points is at F4
        self.reg[7] = 0xF4

        # flags register
        self.fl = 0b00000000

        # branchtable provides O(1) access to handler functions - 
        # prevents us from having to check the opcode value against EVERY possible function - (O(n) time complexity)
        self.branchtable = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b00010001: self.RET,
            0b01010000: self.CALL,
            0b10100000: self.ADD,
            0b10000100: self.ST,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010110: self.JNE,
            0b01010101: self.JEQ,
            0b10101000 : self.AND,
            0b10101010 : self.OR,
            0b01101001 : self.NOT,
            0b10100100 : self.MOD,
            0b10101100 : self.SHL,
            0b10101101 : self.SHR,
            0b10101011 : self.XOR,
        }

    def XOR(self, regA, regB):
        self.reg[regA] = self.reg[regA] ^ self.reg[regB]

    def SHR(self, regA, regB):
        self.reg[regA] = self.reg[regA] >> self.reg[regB]

    def SHL(self, regA, regB):
        self.reg[regA] = self.reg[regA] << self.reg[regB]

    def MOD(self, regA, regB):
        if self.reg[regB] == 0:
            print("ERROR: Cannot divide by 0")
            self.HLT()
        else:
            self.reg[regA] = self.reg[regA] % self.reg[regB] 

    def NOT(self, register, _):
        self.reg[register] = ~self.reg[register]

    def OR(self, regA, regB):
        self.reg[regA] = self.reg[regA] | self.reg[regB]

    def AND(self, regA, regB):
        self.reg[regA] = self.reg[regA] & self.reg[regB]
    
    # handler functions to store inside the branchtable #
    # HLT exits the program regardless of what is happening
    def HLT(self):
        self.running = False

    def ST(self):
        register_a = self.ram_read(self.pc + 1)
        register_b = self.ram_read(self.pc + 2)
        b_value = self.reg[register_b]
        a_address = self.reg[register_a]

        self.ram_write(b_value, a_address)

    # takes a value and stores it inside a register
    def LDI(self):
        operand_a = self.ram_read(self.pc + 1) # the register number
        operand_b = self.ram_read(self.pc + 2) # the value to store
        self.reg[operand_a] = operand_b
    
    # Prints the value located at the register
    def PRN(self):
        operand_a = self.ram_read(self.pc + 1) # the register number
        print(self.reg[operand_a])

    # Multiplies to register values together and assigns the result to a register
    def MUL(self, register_a, register_b):
        self.reg[register_a] = self.reg[register_a] * self.reg[register_b]
    
    # compares the values in register a with the value in register b
    def CMP(self, register_a, register_b):
        # print(self.reg[register_a], self.reg[register_b])
        if self.reg[register_a] == self.reg[register_b]:
            self.fl = 0b00000001
            return
        else:
            self.fl = 0b00000000
            
        if self.reg[register_a] > self.reg[register_b]:
            self.fl = 0b00000010
            return
        else:
            self.fl = 0b00000000
        
        if self.reg[register_a] < self.reg[register_b]:
            self.fl = 0b00000100
            return
        else:
            self.fl = 0b00000000

    # pushes the value of the given register to the stack
    def PUSH(self):
        reg_num = self.ram_read(self.pc + 1)
        self.reg[7] -= 1
        SP = self.reg[7]
        value = self.reg[reg_num]

        self.ram_write(value, SP)

    def POP(self):
        reg_num = self.ram_read(self.pc + 1)
        SP = self.reg[7]
        self.reg[reg_num] = self.ram_read(SP)
        self.reg[7] += 1

    def RET(self):
        SP = self.reg[7]
        return_address = self.ram_read(SP)
        self.reg[7] += 1

        self.pc = return_address
    
    def CALL(self):
        # set where we need to return to
        next_instructions = self.pc + 2
        self.reg[7] -= 1
        SP = self.reg[7]
        # return_address = self.ram_read(self.pc + 2)
        self.ram_write(next_instructions, SP)

        # set the pc where the function we are calling is
        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]
    
    def ADD(self, register_a, register_b):
        self.reg[register_a] += self.reg[register_b]
    
    def JMP(self):
        register = self.ram_read(self.pc + 1)
        self.pc = self.reg[register]
    
    def JNE(self):
        register = self.ram_read(self.pc + 1)
        if self.fl & 0b00000001 == False:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def JEQ(self):
        register = self.ram_read(self.pc + 1)
        if self.fl & 0b00000001:
            self.pc = self.reg[register]
        else:
            self.pc += 2



    #                       #                     #

    # returns a location in the ram based on the address passed to it
    def ram_read(self, address):
        return self.ram[address]
    
    # sets a value to the location in ram based on the address and value passed to it
    def ram_write(self, value, address):
        self.ram[address] = value


    # lets us programatically load the commands in from another file
    def load(self):
        """Load a program into memory."""

        address = 0

        # the input from the user should be of length 2 or more if it was entered correctly
        if len(sys.argv) < 2:
            print("No path to file given.")
            print("e.g - filename path/to/file")
            sys.exit()

        try:
            # Open the file
            with open(sys.argv[1]) as file:
                # loop over the lines in the file
                for line in file:
                    # return a list from the lines in the file wherever a comment # appears
                    comment_split = line.split('#')

                    # grab the first item in the list
                    possible_num = comment_split[0]

                    # if it is empty we can skip
                    if possible_num == '':
                        continue
                    
                    # next check to see if the first char in the string is a 1 or 0
                    if possible_num[0] == "1" or possible_num[0] == "0":
                        # if it is we know the length of each opcode should be 8 so we slice to the 8th index
                        num = possible_num[:8]
                        # this will store the opcode/num in the ram at the address location
                        self.ram[address] = int(num, 2)

                        # increase the address
                        address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')


    # this runs for certain functions that the alu should handle
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        try:
            self.branchtable[op](reg_a, reg_b) # <-- these functions take in arguments
        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        except:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # format of opcode is AABCDDDD
        # AA - Number of operands for this opcode, 0-2
        # B - 1 if this is an ALU operation
        # C - 1 if this instruction sets the PC
        # DDDD - Instruction identifier
        
        # set up timer
        # time_start = time.time()

        # the while loop will run through all the instructions that need to be ran using the pc as a guide for where it is
        while self.running:
            # check and see if the IS register is set and interrupts are enabled
            # if self.reg[6]:
            #     masked_interrupts = self.reg[5] & self.reg[6]
            #     interrupt_happened = 0
            #     for i in range(8):
            #         interrupt_happened = ((masked_interrupts >> i) & 1) == 1
            #         if interrupt_happened:
            #             break
                
            #     if interrupt_happened:
            #         self.reg[6] = 0


            # check each to see if a second has elapsed or not
            # if time.time() - time_start >= 1:
            #     # set bit 0 of the IS register
            #     self.reg[6] = 0b00000001 
            #     time_start = time.time() # restet the time

            IR = self.ram[self.pc] # gets the instruction from the location in the ram
            # bitshift the instruction to the left 6 this will leave me with just the 2 digits left and from that i can
            # find out how many operands will be needed in combinartion with the initial one
            num_of_ops = IR >> 6 
            
            is_alu_op = IR >> 5 & 0b001 # 0 if false, 1 if true
            pc_set = IR >> 4 & 0b0001 # 1 if instruction sets pc, 0 if it doesnt


            # if the operation is an alu operation we should handle it there
            # otherwise we can use the branchtable directly from here
            if is_alu_op:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu(IR, operand_a, operand_b)
            else:
                # What is stored in the branchatable are functions which is why we can invoke this
<<<<<<< HEAD
                self.branchtable[IR]() 

            # pc needs to increment by 1 (for the current operation) + however many extra operands there will be
            self.pc += 1 + num_of_ops 
=======
                try:
                    self.branchtable[IR]()
                except:
                    print("opcode: ", bin(self.ram[self.pc]))
            # some instructions set the pc themself, in those cases we should increment the pc
            if pc_set == 0:
                # pc needs to increment by 1 (for the current operation) + however many extra operands there will be
                self.pc += 1 + num_of_ops
>>>>>>> 067dadd85b590d29e2e03f49af9ea38df468a85a



