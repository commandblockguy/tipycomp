import sys, tempfile, subprocess
# Needs the same version as the MicroPython version the CE uses - currently 1.9.3
import mpy_cross

def leb128(num):
	result = bytes()
	while num > 127:
		result += bytes([0x80 | (num & 127)])
		num >>= 7
	result += bytes([num])
	return result

def get_header(text):
	result = bytes('PYMP', encoding='utf8')
	result += leb128(len(text) + 1)
	result += bytes([2])
	result += text
	result += bytes([0])
	return result

def main(pyfile, menufile, outfile, name, args):
	temp_dir = tempfile.mkdtemp(prefix='tipycomp_')
	mpy_filename = temp_dir + '/out.mpy'
	mpy_cross.run(pyfile, '-o', mpy_filename, *args)

	text = open(menufile, 'rb').read()
	header_filename = temp_dir + '/header.bin'
	open(header_filename, 'wb').write(get_header(text))

	subprocess.run(["convbin",
	                "-i", header_filename,"-j", "bin",
	                "-i", mpy_filename, "-j", "bin",
	                "-o", outfile, "-k", "8xv",
	                "-n", name])


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Usage: ' + __file__ + ' pyfile menufile outfile varname (mpy-cross args)')
		exit(1)
	_, pyfile, menufile, outfile, name, *args = sys.argv
	main(pyfile, menufile, outfile, name, args)
