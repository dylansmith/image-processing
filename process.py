#from PIL import Image
import glob, os, subprocess
from optparse import OptionParser

def shellquote(path):
  return path.replace("\\ ", "")

imagemagick = os.path.abspath("./libs/convert.exe")
jpegtran = os.path.abspath("./libs/jpegtran.exe")
srcdir = "./img_input/"
outdir = "./img_output/"
quality = 80
sizes = {
  590: "450x590",
  160: "120x160",
  80: "60x80"
}

def process_dir(path):
  print path
  for f in glob.glob(path + "/*.jpg"):
    parts = os.path.basename(f).split("-")
    if len(parts) > 1:
      process_image(os.path.abspath(f), parts[0])


def process_image(path, code):
  print "---------------------------------------------------"
  print "processing: " + path

  if not os.path.isfile(path):
    print "invalid file:" + path
    return

  if not code:
    print "invalid code"
    return

  for h in sizes.keys():
    sizedir = os.path.join(outdir, sizes[h], code)
    if not os.path.isdir(sizedir):
      os.makedirs(sizedir)
    target = os.path.join(sizedir, os.path.basename(path))

    cmd_resize = "{0} \"{1}\" -colorspace RGB -resize x{2} -quality {3} \"{4}\"".format(imagemagick, os.path.abspath(path), h, quality, os.path.abspath(target))
    cmd_optimize = "{0} -copy none -optimize \"{1}\" \"{2}\"".format(jpegtran, os.path.abspath(target), os.path.abspath(target))
    subprocess.call(cmd_resize);
    subprocess.call(cmd_optimize);
    print "created:    " + target


#===============================================
parser = OptionParser()
parser.add_option("--src", dest="src", default=srcdir, help="the base path to start working from")
parser.add_option("--output", dest="output", default=outdir, help="the path to save to")
parser.add_option("--r", dest="recursive", default=0, help="process recursively")

(options, args) = parser.parse_args()

if options.src:
  srcdir = os.path.abspath(options.src)

if options.output:
  outdir = os.path.abspath(options.output)

if not os.path.isdir(srcdir):
  print "src directory not found:" + srcdir
  exit

if not os.path.isdir(srcdir):
  print "output directory not found:" + outdir
  exit

recursive = bool(options.recursive)

process_dir(srcdir)

if recursive:
  for dirname, dirnames, filenames in os.walk(srcdir):
    for subdirname in dirnames:
      path = os.path.abspath(os.path.join(srcdir, subdirname))
      process_dir(path)
