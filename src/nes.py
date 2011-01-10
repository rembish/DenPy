from cpu import Cpu
from ppu import Ppu
from rom import Rom
from mapper import Mapper

class Nes(object):
    def __init__(self):
        self.cpu = Cpu(self)
        self.ppu = Ppu(self)

        self.rom = None
        self.memory = None

        self.is_running = False

    def reset(self):
        if self.memory:
            self.memory.reset()

        self.cpu.reset()
        self.ppu.reset()

    def start(self):
        pass
    
    def stop(self):
        pass
    
    def load(self, filename):
        if self.is_running:
            self.stop()

        self.rom = Rom(self)
        self.rom.load(filename)

        if self.rom.is_valid:
            self.memory = Mapper(self.rom.mapper_type)
            if not self.memory:
                raise Exception('Unknown mapper: %d' % self.rom.mapper_type)

            self.memory.load()
            self.ppu.set_mirroring(self.rom.get_mirrowing())

        return self.rom.is_valid

    def reload(self):
        if self.rom and self.rom.filename:
            self.load(self.rom.filename)
