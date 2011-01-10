from struct import unpack

from ppu.tile import Tile

NES_PRGROM_PAGESIZE = 0x4000
NES_CHRROM_PAGESIZE = 0x1000
NES_TRAINER_SIZE = 0x200

class Rom(object):
    VERTICAL_MIRRORING = 0
    HORIZONTAL_MIRRORING = 1
    FOURSCREEN_MIRRORING = 2

    def __init__(self, owner):
        self.owner = owner
        self.filename = None

        self.rom_count = 0
        self.rom = []

        self.vrom_count = 0
        self.vrom = []
        self.tiles = []

        self.battery_ram = None
        self.trainer = None

        self.mirroring = None
        self.four_screen = None

        self.mapper_type = None

        self.is_valid = False

    def load(self, filename):
        id = open(filename, 'rb')
        
        (
            signature, _x1a, self.rom_count, self.vrom_count,
            rom_control_byte_1, rom_control_byte_2, _x00000000
        ) = unpack('>3s5BQ', id.read(16))

        if signature != 'NES' and _x1a != 0x1a:
            raise Exception('Checking singnature "NES" failed')

        self.vrom_count *= 2

        self.mirroring = rom_control_byte_1 & 0x01
        self.battery_ram = rom_control_byte_1 & 0x02
        is_trainer = rom_control_byte_1 & 0x04
        self.four_screen = rom_control_byte_1 & 0x08
        self.mapper_type = (rom_control_byte_1 >> 4) | (rom_control_byte_2 & 0xF0)

        if _x00000000 != 0x00000000:
            self.mapper_type &= 0xF

        # For now skip the trainer if it exists.
        if is_trainer & 0x04:
            self.trainer = id.read(NES_TRAINER_SIZE)

        for i in range(self.rom_count):
            self.rom.append(id.read(NES_PRGROM_PAGESIZE))

        for i in range(self.vrom_count):
            self.vrom.append(id.read(NES_CHRROM_PAGESIZE))
            self.tiles.append([Tile()] * 256)

            for j in range(len(self.vrom[i])):
                tile_index = j >> 4
                left_over = j % 16

                if left_over < 8:
                    self.tiles[i][tile_index].set_scanline(left_over,
                        self.vrom[i][j], self.vrom[i][i + 8])
                else:
                    self.tiles[i][tile_index].set_scanline(left_over - 8,
                        self.vrom[i][j - 8], self.vrom[i][i])

        id.close()

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

