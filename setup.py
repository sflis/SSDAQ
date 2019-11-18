from setuptools import setup, find_packages
import os
import sys
from shutil import copyfile, rmtree

install_requires = [
    "zmq",
    "numpy",
    "tables",
    "pyparsing",
    "matplotlib",
    "pyyaml",
    "click",
    "bitarray",
    "protobuf",
    "blessed",
    "pyqtgraph",
    "mysqlclient",
    "pyarrow"
]

#


if not os.path.exists("tmps"):
    os.makedirs("tmps")
copyfile("ssdaq/version.py", "tmps/version.py")
__import__("tmps.version")
package = sys.modules["tmps"]
package.version.update_release_version("ssdaq")

setup(
    name="SSDAQ",
    version=package.version.get_version(pep440=True),
    description="A framework to handle slow signal data from the CHEC-S camera",
    author="Samuel Flis",
    author_email="samuel.flis@desy.de",
    url="https://github.com/sflis/SSDAQ",
    packages=find_packages(),
    provides=["ssdaq"],
    license="GNU Lesser General Public License v3 or later",
    install_requires=install_requires,
    extras_requires={
        #'encryption': ['cryptography']
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "control-ssdaq=ssdaq.bin.ssdaq_control:main",
            "chec-slowsig-dumper=ssdaq.bin.terminaldumpers:slowsignaldump",
            "chec-mon-dumper=ssdaq.bin.terminaldumpers:mondumper",
            "chec-trigger-dumper=ssdaq.bin.terminaldumpers:triggerdump",
            "chec-timestamp-dumper=ssdaq.bin.terminaldumpers:timestampdump",
            "chec-log-dumper=ssdaq.bin.terminaldumpers:logdump",
            "chec-timestamp-writer=ssdaq.bin.writers:timestampwriter",
            "chec-trigger-writer=ssdaq.bin.writers:triggerwriter",
            "chec-atrigger-writer=ssdaq.bin.writers:atriggerwriter",
            "chec-log-writer=ssdaq.bin.writers:logwriter",
            "chec-slowsig-writer=ssdaq.bin.writers:slowsignal",
            "chec-aslowsig-writer=ssdaq.bin.writers:aslowsignal",
            "chec-slowsig-viewer=ssdaq.bin.slowsignalviewer:slowsignalviewer",
            "chec-timestamp-viewer=ssdaq.bin.slowsignalviewer:timestampviewer",
            "chec-triggerpattern-viewer=ssdaq.bin.slowsignalviewer:triggerpatternviewer",
            "chec-daq-dash=ssdaq.bin.dash:mondumper",
        ]
    },
)


rmtree("tmps")
