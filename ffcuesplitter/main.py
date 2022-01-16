"""
First release: January 16 2022

Name: main.py
Porpose: provides an argparser interface for FFcuesplitter class
Platform: MacOs, Gnu/Linux, FreeBSD
Writer: jeanslack <jeanlucperni@gmail.com>
license: GPL3
Rev: January 16 2022
Code checker: flake8 and pylint
####################################################################

This file is part of ffcuesplitter.

    ffcuesplitter is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ffcuesplitter is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ffcuesplitter.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse

from ffcuesplitter.datastrings import informations
from ffcuesplitter.cuesplitter import FFCueSplitter
from ffcuesplitter.str_utils import msgdebug, msgend
from ffcuesplitter.exceptions import (InvalidFileError,
                                     ParserError,
                                     FFCueSplitterError
                                     )

# data strings
INFO = informations()
DATA = INFO[0]


def main():
    """
    Defines and evaluates positional arguments
    using the argparser module.
    """
    parser = argparse.ArgumentParser(prog=DATA['prg_name'],
                                     description=DATA['short_decript'],
                                     # add_help=False,
                                     )
    parser.add_argument('--version',
                        help="Show the current version and exit",
                        action='version',
                        version=(f"ffcuesplitter v{DATA['version']} "
                                 f"- {DATA['release']}"),
                        )
    parser.add_argument('-i', '--input-cuefile',
                        metavar='IMPUTFILE',
                        help=("An absolute or relative CUE sheet file, "
                              "example: -i 'mycuesheetfile.cue'"),
                        action="store",
                        required=False,
                        )
    parser.add_argument('-f', '--format-type',
                        choices=["wav", "wv", "flac", "mp3", "ogg", "m4a"],
                        help=("Preferred audio format to output, "
                              "default is 'flac'"),
                        required=False,
                        default='flac',
                        )
    parser.add_argument("-o", "--output-dir",
                        action="store",
                        dest="outputdir",
                        help=("Absolute or relative destination path for "
                              "output files. If a specified destination "
                              "folder does not exist, it will be created "
                              "automatically. By default it is the same "
                              "path location as IMPUTFILE"),
                        required=False,
                        default='.'
                        )
    parser.add_argument("-ow", "--overwrite",
                        choices=["ask", "never", "always"],
                        dest="overwrite",
                        help=("Overwrite files on destination if they exist, "
                              "Default is `ask` before proceeding"),
                        required=False,
                        default='ask'
                        )
    parser.add_argument("--ffmpeg_url",
                        metavar='URL',
                        help=("Specify a custom ffmpeg path, "
                              "e.g. '/usr/bin/ffmpeg', Default is `ffmpeg`"),
                        required=False,
                        default='ffmpeg'
                        )
    parser.add_argument("--ffmpeg_loglevel",
                        choices=["error", "warning", "info",
                                 "verbose", "debug"],
                        help=("Specify a ffmpeg loglevel, "
                              "Default is `warning`"),
                        required=False,
                        default='warning'
                        )
    parser.add_argument("--ffmpeg_add_params",
                        metavar="'PARAMS ...'",
                        help=("Additionals ffmpeg parameters, as 'codec "
                              "quality', etc. Note, all additional parameters "
                              "must be quoted."),
                        required=False,
                        default=''
                        )
    parser.add_argument("--ffprobe_url",
                        metavar='URL',
                        help=("Specify a custom ffprobe path, "
                              "e.g. '/usr/bin/ffprobe', Default is `ffprobe`"),
                        required=False,
                        default='ffprobe'
                        )
    parser.add_argument("--dry",
                        action='store_true',
                        help=("Perform the dry run with no "
                              "changes done to filesystem."),
                        required=False,
                        )
    args = parser.parse_args()

    if args.input_cuefile:
        kwargs = {'filename': args.input_cuefile}
        kwargs['outputdir'] = args.outputdir
        kwargs['suffix'] = args.format_type
        kwargs['overwrite'] = args.overwrite
        kwargs['ffmpeg_url'] = args.ffmpeg_url
        kwargs['ffmpeg_loglevel'] = args.ffmpeg_loglevel
        kwargs['ffmpeg_add_params'] = args.ffmpeg_add_params
        kwargs['ffprobe_url'] = args.ffprobe_url
        kwargs['dry'] = args.dry

        try:
            split = FFCueSplitter(**kwargs)
            split.open_cuefile()
            split.do_operations()

        except (InvalidFileError, ParserError, FFCueSplitterError) as error:
            msgdebug(err=f"{error}")
        else:
            msgend(done=True)
    else:
        parser.error("Requires an INPUTFILE, please provide it")


if __name__ == '__main__':
    main()