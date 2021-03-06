"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
ADD = 0b10100000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

# flags
EFLAG = 0b01
GFLAG = 0b10
LFLAG = 0b11

class CPU:
    """Main CPU class."""

    def __init__(self): #, ram, register, im, iS, sp, pc, ir, mar, mdr, fl
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.im = 0
        self.iS = 0
        self.sp = 0xf4
        self.register[5] = self.im
        self.register[6] = self.iS
        self.register[7] = self.sp
        self.running = True
        self.pc = 0
        # self.ir = 0
        # self.mar = 0
        # self.mdr = 0
        self.fl = None

        self.instructions = {}
        self.instructions[HLT] = self.fxn_halt
        self.instructions[LDI] = self.fxn_load_integer
        self.instructions[PRN] = self.fxn_print
        self.instructions[MUL] = self.fxn_multiply
        self.instructions[PUSH] = self.fxn_push
        self.instructions[POP] = self.fxn_pop
        self.instructions[CALL] = self.fxn_call
        self.instructions[ADD] = self.fxn_add
        self.instructions[RET] = self.fxn_return
        self.instructions[CMP] = self.fxn_compare
        self.instructions[JMP] = self.fxn_jump
        self.instructions[JEQ] = self.fxn_jumpeq
        self.instructions[JNE] = self.fxn_jumpNeq


    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) < 2:
            raise Exception(
        'Missing second argument, file name / route, in command line.'
        )

        program = sys.argv[1]

        with open(program) as p:
            for line in p:
                line = line.split('#')
                if line[0] == '' or line[0] == '\n':
                    continue
                self.ram[address] = int(line[0], 2)
                address +=1
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        elif op == 'CMP':
            a = self.register[reg_a]
            b = self.register[reg_b]
            if a > b:
                self.fl = GFLAG
            elif a < b:
                self.fl = LFLAG
            else:
                self.fl = EFLAG
        else:
            raise Exception("Unsupported ALU operation")
    
    def fxn_add(self, reg, op0):
        self.alu('ADD', reg, op0)
        self.pc += 3
    
    def fxn_call(self, reg, op0):
        rcount = self.pc + 2
        self.sp -= 1
        self.ram[self.sp] = rcount
        self.pc = self.register[reg]
    
    def fxn_compare(self, op, op0):
        self.alu('CMP', op, op0)
        self.pc += 3
    
    def fxn_halt(self, op, op0):
        self.running = False
    
    def fxn_jump(self, op, op0):
        self.pc = self.register[op]
    
    def fxn_jumpeq(self, op, op0):
        if self.fl == EFLAG:
            self.pc = self.register[op]
        else:
            self.pc += 2
    
    def fxn_jumpNeq(self, op, op0):
        if self.fl != EFLAG:
            self.pc = self.register[op]
        else:
            self.pc += 2
    
    def fxn_load_integer(self, reg, int):
        if reg < 5:
            self.register[reg] = int
            self.pc += 3
        else:
            raise Exception(
        f'Register {reg} is reserved. Retry with a register value less than 5.'
        )
    
    def fxn_multiply(self, int, multiplicand):
        self.register[int] *= self.register[multiplicand]
        self.pc +=3
    
    def fxn_print(self, reg, op0):
        print(self.register[reg])
        self.pc +=2

    def fxn_pop(self, reg, op0):
        self.register[reg] = self.ram[self.sp]
        self.sp += 1
        self.sp &= 0xff
        self.pc += 2

    def fxn_push(self, reg, op0):
        self.sp -= 1
        self.sp &= 0xff
        self.ram[self.sp] = self.register[reg]
        self.pc += 2
    
    def fxn_return (self, op, op0):
        return_address = self.ram[self.sp]
        self.pc = return_address
        self.sp += 1
    
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
    
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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram_read(self.pc)
            operand = self.ram_read(self.pc + 1)
            operand_0 = self.ram_read(self.pc + 2)
            if ir not in self.instructions:
                raise Exception(
f'Unknown instruction {ir} at address {self.pc}. Please check ls8-spec.md in the ls8 repo.'
)
            else:
                fxn = self.instructions[ir]
                fxn(operand, operand_0)


# cpu = CPU()
# print(cpu.register)