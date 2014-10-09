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
        eq_(writer.buffer, "hello world\n")
        writer.append("lorem ipsum dolor sit amet")
        eq_(writer.buffer, "hello world\nlorem ipsum dolor sit amet\n", "The buffer should contain old text and the newly added")


class FormatterTest(TestCase):

    def test_tsv_formatted_output(self):
        formatter = Formatter(file_format='tsv')
        FormatterTest.check_sv_formatted_output(formatter)

    def test_csv_formatted_output(self):
        formatter = Formatter(file_format='csv')
        FormatterTest.check_sv_formatted_output(formatter)

    @staticmethod
    def check_sv_formatted_output(formatter):
        separator = formatter.separator
        data = ""
        eq_(formatter.format_content(data), data, "The formatter should do nothing to empty data")
        formatted_header = formatter.format_header(['a', 'b', 'c'])
        eq_("a"+separator+"b"+separator+"c\n", formatted_header)
        data = {'b': 1, 'c': 55, 'a': 'ok'}
        formatted_content = formatter.format_content(data)
        eq_("ok"+separator+"1"+separator+"55\n", formatted_content, "The formatter should end the line for the next entry")

    def test_json_formatted_output(self):
        formatter = Formatter('json')
        data = ""
        formatted_content = formatter.format_content(data)
        eq_(formatted_content, data, "The formatter should do nothing to empty data")
        data = "{'key': 'a', 'value': 2}"
        formatted_content = formatter.format_content(data)
        eq_(formatted_content, data, "The formatter should add nothing as this is a first entry")
        data = "{'key': 'b', 'value': 56}"
        formatted_content = formatter.format_content(data)
        eq_(formatted_content, "," + data, "The formatter should add ',' to separate this entry from previous one")

    def test_csv_formatted_file(self):
        formatter = Formatter('csv')
        keys = ['k1', 'k2', 'k3']
        formatted_header = formatter.format_header(keys)
        eq_(formatted_header, 'k1,k2,k3\n', "The formatted header should concatenate keys")
        data = {'k1': 1, 'k2': '2', 'k3': 3.0}
        formatted_content = formatter.format_content(data)
        eq_(formatted_content, '1,2,3.0\n', "The formatter should concatenate values")
        data = {'k1': 1, 'k3': 3.0}
        formatted_content = formatter.format_content(data)
        eq_(formatted_content, '1,NA,3.0\n', "Missing values should be replaced by 'NA'")

