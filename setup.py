import subprocess

from setuptools import setup

try:
    # Get the version of GDAL using gdal-config
    gdal_version = subprocess.check_output(
        ["gdal-config", "--version"], text=True
    ).strip()
except FileNotFoundError as e:
    raise Exception("Can't find gdal-config. Is GDAL installed?") from e


setup(
    name="vectors2vrt",
    version="0.3",
    description="Generate a VRT file from GIS vector sources",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/fgregg/vectors2vrt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
    packages=["vectors2vrt"],
    entry_points={
        "console_scripts": [
            "vectors2vrt = vectors2vrt:main",  # Entry point for the script
        ],
    },
    install_requires=[f"gdal=={gdal_version}", "click"],
    extras_require={
        "dev": [
            "black",
            "isort",
        ],
    },
    # Include wheel, setuptools as requirements for the build
    setup_requires=["setuptools>=42", "wheel"],
)
