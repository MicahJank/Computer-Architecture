PRINT_TIM      =  0b00000001
HALT           =  0b00000010
PRINT_NUM      =  0b01000011  # command 3
SAVE           =  0b10000100
PRINT_REGISTER =  0b01000101
ADD            =  0b10000110  # command 6
​
​
# Rules of our  game
## we store everything in memory
## we move our PC to step through memory, and execute commands
​
memory = [
    PRINT_TIM,  
    PRINT_TIM,
    PRINT_NUM, 
    99,
    SAVE,        # <--- PC
    42,  # number to save
    2,   # register to save into
    SAVE,
    42,  # number to save
    3,   # into R3
    ADD, # registers[2] = registers[2] + registers[3]
    2,   # Register index
    3,   # also index
    PRINT_REGISTER,  # should print 84
    2,
    HALT, 
          ]
​
running = True
pc = 0
​
​
​
# Memory bus
## a bunch of wires that the CPU uses to send an address to RAM
## also a data bus: CPU sends data to RAM, RAM sends data to CPU
##     CPU
##  ||||||||
##  ||||||||
##  ||||||||
##     RAM
​
# 0b00000001
# 0b00000010
# 0b11111111
​
​
​
# save the number 42 into R2
# what arguments does SAVE require?
​
# registers (use as variables)
# R0-R7
registers = [None] * 8
​
while running:
​
    command = memory[pc]
​
    num_operands = command >> 6
​
    if command == PRINT_TIM:
        print("Tim!")
​
    if command == PRINT_NUM:
        number_to_print = memory[pc + 1]
        print(number_to_print)
​
    if command == SAVE:
        num = memory[pc + 1]
        index = memory[pc + 2]
        registers[index] = num
​
    if command == PRINT_REGISTER:
        reg_idx = memory[pc + 1]
        print(registers[reg_idx])
​
    if command == ADD:
        first_reg_idx = memory[pc + 1]
        second_reg_idx = memory[pc + 2]
​
        registers[first_reg_idx] += registers[second_reg_idx]
​
    if command == HALT:
        running = False
​
    # what if we set the pc directly?
    pc += num_operands + 1