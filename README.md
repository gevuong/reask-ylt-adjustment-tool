# Environment Setup

This document outlines the steps taken to set up the development environment for the climateInsuranceBackend project. It includes setting up a Conda environment, configuring a Flask application, and ensuring all necessary dependencies are installed and properly configured.

1. Creating and Activating the Conda Environment
   A Conda environment was created to manage the dependencies of the project. The environment is defined by an environment.yml file located in the `deploy` directory.

- /climateInsuranceBackend
  - /demo-data
  - /output-data
  - /pylt
    - /**pycache**
    - /deploy
    - /utilities
  - /ylt-outputs
    - /demo

# Navigate to the project directory

```bash
cd path/to/climateInsuranceBackend
```

# Create the Conda environment

```bash
conda env create -f pylt/deploy/environment.yml
```

# Activate the environment

```bash
conda activate pylt
```

2. Verifying the Python Interpreter
   Ensured that the Python interpreter used was the one installed in the Conda environment.

Commands to Check Python Path:

```bash
which python
which python3
```

3. Installing Flask and Setting Up the API
   Flask was installed within the Conda environment to handle the backend API.

```bash
conda install flask
```

# Run the Api

```bash
python3 app.py
```

# Test for functionality

from a separate terminal call

```bash
curl -X POST http://127.0.0.1:5000/adjust
```
