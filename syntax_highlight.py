#! /usr/bin/env python
import gi
try:
  gi.require_version ('GMime', '3.0')
except ValueError:
  gi.require_version ('GMime', '2.6')

from gi.repository import GMime

from pygments               import highlight
from pygments.lexers        import guess_lexer
from pygments.formatters    import HtmlFormatter

class SyntaxHighlight:

  def high (self, segment):
    lexer = guess_lexer (segment)

    print ("filtering: guessed language:", str(lexer))

    return highlight (segment, lexer, HtmlFormatter (noclasses = True))

  def do_filter_part (self, text, html, mime_type, is_patch):
    """
    Filter the part and output safe HTML.

    Search for code tags (``` or <code>), or determine if part is a patch.
    Syntax highlight the relevant parts and use the html part for the rest.
    """

    ## Try to figure out if part is a patch
    if is_patch:
      from pygments.lexers.diff import DiffLexer
      return highlight (text, DiffLexer (), HtmlFormatter (noclasses = True))

    ## Look for code segments between code-tags
    starttags = [ '```', '<code>'  ]
    endtags   = [ '```', '</code>' ]

    if mime_type == 'text/html':
      for tag, antitag in zip(starttags, endtags):
        i = 0

        def tags ():
          nonlocal i
          i = html.find (tag, i)
          if i != -1:
            i += len (tag)
            yield i

        for j in tags ():
          e = html.find (antitag, i)

          if e != -1:
            segment = self.high (html[i:e])
            html    = html[:i-len(tag)] + segment + html[e + len(antitag):]

            i += len(segment) - len(tag)

          else:
            break

      return html

    elif mime_type == 'text/plain':
      # The GMime filter has created the HTML line-for-line. So if we find the
      # code tag on a line, it matches the same line in the HTML part.

      text_lines = text.split ('\n')
      html_lines = html.split ('\n')

      no     = 0
      offset = 0 # offset between HTML and TEXT part after syntax highlighting a segment
      while no < len(text_lines):
        l = text_lines[no]
        for tag, antitag in zip (starttags, endtags):
          it = l.find (tag)
          if it > -1:
            ih = html_lines[no + offset].find (tag)

            # find end
            for eno,el in enumerate (text_lines[no:]):
              iet = el.find (antitag)
              ieh = html_lines[no + eno + offset].find (antitag)

              if (eno > 0 and iet > -1) or (eno == 0 and iet > it):
                # found end tag
                segment     = text_lines[no:no + eno+1]
                segment[0]  = segment[0][it + len(tag):]
                segment[-1] = segment[-1][:iet]

                html_segment = self.high ('\n'.join (segment)).split ('\n')

                html_segment[0]  = html_lines[no + offset][ih + len(tag):] + html_segment[0]
                html_segment[-1] = html_segment[-1] + html_lines[no + eno + offset][ieh + len(antitag):]

                html_lines = html_lines[:no + offset] + html_segment + html_lines[no + eno + offset +1:]

                offset += len(html_segment) - len(segment)
                no     += eno
                break
            break
        no += 1

      return '\n'.join(html_lines)

    else:
      return html


