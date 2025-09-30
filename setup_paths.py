# -*- coding: utf-8 -*-
"""
Configuración de paths para importaciones - Wrapper para scripts/setup_paths.py
"""
import sys
import os
from pathlib import Path

def setup_paths():
    """Configura los paths necesarios para las importaciones"""
    # Obtener directorio base del proyecto
    base_dir = Path(__file__).parent
    src_dir = base_dir / 'src'
    scripts_dir = base_dir / 'scripts'
    
    # Agregar directorios al path si no están ya
    paths_to_add = [str(base_dir), str(src_dir), str(scripts_dir)]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    return base_dir, src_dir

# Configurar paths automáticamente al importar este módulo
BASE_DIR, SRC_DIR = setup_paths()