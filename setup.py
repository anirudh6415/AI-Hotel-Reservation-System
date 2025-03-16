from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name ="Hotel-reservations-system",
    version="0.1",
    author="Anirudh",
    packages= find_packages(),
    install_requires = requirements,
)

### 
### To RUN this File pip install -e .