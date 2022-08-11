#!/usr/bin/python

import sys

try:
  input = sys.argv[1]
  output = sys.argv[2]
except IndexError:
  sys.stderr.write("usage: %s input_file output_file\n" % sys.argv[0])
  sys.exit(-1)

data = open(input, "r").read().split("\n")
out = open(output, "w+")

output = ""
count = 0

device = None
serial = None

idLine = "* 1-Wire Device Name: "
serialLine = "* 1-Wire Device Address: "

for line in data:

  if line.startswith(idLine) and count == 0:
    device = line[len(idLine):]
    print("Found device: %s" % device)

  if line.startswith(serialLine) and count == 0:
    serial = line[len(serialLine):]
    print("Found serial: %s" % serial)

  # the lines starting with "Page xyz:" are what you want
  if line.startswith("Page "):
    if count == 0:
      count = count + 1
      continue
    line = line.split(": ")[1]
    # each line is 64 bytes long
    for i in range(0, 64, 2):
      byte = int(line[i:i+2], 16)
      output = output + chr(byte)

out.write(output)
out.close()
