import os, sys, time

# CAPRICORN CLASS
class Capricorn:
    def __init__(self, filename: str, block_size: int):
        try:
            self.filename = filename
            # Read file:
            self.buffer = open(filename, "rb").read()
            # Set block size:
            self.block_size = block_size
        except Exception as error:
            print("\033[91m  {0}\033[00m".format(str(error)))

    def split(self, path):
        print("Splitting \033[93m{0}\033[00m".format(self.filename))
        blocks = int(len(self.buffer) / self.block_size)
        for b in range(1, blocks):
            buf = self.buffer[:b * self.block_size]
            output_path = os.path.join(path, "{0}_{1}".format(self.filename, b))
            print("\033[93m>\033[00m Now on block {0}/{1}".format(b, blocks - 1))
            # Block file:
            bf = open(output_path, "wb")
            bf.write(buf)
            bf.close()
        print("Done.")

# START SCRIPT:
if __name__ == "__main__":
    print("\033[93m                           .__")
    print("  ____ _____  _____________|__| ____  ___________  ____")
    print("_/ ___\\\__  \ \____ \_  __ \  |/ ___\/  _ \_  __ \/    \ ")
    print("\  \___ / __ \|  |_> >  | \/  \  \__(  <_> )  | \/   |  \ ")
    print(" \___  >____  /   __/|__|  |__|\___  >____/|__|  |___|  /")
    print("     \/     \/|__|                 \/                 \/\033[00m\n")

    if len(sys.argv) != 3:
        print("\033[93m  * Usage:\033[00m {0} <filename> <block size>".format(sys.argv[0]))
    else:
        # Try to run:
        try:
            splt = Capricorn(sys.argv[1], int(sys.argv[2]))
            splt.split(os.getcwd())
        except Exception as error:
            print("\033[91m  {0}\033[00m".format(str(error)))
