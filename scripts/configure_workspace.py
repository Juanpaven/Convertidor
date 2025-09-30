# -*- coding: utf-8 -*-
"""
Configuración del entorno Python para el workspace
"""
import sys
import os
from pathlib import Path

def configure_workspace():
    """Configura el workspace para VS Code"""
    workspace_path = Path(__file__).parent
    
    # Verificar que el intérprete de Python está configurado correctamente
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Workspace path: {workspace_path}")
    
    # Verificar que las funciones built-in están disponibles
    builtins_test = {
        'print': print,
        'len': len,
        'range': range,
        'enumerate': enumerate,
        'min': min,
        'max': max,
        'int': int,
        'any': any,
        'Exception': Exception,
        'ImportError': ImportError
    }
    
    print("\nFunciones built-in disponibles:")
    for name, func in builtins_test.items():
        print(f"  ✓ {name}: {type(func)}")
    
    # Verificar módulos estándar
    try:
        import gc
        import time
        print(f"\nMódulos estándar:")
        print(f"  ✓ gc: {gc}")
        print(f"  ✓ time: {time}")
    except ImportError as e:
        print(f"  ❌ Error importando módulos: {e}")
    
    return True

if __name__ == "__main__":
    configure_workspace()