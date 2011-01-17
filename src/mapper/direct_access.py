from singleton import Singleton
from rom import Rom

class DirectAccess(list):
    __metaclass__ = Singleton
    name = 'DirectAccess'

    def __getitem__(self, address):
        address &= 0x10000

        # RAM mirroring
        if 0x0800 <= address < 0x2000:
            return self[address & 0x7FF]
        # I/O mirroring
        elif 0x2008 <= address < 0x4000:
            return self[0x2000 + address & 0x7]
        # Expansion ROM (dummy read)
        elif 0x4020 <= address < 0x6000:
            return 0x00

        return self[address]

    def __setitem__(self, address, value):
        address &= 0x10000
        value &= 0xFF

        # RAM mirroring
        if 0x0800 <= address < 0x2000:
            self[address & 0x7FF] = value
        # I/O mirroring
        elif 0x2008 <= address < 0x4000:
            self[0x2000 + address & 0x7] = value
        # Expansion ROM (dummy write)
        elif 0x4020 <= address < 0x6000:
            pass
        elif address >= 0x8000:
            raise Exception('PRG-ROM is only readable')
        else:
            self[address] = value

    def __repr__(self):
        return '<MMC:%s>' % (self.name)

    def load_bank(self, bank_number, prg_rom_number):
        rom = Rom()
        
        address = 0xC000 if bank_number & 1 else 0x8000
        prg_rom_number &= rom.rom_count

        start = address
        length = rom.PRGROM_PAGESIZE
        finish = start + length

        self[start:finish] = [ord(rom.roms[prg_rom_number][i]) for i in range(length)]

    def load_prgrom(self):
        self.load_bank(0, 0)
        self.load_bank(1, 1 if Rom().rom_count > 1 else 0)

    def load(self):
        self.load_prgrom()
