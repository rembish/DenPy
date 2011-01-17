from mapper import Mapper

from py65.devices import mpu6502
from py65.utils.conversions import itoa

class Cpu(mpu6502.MPU):
    INTERRUPT_IRQ = 1
    INTERRUPT_NMI = 2
    INTERRUPT_RESET = 4

    def __init__(self, debug=False):        
        mpu6502.MPU.__init__(self, memory=Mapper(), pc=0x8000, debug=debug)
        self.name = '2a03'
        self.irq = None

    def __repr__(self):
        return '<CPU:%s PC=%04X A=%02X X=%02X Y=%02X SP=%02X NV-B-IZC=%s>' % (
            self.name, self.pc, self.a, self.x, self.y, self.sp + 0x0100,
            itoa(self.p, 2).rjust(8, '0')
        )

    def step(self):
        # Process interruption before command
        if self.irq:
            flags = self.p ^ self.ZERO

            if self.irq == self.INTERRUPT_IRQ:
                # If disabled I flag
                if not (self.p & self.INTERRUPT):
                    self.do_irq(flags)
            elif self.irq == self.INTERRUPT_NMI:
                self.do_nmi(flags)
            elif self.irq == self.INTERRUPT_RESET:
                self.do_reset()
            
            self.irq = None

        return mpu6502.MPU.step()

    def request_irq(self, type):
        if self.irq and self.irq == self.IrqTo:
            return

        self.irq = type

    def do_irq(self, flags):
        self.stPushWord(self.pc + 1)
        self.stPush(flags)

        self.p |= self.INTERRUPT
        self.p &= ~self.BREAK

        self.pc = self.WordAt(self.IrqTo)

    def do_nmi(self, flags):
        # Check if 7 bit in PPU Control Register 1 is set
        if self.ByteAt(0x2000) & 0x80:
            self.stPushWord(self.pc + 1)
            self.stPush(flags)

            self.pc = self.WordAt(self.NMITo)

    def do_reset(self):
        self.pc = self.WordAt(self.ResetTo)
