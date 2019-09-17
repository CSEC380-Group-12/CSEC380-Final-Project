#! /usr/bin/python

"""
test_hello_world.py: test the content/body of an HTML page
Author: Bad3r
"""

from lxml import html


def test_hello_world():
    body = html.parse('http://localhost').xpath('//body')[0].text_content()
    assert 'Hello World!' == body


if __name__ == '__main__':
    test_hello_world()
