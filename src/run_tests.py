"""Script auxiliar para executar testes."""
import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao PYTHONPATH
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Executa pytest
if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "tests/"])

