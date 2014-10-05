__author__ = 'dzlab'

from unittest import TestCase
from core.inout.writer import BufferedWriter, Formatter
from nose.tools import *


class WriterTest(TestCase):

    class FakeOutput:

        def __init__(self):
            self.buffer = ''

        def write(self, line):
            self.buffer += line

    @staticmethod
    def create_buffered_writer_with_block(block=1):
        return BufferedWriter(output=WriterTest.FakeOutput(), block=block)

    def it_should_writer_to_output_test(self):
        writer = WriterTest.create_buffered_writer_with_block()
        writer.append("")
        eq_(writer.buffer, "", "The buffer should be empty as we appended an empty string")
        writer.append("hello world")
        eq_(writer.buffer, "", "The buffer should be empty as the text was writing to output")
        writer.append("lorem ipsum dolor sit amet")
        eq_(writer.buffer, "", "The buffer should be empty as the text was writing to output again")

    def it_should_writer_to_internal_buffer_test(self):
        writer = WriterTest.create_buffered_writer_with_block(1000)
        writer.append("")
        eq_(writer.buffer, "", "The buffer should be empty as we appended an empty string")
        writer.append("hello world")
        eq_(writer.buffer, "hello world\n", "The buffer should not be empty as the text was added")
        writer.append("lorem ipsum dolor sit amet")
        eq_(writer.buffer, "hello world\nlorem ipsum dolor sit amet\n", "The buffer should contain old text and the newly added")


class FormatterTest(TestCase):

    def test_csv_formatted_output(self):
        formatter = Formatter()
        data = ""
        eq_(formatter.format(data), data, "The formatter should do nothing to empty data")
        data = "a, b, c"
        eq_(formatter.format(data), data + '\n', "The formatter should end the line for the next entry")

    def test_json_formatted_output(self):
        formatter = Formatter('json')
        data = ""
        eq_(formatter.format(data), data, "The formatter should do nothing to empty data")
        data = "{'key': 'a', 'value': 2}"
        eq_(formatter.format(data), data, "The formatter should add nothing as this is a first entry")
        data = "{'key': 'b', 'value': 56}"
        eq_(formatter.format(data), "," + data, "The formatter should add ',' to separate this entry from previous one")