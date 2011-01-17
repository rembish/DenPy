from pprint import pprint
from nes import Nes

emulator = Nes()
emulator.load('../roms/tutor.nes')
pprint(emulator.__dict__)
