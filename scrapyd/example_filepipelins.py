#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join

class PyFilePipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)), basename(path))