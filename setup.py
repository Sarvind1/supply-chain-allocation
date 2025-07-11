"""Setup configuration for supply chain allocation engine."""

from setuptools import setup, find_packages

setup(
    name="supply-chain-allocation",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.5.0",
        "networkx>=3.2.1",
        "pandas>=2.1.3",
        "numpy>=1.24.3",
        "click>=8.1.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.7.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "allocate=src.main:main",
        ],
    },
)