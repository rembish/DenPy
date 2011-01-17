from os.path import basename
from struct import unpack

from singleton import Singleton

class Rom(object):
    __metaclass__ = Singleton
    
    PRGROM_PAGESIZE = 0x4000
    CHRROM_PAGESIZE = 0x1000
    TRAINER_SIZE = 0x200

    VERTICAL_MIRRORING = 0
    HORIZONTAL_MIRRORING = 1
    FOURSCREEN_MIRRORING = 2

    def __init__(self):
        self.filename = None

        self.rom_count = 0
        self.roms = []

        self.vrom_count = 0
        self.vroms = []

        self.battery_ram = None
        self.trainer = None

        self.mirroring = None
        self.four_screen = None

        self.mapper_type = None

        self.is_valid = None

    def load(self, filename):
        id = open(filename, 'rb')
        
        (
            signature, _x1a, self.rom_count, self.vrom_count,
            rom_control_byte_1, rom_control_byte_2, _x00000000
        ) = unpack('>3s5BQ', id.read(16))

        if signature != 'NES' and _x1a != 0x1a:
            raise Exception('Checking singnature "NES" failed')

        self.mirroring = rom_control_byte_1 & 0x01
        self.battery_ram = rom_control_byte_1 & 0x02
        is_trainer = rom_control_byte_1 & 0x04
        self.four_screen = rom_control_byte_1 & 0x08
        self.mapper_type = (rom_control_byte_1 >> 4) | (rom_control_byte_2 & 0xF0)

        if _x00000000 != 0x00000000:
            self.is_valid = False

        # For now skip the trainer if it exists.
        if is_trainer & 0x04:
            self.trainer = id.read(self.TRAINER_SIZE)

        for i in range(self.rom_count):
            self.roms.append(id.read(self.PRGROM_PAGESIZE))

        for i in range(self.vrom_count):
            self.vroms.append(id.read(self.CHRROM_PAGESIZE))

        id.close()

        if self.is_valid == None:
            self.is_valid = True

        self.filename = filename

    def get_mirrowing(self):
        if self.four_screen:
            return self.FOURSCREEN_MIRRORING

        if not self.mirroring:
            return self.HORIZONTAL_MIRRORING

        return self.VERTICAL_MIRRORING

    def reset(self):
        if self.filename:
            self.load(self.filename)

    def __repr__(self):
        return '<ROM:%s PRG-ROMs=%d CHR-ROMs=%d>' % (
            basename(self.filename or 'empty'),
            self.rom_count or 'no', self.vrom_count or 'no'
        )
