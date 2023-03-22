# Tomoco: experimental data acquisition GUI (Python, Qt)

Early stage experiment currently building out an approach to be used at the FXI
beamline at the National Synchrotron Light Source II (NSLS-II). It makes use of
the Ophyd project to abstract control of a sample stage, along with RE-0MQ to
submit plans to a locally running Bluesky Run Engine.

To install a development version create a virtual environment using your preferred tool and install this repository:
```
pip install -e .
```
from the root of the git repository this README file resides in. You can then run the main entry point using the convenience executable from your shell:
```
tomoco
```
