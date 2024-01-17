from setuptools import setup, find_packages

setup(
    name = "aiograf",
    version = '0.1.1',
    packages = find_packages(),
    install_requires = [
        "aiogram==2.25.1",
        "dill==0.3.7",
        "Pyrogram==2.0.106",
        "TgCrypto==1.2.5",
        "aiocryptopay==0.3.5",
    ],
)
