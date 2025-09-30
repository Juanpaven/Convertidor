# -*- coding: utf-8 -*-
"""
Configuración de paths para importaciones
"""
import sys
import os
from pathlib import Path

def setup_paths():
    """Configura los paths necesarios para las importaciones"""
    # Obtener directorio base del proyecto (ir un nivel arriba desde scripts)
    base_dir = Path(__file__).parent.parent
    src_dir = base_dir / 'src'
    
    # Agregar directorios al path si no están ya
    paths_to_add = [str(base_dir), str(src_dir)]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    return base_dir, src_dir

# Configurar paths automáticamente al importar este módulo
BASE_DIR, SRC_DIR = setup_paths()