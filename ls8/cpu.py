"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0x00] * 0xFF
        self.reg = [0] * 8

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
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

    # takes a binary opcode and returns a string representation of the instructions (i.e - 0b00000001 would give back 'HLT')
    def decodeInstruction(self, opcode):
        if opcode == 0b00000001:
            return 'HLT'
        elif opcode == 0b10000010:
            return 'LDI'
        elif opcode == 0b01000111:
            return 'PRN'
        elif opcode == 0b10100000:
            return 'ADD'
        elif opcode == 0b10101000:
            return 'AND'
        elif opcode == 0b01010000:
            return 'CALL'
        elif opcode == 0b10100111:
            return 'CMP'
        elif opcode == 0b01100110:
            return 'DEC'
        elif opcode == 0b10100011:
            return 'DIV'
        elif opcode == 0b01100101:
            return 'INC'
        elif opcode == 0b01010010:
            return 'INT'
        elif opcode == 0b00010011:
            return 'IRET'
        elif opcode == 0b01010101:
            return 'JEQ'
        elif opcode == 0b01011010:
            return 'JGE'
        elif opcode == 0b01010111:
            return 'JGT'
        elif opcode == 0b01011001: 
            return 'JLE'
        elif opcode == 0b01011000:
            return 'JLT'
        elif opcode == 0b01010100:
            return 'JMP'
        elif opcode == 0b01010110:
            return 'JNE'
        elif opcode == 0b10000011:
            return 'LD'
        elif opcode == 0b10100100:
            return 'MOD'
        elif opcode == 0b10100010:
            return 'MUL'
        elif opcode == 0b00000000:
            return 'NOP'
        elif opcode == 0b01101001:
            return 'NOT'
        elif opcode == 0b10101010:
            return 'OR'
        elif opcode == 0b01000110:
            return 'POP'
        elif opcode == 0b01001000:
            return 'PRA'
        elif opcode == 0b01000101:
            return 'PUSH'
        elif opcode == 0b00010001:
            return 'RET'
        elif opcode == 0b10101100:
            return 'SHL'
        elif opcode == 0b10101101:
            return 'SHR'
        elif opcode == 0b10000100:
            return 'ST'
        elif opcode == 0b10100001:
            return 'SUB'
        elif opcode == 0b10101011:
            return 'XOR'
    def run(self):
        """Run the CPU."""
        # format of opcode is AABCDDDD
        # AA - Number of operands for this opcode, 0-2
        # B - 1 if this is an ALU operation
        # C - 1 if this instruction sets the PC
        # DDDD - Instruction identifier
        
        for instruction in self.ram:
            IR = self.ram[self.pc]
            command = self.decodeInstruction(IR)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # how much should the pc increment by
            # always defaults to 1
            pc_increment = 1

            # first checking for an LDI operation - according to readme
            # this should set the given position to the given number
            if command == 'LDI':
                self.reg[operand_a] = operand_b
                pc_increment = pc_increment + 2
            elif command == 'PRN': # <- PRN
                print(self.reg[operand_a])
                pc_increment = pc_increment + 1
            elif command == 'HLT': #<- HLT
                sys.exit()
            
            # update the pc so we can get the next set of instructions
            self.pc += pc_increment



