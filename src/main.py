from nes import Nes

emulator = Nes()
emulator.load('../roms/Tetris_(U)_[!].nes')
print emulator.__dict__
