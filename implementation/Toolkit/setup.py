from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="care_sm_toolkit",
    version="1.3",
    packages=find_packages(exclude=["toolkit.API", "toolkit.API.*"]),
    author="Pablo Alarcón Moreno",
    author_email="pabloalarconmoreno@gmail.com",
    url="https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2",
    description="A toolkit for CARE-SM data transformation.",
    long_description="See README.md",
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["FAIR-in-a-box", "Fiab", "CARE-SM", "Toolkit"],
    project_urls={
        "Source": "https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/tree/main/implementation/Toolkit",
        "Bug Tracker": "https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/issues",
    },
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest",
            "pytest-mock",
        ],
    },
    include_package_data=True,

)