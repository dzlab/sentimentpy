__author__ = 'dzlab'

from unittest import TestCase
from core.inout.writer import BufferedWriter
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