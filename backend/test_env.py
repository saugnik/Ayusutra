try:
    import aiofiles
    print("aiofiles is installed!")
except ImportError:
    print("aiofiles is NOT installed.")

import os
print("CWD:", os.getcwd())
