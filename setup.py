from setuptools import setup, find_packages

setup(
    name="Labra",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "pytest",
        "allure-pytest",
        "pytest-playwright"
    ],
    python_requires=">=3.10",
    author="Aven Stewart",
    author_email="avenstewart@gmail.com",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avenstewart/Labra",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
