import random

from ..conf import NodeCategories


class DPaint_Random:
    """Random number generator"""
    NODE_NAME = "Random Number Generator"
    ICON = "🔃"
    CATEGORY = NodeCategories.UTILITY
    RETURN_TYPES = ("FLOAT","INT",)
    RETURN_NAMES = ("random_float","random_int")
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "min_value": ("FLOAT", {"default": 0.0}),
                "max_value": ("FLOAT", {"default": 1.0}),
                "distribution": (["uniform", "normal"],),
            }
        }

    def result(self, seed, min_value, max_value, distribution):
        r = random.Random(seed)
        def _rnd_values():
            v = r.random() * (max_value - min_value) + min_value
            return v, int(round(v))
        if distribution == "uniform":
            return _rnd_values()
        else:
            v = 0
            for i in range(5):
                v += _rnd_values()[0]
            v = v / 5
            return v, int(round(v))

