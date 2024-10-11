from setuptools import setup, find_packages

setup(
    name="UART",
    version="1.0.0",
    author="IVEN-CN",
    author_email="hyf_iven@outlook.com",
    description="重写并且继承了pyserial库的串口类，封装了一些常用的串口操作",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",      # 
    url="https://github.com/Blue-Net-Team/UART.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyserial",
    ],
)