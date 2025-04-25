from setuptools import setup, find_packages

setup(
    name="taubert",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyserial>=3.5",
        "RPi.GPIO>=0.7.0",
    ],
    entry_points={
        "console_scripts": [
            "taubert=taubert.main:main",
        ],
    },
    python_requires=">=3.7",
    author="Naohiro IIDA",
    author_email="nao@nekotorobot.com",
    description="Python control software for Taubert omnidirectional robot",
    keywords="robot, raspberry pi, servo, omnidirectional",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
