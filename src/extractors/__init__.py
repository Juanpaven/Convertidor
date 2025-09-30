# -*- coding: utf-8 -*-
"""
Extractors package - Extractores especializados por sección
"""

from .base_extractor import BaseExtractor
from .info_basica import InformacionBasicaExtractor

__all__ = [
    'BaseExtractor',
    'InformacionBasicaExtractor'
]