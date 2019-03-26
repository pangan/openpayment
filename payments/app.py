# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import sys
import logging

from flask import Flask

from payments.endpoints import open_payments, download


_LOG = logging.getLogger()

LOG_FORMATTER = logging.Formatter(
            '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S +0000')




class App(object):  # pragma: no cover

    api = None
    declarative_base = None
    session_object = None


    @classmethod
    def init_flask(cls, root_path=None):

        if root_path:
            cls.api = Flask(__name__, root_path=root_path)
        else:
            cls.api = Flask(__name__)

        cls.init_logger()


    @classmethod
    def init_logger(cls):

        log_level = logging.DEBUG

        root = logging.getLogger()
        root.setLevel(log_level)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(log_level)
        ch.setFormatter(LOG_FORMATTER)
        root.addHandler(ch)


App.init_flask()
api = App.api
api.logger_name = "flask.app"


api.register_blueprint(open_payments.bp)
api.register_blueprint(download.bp)

download.output_excel.init_excel(api)
