"""CPU functionality."""

import sys

PRN = 0b01000111
LDI = 0b10000010
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.sp = 7
        self.program_filename = ""

        self.branchtable = {}
        self.branchtable[HLT] = self.handle_halt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop

    def load(self):
        """Load a program into memory."""
        try:
            address = 0
            with open(self.program_filename) as f:
                for lines in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if len(num) == 0:
                        continue

                    value = int(num, 2)
                    self.ram[address] = value
                    address += 1

            with open(self.program_filename) as f:
                for line in f:
                    comment_split = line.spit("#")
                    num = comment_split[0].strip()

                    if len(num) == 0:
                        continue
                        value = int(num, 2)
                        self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        IR = self.ram[self.pc]

        if len(sys.argv) != 2:
            print('Usage: cpy.py filename')
            sys.exit(1)

        self.program_filename = sys.argv[1]
        self.load()

        while self.running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.branch_table[IR](operand_a, operand_b)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def handle_halt(self, op_a, op_b):
        self.running = False

    def handle_ldi(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc += 3

    def handle_prn(self, op_a, op_b):
        print(self.reg[op_a])
        self.pc += 2

    def handle_mul(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)
        self.pc += 3

    def handle_push(self, op_a, op_b):
        reg = self.ram_read(self.pc + 1)
        val = self.reg[reg]
        self.reg[self.sp] -= 1
        self.ram_write(val, self.reg[self.sp])
        self.pc += 2

    def handle_pop(self, op_a, op_b):
        reg = self.ram_read(self.pc + 1)
        val = self.ram_read(self.reg[self.sp])
        self.reg[reg] = val
        self.reg[self.sp] += 1
        self.pc += 2


cpu = CPU()
cpu.load()
# cpu.run()
