import sys
import os

# Adiciona a pasta raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui import App
from data.db import *

init_db()
if __name__ == '__main__':
    app = App()
    app.mainloop()