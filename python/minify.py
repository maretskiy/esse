#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys


class MinifierError(Exception):
    pass


class Minifier():
    """Minify and concatenate assets files."""

    version = 1.0

    def __error(self, message):
        raise MinifierError(message)

    def process_css(self, css):
        """Minify CSS."""

        # Triggers
        t_expect_smth = 0
        t_in_selector = 1           # selector...
        t_in_cssblock = 2           # selector {...
        t_in_cssvalue = 3           # selector {property:...
        c_noncomment = 0
        c_expect_startcomment = 1   # /...
        c_in_comment = 2            # /*...
        c_expect_endcomment = 3     # /*...*...

        # Init
        minified = ''
        position = 0
        previous = None
        whitespaces = (' ', '\t', '\n')
        t = t_expect_smth
        c = c_noncomment

        for i in css:
            position += 1

            # Comments
            if c == c_expect_startcomment:
                if i == '*':
                    c = c_in_comment
                else:
                    c = c_noncomment
                    minified += '/' + i
                continue

            elif c == c_in_comment:
                if i == '*':
                    c = c_expect_endcomment
                continue

            elif c == c_expect_endcomment:
                if i == '/':
                    c = c_noncomment
                elif i == '*':
                    pass
                else:
                    c = c_in_comment
                continue

            elif i == '/':
                c = c_expect_startcomment
                continue

            # css
            if t == t_expect_smth:
                if i not in whitespaces:
                    t = t_in_selector
                    minified += i
            elif t == t_in_selector:
                if i == '{':
                    t = t_in_cssblock
                    minified += i
                elif i in whitespaces:
                    if previous not in whitespaces:
                        minified += ' '
                else:
                    minified += i

            elif t == t_in_cssblock:
                if i == ':':
                    t = t_in_cssvalue
                    minified += i
                elif i == '}':
                    t = t_expect_smth

                    # Remove semicolon if exists
                    if minified.endswith(';'):
                        minified = minified[0:-1]

                    minified += i + '\n' # newline!
                elif i not in whitespaces:
                    minified += i

            elif t == t_in_cssvalue:
                if i == ';':
                    t = t_in_cssblock
                    minified += i
                elif i in whitespaces:
                    if previous not in whitespaces \
                            and previous != ':' \
                            and previous != ',':
                        minified += ' '
                else:
                    minified += i

            previous = i

        return minified

    def process_js(self, js):
        """Minify JavaScript."""

        def minify_line(line):
            return line.strip() + '\n'

        # Triggers
        t_nl_expect_smth = 0
        t_code = 1
        t_expect_comment = 2                # /
        t_comment = 3                       # /* ...
        t_comment_expect_nl = 4             # // ...
        t_comment_expect_keepcomment = 5    # /*!
        t_keepcomment = 6                   # /*! ...

        # Init
        minified = ''
        position = 0
        previous = None
        line = ''
        whitespaces = (' ', '\t')
        t = t_nl_expect_smth

        for i in js:

            position += 1
            line += i

            if i == '\n':
                if t == t_code:
                    t = t_nl_expect_smth
                    minified += minify_line(line)
                elif t == t_keepcomment:
                    minified += minify_line(line)
                elif t == t_comment_expect_nl:
                    t = t_nl_expect_smth
                line = ''

            elif t == t_nl_expect_smth:
                if i == '/':
                    t = t_expect_comment
                elif i not in whitespaces:
                    t = t_code

            elif t == t_expect_comment:
                if i == '/':
                    t = t_comment_expect_nl
                elif i == '*':
                    t = t_comment_expect_keepcomment

            elif t == t_comment_expect_keepcomment:
                if i == '!':
                    t = t_keepcomment
                else:
                    t = t_comment

            elif t == t_comment:
                if i == '/' and previous == '*':
                    t = t_nl_expect_smth
                    line = ''

            elif t == t_keepcomment:
                if i == '/' and previous == '*':
                    t = t_nl_expect_smth
                    minified += minify_line(line)
                    line = ''

            previous = i

        return minified

    def concat(self, data_type, input_files):
        """Concatenate and minify given files.

        :param data_type: str, data type to minify
        :param input_files: list of input files
        :returns: str, concatenated result
        """

        minifier = getattr(self, 'process_%s' % data_type)

        cat = ''
        for f in input_files:
            if not os.path.isfile(f):
                self.__error("file not found: %s" % f)
            with open(f) as fd:
                cat += (fd.read() + '\n')

        return minifier(cat)


if __name__ == '__main__':

    # FIXME: Use argparse

    if len(sys.argv) < 4:
        sys.exit(
            "Usage: %s css|js <out_file> <in_file1> <in_file2>..."\
                 % os.path.basename(sys.argv[0]))

    minifier = Minifier()
    file_out = sys.argv[2]
    try:
        data = minifier.concat(sys.argv[1], sys.argv[3:])
    except MinifyError as e:
        sys.exit("error: %s" % e)

    # Save data to file
    overwritten = False
    if os.path.isfile(file_out):
        overwritten = True
    elif os.path.exists(file_out):
        sys.exit("error: bad output file: %s" % file_out)
    else:
        dirname = os.path.dirname(file_out)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
    try:
        with open(file_out, 'w') as fd:
            fd.write(data)
    except IOError as e:
        sys.exit(
            "failed to write to file: %s (%s)" % (file_out, e))

    if overwritten:
        print "done: minified file overwritten: %s" % file_out
    else:
        print "done: minified file created: %s" % file_out
