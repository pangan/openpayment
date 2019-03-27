# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from payments.app import api


if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    make_server('127.0.0.1', 5000, api).serve_forever()
