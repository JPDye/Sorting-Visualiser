from setuptools import setup, find_packages

setup(
        name="viz",
        version="0.1",
        packages=find_packages(),
        install_requires=["numpy", "Pillow",  "imagio"],

        author="Joseph Dye",
        author_email="jpzh.dye@gmail.com",
        url="https://github.com/JPDye",

        description="Randomises input images and then sorts them in order to visualise different sorting algorithms.",

        license="MIT",
        )
