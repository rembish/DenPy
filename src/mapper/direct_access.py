from singleton import Singleton
from rom import Rom
from cpu import Cpu

class DirectAccess(object):
    __metaclass__ = Singleton
    name = 'Direct Access'

    def __init__(self, owner):
        self.owner = owner

    def __getitem__(self, address):
        pass

    def __setitem__(self, address, value):
        pass

    def load(self):
        self.load_prgrom()
        self.load_chrrom()
        self.load_batteryrom()

        #self.owner.cpu.requestIrq(self.owner.cpu.IRQ_RESET)

    def load_prgrom(self):
        self.load_rom_bank(0, 0x8000)
        self.load_rom_bank(int(Rom().rom_count > 1), 0xC000)

    def load_rom_bank(self, bank, address):
        rom = Rom()
        bank %= rom.rom_count
        Cpu().memory[address:address + rom.PRGROM_PAGESIZE] = rom.roms[bank]
