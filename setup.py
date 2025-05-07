from setuptools import setup, find_packages

setup(
    name="Wind",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "wind.data": ["config.json"],
    },
    install_requires=["rich"],
    entry_points={
        "console_scripts": [
            "wind=wind.cli:main",
        ],
    },
    description="Pattern-based password wordlist generator",
    author="0xf0xy",
    license="MIT",
)
