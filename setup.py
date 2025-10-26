from setuptools import setup, find_packages
from pathlib import Path
import re

# Function to read version from qpac/__init__.py
def read_version():
    init_file = Path(__file__).parent / "qpac" / "__init__.py"
    content = init_file.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string in __init__.py")

setup(
    name="qpac",
    version=read_version(),  # Automatically read version from __init__.py
    packages=find_packages(),  # Automatically include qpac/
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24"
    ],
    url="https://github.com/soumyapriyagoswami/qpac.git",  # Replace with your repo
    author="Soumyapriya Goswami",
    author_email="soumyapriya.goswami.it2023@kgec.ac.in",
    description="Quantum-Inspired Pattern-Aware Compression (QPAC) Python Library",
    long_description=(Path(__file__).parent / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
