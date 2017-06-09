#!/usr/bin/python3
import sys
import os
import os.path
import subprocess
from shutil import copyfile
from optparse import OptionParser

opt_parser = OptionParser()

opt_parser.add_option('-s', '--sizes',
        action='store',
        type='str',
        dest='sizes',
        default='32,48,96,128,scalable',
        )

opt_parser.add_option('-o', '--output-pattern',
        action='store',
        type='str',
        dest='output_pattern',
        default='icons/hicolor/<size2>/apps'
        )

(options, args) = opt_parser.parse_args()

svg_file = args[0]

output_pattern = options.output_pattern
sizes_str = options.sizes
sizes=sizes_str.split(',')

name = os.path.splitext(os.path.basename(svg_file))[0]

def svg2png(svg_file, output, size):
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), '-o', output, svg_file ])

def get_filename(pattern, size, name):
    if size == 'scalable':
        size1 = size
        size2 = size
    else:
        # size is num
        size1 = size
        size2 = size + 'x' + size

    if '<size1>' in pattern:
        pattern = pattern.replace('<size1>', size1, 1)
    elif '<size2>' in pattern:
        pattern = pattern.replace('<size2>', size2, 1)
    else:
        raise Exception('no found <sizeX> in pattern %s' % pattern)
    return os.path.join(pattern, name)

# main()
print("src ", svg_file, os.path.getsize(svg_file))
for size in sizes:
    ext = '.png'
    if size == 'scalable':
        ext = '.svg'

    output = get_filename(output_pattern, size , name + ext)
    os.makedirs( os.path.dirname(output), mode=0o755, exist_ok=True)

    if ext == '.png':
        svg2png(svg_file, output, int(size))
    else:
        copyfile(svg_file, output)
    print(output, os.path.getsize(output))

