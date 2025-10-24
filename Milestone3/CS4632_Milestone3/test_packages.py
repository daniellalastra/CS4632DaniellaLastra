try:
    import pandas as pd
    import simpy
    import matplotlib
    import numpy as np
    print("✅ All packages installed successfully!")
    print(f"Pandas version: {pd.__version__}")
except ImportError as e:
    print(f"❌ Error: {e}")