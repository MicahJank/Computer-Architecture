"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0x00] * 0xFF
        self.reg = [0] * 8
        self.branchtable = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL
        }
    
    def HLT(self):
        sys.exit()

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
    
    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])

    def MUL(self, register_a, register_b):
        self.reg[register_a] = self.reg[register_a] * self.reg[register_b]

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value


    # lets us programatically load the commands in from another file
    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) < 2:
            print("No path to file given.")
            print("e.g - filename path/to/file")
            sys.exit()

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')

                    possible_num = comment_split[0]

                    if possible_num == '':
                        continue
                
                    if possible_num[0] == "1" or possible_num[0] == "0":
                        num = possible_num[:8]
                        self.ram[address] = int(num, 2)
                        address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        try:
            self.branchtable[op](reg_a, reg_b)
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
        

        while self.pc <= len(self.ram):
            IR = self.ram[self.pc]
            num_of_ops = IR >> 6
            is_alu_op = IR >> 5 & 0b001 # if 0 false if 1 true
            pc_set = IR >> 4 & 0b0001 # 1 if instruction sets pc 0 if it doesnt
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # if the operation is an alu operation we should handle it there
            # otherwise we can use the branchtable directly from here
            if is_alu_op:
                self.alu(IR, operand_a, operand_b)
            else:
                self.branchtable[IR]()

            # pc needs to increment by 1 (for the current operation) + however many extra operands there will be
            self.pc += 1 + num_of_ops



