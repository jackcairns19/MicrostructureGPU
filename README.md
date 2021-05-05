# MicrostructureGPU

**SETUP:**

  In order to run the code locally, first you will need to clone this repository to your local machine. From there
  you will need to download the latest version of Python. You will also need to  download and install Nvidia's Cuda
  compiler driver. BOTH Python and NVCC need to be added to the path variable of your machine.
  
  The Python installers for Windows include pip. You should be able to access pip using:

    py -m pip --version

  Verify that pip is up-to-date by running:

    py -m pip install --upgrade pip
    
  From here, you need to create a Python virtual environment in the same directory in which the project has been cloned to.
  
    py -m pip install --user virtualenv
    py -m venv env
    
  Activate the environment from the same directory:
  
    .\env\Scripts\activate
    
  The following packages need to be installed via pip:
  
    pip install tk
    pip install Pillow
    pip install cupy-cuda112
    pip install numpy
    pip install scipy
    pip install threadpoolctl
    
    
**RUNNING THE CODE**

Activate the environment:

    .\env\Scripts\activate
    
Run NumPy implementation:

    python ./BinaryMicrostructureGUI.py
    
Run CuPy Implementation:

    python ./BinaryMicrostructureGUI_CuPy.py

