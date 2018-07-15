#! /usr/bin/env python

import unittest

from syntax_highlight import *

class TestSyntaxHighlight (unittest.TestCase):

  def test_html_py (self):
    html = '''
    <html>
    <body>
      <p>Some text</p>
      <pre>
        <code>
        import sys

        def something (foo):
          return foo

        sys.exit (1)
        </code>
      </pre>
      <p> some more text </p>
    </body>
    </html>
    '''

    s = SyntaxHighlight ()

    print ( s.do_filter_part ('', html, 'text/html', False) )

  def test_text_c (self):
    text = '''```
int main (int argc, char ** argv) {
  int a = 0;
  int b = 2;
  int c;

  c = a + b;
  return c;
}

```'''

    html = '''```<br>
int main (int argc, char ** argv) {<br>
&nbsp; int a = 0;<br>
&nbsp; int b = 2;<br>
&nbsp; int c;<br>
<br>
&nbsp; c = a + b;<br>
&nbsp; return c;<br>
}<br>
<br>
```<br>
<br>'''

    s = SyntaxHighlight ()

    print ( s.do_filter_part (text, html, 'text/plain', False) )

  def test_two_segments (self):

    text = '''```
<html>
  <head>
  </head>
</html>
```

```
import sys

def foo (bar):
  return bar + 1
```

'''


    html = '''```<br>
&lt;html&gt;<br>
&nbsp; &lt;head&gt;<br>
&nbsp; &lt;/head&gt;<br>
&lt;/html&gt;<br>
```<br>
<br>
```<br>
import sys<br>
<br>
def foo (bar):<br>
&nbsp; return bar + 1<br>
```<br>
<br>
<br>'''

    s = SyntaxHighlight ()

    print ( s.do_filter_part (text, html, 'text/plain', False) )

if __name__ == '__main__':
  unittest.main ()



