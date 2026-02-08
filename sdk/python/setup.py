from setuptools import setup, find_packages

setup(
    name="empathy-sdk",
    version="0.1.0",
    description="Client SDK for Empathy API - Human-friendly error messages",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
