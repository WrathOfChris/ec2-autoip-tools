import os
import re
from ec2_autoip_tools import __version__
from setuptools import setup, find_packages

setup(
    name='ec2-autoip-tools',
    version=__version__,
    author="Chris Maxwell",
    author_email="chris@wrathofchris.com",
    description="Tools for auto-assigning IP addresses within EC2",
    url = "https://github.com/WrathOfChris/ec2-autoip-tools",
    download_url = 'https://github.com/WrathOfChris/ec2-autoip-tools/tarball/%s' % __version__,
    license="Apache",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'boto',
        'PyYAML'
    ],
    entry_points={
        "console_scripts": [
            "ec2-autoip-atboot = ec2_autoip_tools.cli:ec2_autoip_atboot"
        ]
    }
)
