from glob import iglob
from os import getenv, makedirs, path, sep
from re import sub
from sys import argv

from dotenv import find_dotenv, load_dotenv
from pyAudioAnalysis import audioBasicIO, audioSegmentation

load_dotenv(find_dotenv())

try:
    if not path.isdir(getenv('OUTPUT_DIR')):
        makedirs(getenv('OUTPUT_DIR'))

    def escape_glob_brackets(globPattern):
        globPattern = sub(r'\[', '[[]', globPattern)
        globPattern = sub(r'(?<!\[)\]', '[]]', globPattern)
        return globPattern

    def process_path(globPattern):
        globPattern = escape_glob_brackets(globPattern)
        paths = iglob(globPattern, recursive=getenv('RECURSIVE_TRAVERSAL'))
        for p in paths:
            if path.isdir(p):
                process_path(p + sep + '*')
            else:
                extract_chorus(p)

    def extract_chorus(input):
        try:
            if not path.exists(input):
                return

            [sampling_rate, signal, song] = audioBasicIO.read_audio_file(input)
            [A1, A2, B1, B2, Smatrix] = audioSegmentation.music_thumbnailing(signal, sampling_rate, thumb_size=float(getenv('SNIPPET_LENGTH')))
            firstSegment = song[A1 * 1000:A2 * 1000]
            firstFaded = firstSegment.fade_in(1000).fade_out(1000)

            baseFilename = path.splitext(path.basename(input))[0]
            filename = path.join(getenv('OUTPUT_DIR'), baseFilename + getenv('SNIPPET_SUFFIX') + '.mp3')
            firstFaded.export(filename, format='mp3')
        except Exception as ex:
            print(ex)

    for f in argv[1:]:
        process_path(f)

except Exception as ex:
    print(ex)
