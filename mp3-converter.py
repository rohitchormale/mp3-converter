#!/usr/bin/env python3


__version__ = "1.0.0"


"""
MP3 Converter v3
Convert your video files to audio with ease.

usage: mp3-converter.py <infile>|<indir> [outfile|outdir]

"""

import sys
import os
from subprocess import call


LOGLEVEL = "panic"
infiles = []


def walk_dir(indir, outdir):
    global infiles
    for root, dirs, files in os.walk(indir, topdown=False):
        for fname in files:
            # input path
            name, ext = os.path.splitext(fname)
            if ext in (".mp3", ".py"):
                continue
            infile = os.path.join(root, fname)
            # output path
            oname = "%s.%s" %(name, "mp3")
            outfile = os.path.join(outdir, oname)
            infiles.append((infile, outfile))


def walk_file(infile, outfile):
    infiles.append((infile, outfile))


def convert_files():
    for infile, outfile in infiles:
        print("Converting '%s' to '%s'" % (infile, outfile))
        call(["ffmpeg", "-hide_banner", "-loglevel", LOGLEVEL, "-nostats", "-i", infile, "-q:a", "0", "-map", "a", outfile])


def help(exit=True):
    sys.stderr.write("usage: mp3-converter.py <infile>|<indir> [outfile|outdir]\n")
    if exit:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        help()

    if len(sys.argv) == 2:
        infile = sys.argv[1]
        if not os.path.exists(infile):
            sys.stderr.write("Input file doesn't exists.\n")
            help()

        if os.path.isdir(infile):
            indir = infile
            outdir = "audio"
            if os.path.exists(outdir):
                if os.path.isdir(outdir):
                    walk_dir(indir, outdir)
                    convert_files()
                else:
                    sys.stderr.write("File already exists \n")
                    help()
            else:
                os.makedirs(outdir)
                walk_dir(indir, outdir)
                convert_files()

        else:
            name, ext = os.path.splitext(infile)
            if ext in ("mp3", "py"):
                print("Invalid file name")
                help()
            outfile = "%s.%s" % (name, "mp3")
            if os.path.exists(outfile):
                print("File already exists")
                help()
            else:
                walk_file(infile, outfile)
                convert_files()


    if len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        if not os.path.exists(infile):
            print("Input file doesn't exists")
            help()

        if os.path.isdir(infile):
            indir = infile
            outdir = outfile
            if os.path.exists(outdir):
                if os.path.isdir(outdir):
                    walk_dir(indir, outdir)
                    convert_files()
                else:
                    print("File already exists")
                    help()
            else:
                os.makedirs(outdir)
                walk_dir(indir, outdir)
                convert_files()

        else:
            name, ext = os.path.splitext(infile)
            if ext in ("mp3", "py"):
                print("Invalid file name")
                help()
            if os.path.exists(outfile):
                if os.path.isdir(outfile):
                    outfile = os.path.join(outfile, "%s.%s" % (os.path.basename(name), "mp3"))
                    walk_file(infile, outfile)
                    convert_files()
                else:
                    print("File already exists")
                    help()
            else:
                walk_file(infile, outfile)
                convert_files()
