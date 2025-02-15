# -*- coding: utf-8 -*-
import sys, os

#sys.path.append(str(os.path.dirname(os.path.abspath(__file__))))

from .conf import DPaint_Config


def setup_default_config():
    DPaint_Config()
    pass

def run_install():
    setup_default_config()


if __name__ == "__main__":
    run_install()
