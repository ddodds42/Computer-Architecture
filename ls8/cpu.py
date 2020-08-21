"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self): #, ram, register, im, iS, sp, pc, ir, mar, mdr, fl
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.im = 0
        self.iS = 0
        self.sp = 0
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
    
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
    
    def fxn_halt(self, op, op0):
        self.running = False
    
    def fxn_load_integer(self, reg, int):
        if reg < 5:
            self.register[reg] = int
            self.pc += 3
        else:
            raise Exception(
        f'Register {reg} is reserved. Retry with a register value less than 5.'
        )
    
    def fxn_print(self, reg, op0):
        print(self.register[reg])
        self.pc +=2


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
# cpu.fxn_load_integer(3, 25)
# cpu.fxn_halt()
# print(cpu.register, '\n', cpu.pc, '\n', cpu.running)

# print(cpu.ram[:10])
# cpu.load()
# print(cpu.ram[:10])

# cpu.ram_write(0b00001001, 0b11111111)
# print(cpu.ram[:10])
# print(cpu.ram_read(0b00001001))