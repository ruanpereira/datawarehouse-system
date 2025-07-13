import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from gui import App
from data.db import *


if __name__ == '__main__':
    app = App()
    app.mainloop()