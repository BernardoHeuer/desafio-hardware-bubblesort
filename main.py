class MiniCPU:
    def __init__(self, mem):
        self.mem = mem[:]
        self.reg = [0, 0, 0, 0]
        self.pc = 0
        self.zf = 0
        self.running = True
        self.ciclo = 0

    def fetch(self):
        op = self.mem[self.pc]
        a = self.mem[self.pc + 1]
        b = self.mem[self.pc + 2]
        self.pc += 3
        return op, a, b

    def decode_execute(self, op, a, b):
        if op == 0x01:
            self.reg[a] = self.mem[b]
        elif op == 0x02:
            self.mem[b] = self.reg[a]
        elif op == 0x03:
            self.reg[a] = (self.reg[a] + self.reg[b]) & 0xFF
        elif op == 0x04:
            self.reg[a] = (self.reg[a] - self.reg[b]) & 0xFF
        elif op == 0x05:
            self.reg[a] = b
        elif op == 0x06:
            self.zf = 1 if self.reg[a] == self.reg[b] else 0
        elif op == 0x07:
            self.pc = a
        elif op == 0x08:
            if self.zf:
                self.pc = a
        elif op == 0x09:
            if not self.zf:
                self.pc = a
        elif op == 0x0A:
            self.running = False

    def trace(self, op, a, b):
        nomes = {1:'LOAD',2:'STORE',3:'ADD',4:'SUB',
                 5:'MOV',6:'CMP',7:'JMP',8:'JZ',9:'JNZ',10:'HALT'}
        nome = nomes.get(op, '???')

        print(f"Ciclo {self.ciclo}: {nome} {a},{b} | "
              f"R0={self.reg[0]} R1={self.reg[1]} "
              f"R2={self.reg[2]} R3={self.reg[3]} | "
              f"PC={self.pc} ZF={self.zf}")

    def run(self):
        while self.running and self.pc < 256:
            self.ciclo += 1
            op, a, b = self.fetch()
            self.decode_execute(op, a, b)
            self.trace(op, a, b)


def build_program():
    mem = [0] * 256
    pos = 0

    def instr(op, a, b):
        nonlocal pos
        mem[pos] = op
        mem[pos+1] = a
        mem[pos+2] = b
        pos += 3

    mem[0x10] = 40
    mem[0x11] = 10
    mem[0x12] = 30
    mem[0x13] = 20

    instr(0x05, 2, 1)
    instr(0x05, 3, 0)

    def compare_swap(addrA, addrB):
        nonlocal pos

        start = pos

        instr(0x01, 0, addrA)
        instr(0x01, 1, addrB)

        loop = pos

        instr(0x06, 0, 3)
        jz_end = pos
        instr(0x08, 0, 0)

        instr(0x06, 1, 3)
        jz_swap = pos
        instr(0x08, 0, 0)

        instr(0x04, 0, 2)
        instr(0x04, 1, 2)

        instr(0x07, loop, 0)

        swap_addr = pos

        instr(0x01, 0, addrA)
        instr(0x01, 1, addrB)
        instr(0x02, 0, addrB)
        instr(0x02, 1, addrA)

        end_addr = pos

        mem[jz_end+1] = end_addr
        mem[jz_swap+1] = swap_addr

    compare_swap(0x10, 0x11)
    compare_swap(0x11, 0x12)
    compare_swap(0x12, 0x13)

    compare_swap(0x10, 0x11)
    compare_swap(0x11, 0x12)

    compare_swap(0x10, 0x11)

    instr(0x0A, 0, 0)

    return mem


if __name__ == "__main__":
    mem = build_program()
    cpu = MiniCPU(mem)
    cpu.run()

    print("\nResultado:", cpu.mem[0x10:0x14])