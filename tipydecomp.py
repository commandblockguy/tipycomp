import subprocess
import sys
import tempfile

def get_menu_pos(data):
    length = 0
    index = 4
    shift = 0
    while True:
        byte = data[index]
        length |= (byte & 0x7f) << shift
        index += 1
        shift += 7
        if byte & 0x80 == 0:
            break

    start = index + 1
    end = start + length

    return (start, end)

def dump_menu(data):
    start, end = get_menu_pos(data)
    menu = data[start:end-1]
    print(str(menu, encoding="utf8"))

def disasm(data, temp_dir):
    start, end = get_menu_pos(data)
    mpy_data = data[end:]
    mpy_filename = temp_dir + 'in.mpy'
    open(mpy_filename, 'wb').write(mpy_data)
    subprocess.run(["mpy-disasm/mpy-disasm", mpy_filename])

def main(mode, infile):
    temp_dir = tempfile.mkdtemp(prefix='tipycomp_')

    bin_filename = temp_dir + '/in.bin'

    subprocess.run(["convbin",
                    "-i", infile, "-j", "8x",
                    "-o", bin_filename, "-k", "bin"],
                    stdout=subprocess.DEVNULL)

    data = open(bin_filename, 'rb').read()

    if mode == 'menu':
        dump_menu(data)
    elif mode == 'disasm':
        disasm(data, temp_dir)
    else:
        print('Invalid mode ' + mode)
        print('Use "menu" or "disasm"')
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + __file__ + ' (menu|disasm) infile')
        exit(1)
    main(*sys.argv[1:])