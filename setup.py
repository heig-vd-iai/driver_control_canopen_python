from setuptools import setup, find_packages

setup(
    name="driver_control_canopen",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "canopen==2.3.0",
        "PyYAML==6.0.1",
        "voluptuous==0.14.2"
    ],
    author="Adrien Cardinale",
    author_email="adrien.cardinale@heig-vd.ch",
    description="Small library for control motor driver in CANopen with python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/heig-vd-iai/driver_control_canopen_python",  # Remplacez par l'URL de votre repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)