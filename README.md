# Pilemma

This project is a concrete example of a decentralized autonomous protocol modeled (roughly) in an OpenAI gym environment. 


Requirments can be installed with 

```
pip install -r requirements.txt
```

You will most likely run into an error installing mpi4py

For my Centos7 systems I needed to do the following to install and link mpicc to mpi4py for installation:

```
yum install openmpi-devel
env MPICC=/usr/lib64/openmpi/bin/mpicc pip3.6 install --no-cache-dir mpi4py
```
