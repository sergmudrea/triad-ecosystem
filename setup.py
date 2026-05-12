#!/usr/bin/env python3
# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="triad-ecosystem",
    version="2.0.0",
    author="Z3R0",
    author_email="z3r0@triad.ecosystem",
    description="Self-evolving autonomous cyber ecosystem with Black-Red-Blue agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/z3r0/triad-ecosystem",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.12.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
        "dashboard": ["plotly>=5.18.0", "aiohttp>=3.9.3", "websockets>=12.0"],
    },
    entry_points={
        "console_scripts": [
            "triad=orchestrator:main",
            "triad-dashboard=visualization.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
