# -*- coding: utf-8 -*-

from .conf import DPaint_Config


def setup_default_config():
    DPaint_Config()
    pass

def run_install():
    setup_default_config()


if __name__ == "__main__":
    run_install()
