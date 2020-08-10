"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pc is the program counter and keeps track of where we are in the 
        self.pc = 0
        self.ram = [0x00] * 0xFF # <-- stores 256 bytes

        self.reg = [0] * 8 # <-- total of 8 registers

        # branchtable provides O(1) access to handler functions - 
        # prevents us from having to check the opcode value against EVERY possible function - (O(n) time complexity)
        self.branchtable = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL
        }
    
    # handler functions to store inside the branchtable #
    # HLT exits the program regardless of what is happening
    def HLT(self):
        sys.exit()

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
        
        # the while loop will run through all the instructions that need to be ran using the pc as a guide for where it is
        while self.pc <= len(self.ram):
            IR = self.ram[self.pc] # gets the instruction from the location in the ram
            # bitshift the instruction to the left 6 this will leave me with just the 2 digits left and from that i can
            # find out how many operands will be needed in combinartion with the initial one
            num_of_ops = IR >> 6 
            
            is_alu_op = IR >> 5 & 0b001 # 0 if false, 1 if true
            pc_set = IR >> 4 & 0b0001 # 1 if instruction sets pc, 0 if it doesnt

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # if the operation is an alu operation we should handle it there
            # otherwise we can use the branchtable directly from here
            if is_alu_op:
                self.alu(IR, operand_a, operand_b)
            else:
                # What is stored in the branchatable are functions which is why we can invoke this
                self.branchtable[IR]() 

            # pc needs to increment by 1 (for the current operation) + however many extra operands there will be
            self.pc += 1 + num_of_ops



