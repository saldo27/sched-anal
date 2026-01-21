"""
Setup configuration for Shift Schedule Analyzer
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sched-analyzer",
    version="1.0.0",
    author="Luis Herrera Para",
    description="Herramienta para análisis de guardias desde calendarios PDF y Excel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saldo27/sched-anal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask==3.1.2",
        "flask-cors==4.0.0",
        "werkzeug==2.3.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "pdfplumber>=0.10.0",
        "python-dateutil>=2.8.0",
        "ReportLab>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sched-analyzer=app:app.run",
        ],
    },
)
