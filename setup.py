"""This is a setup.py script to install ShakeNBreak."""

import os
import warnings

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

path_to_file = os.path.dirname(os.path.abspath(__file__))


# See https://stackoverflow.com/questions/34193900/how-do-i-distribute-fonts-with-my-python-package
def _install_custom_font():
    """Install ShakeNBreak custom font."""
    print("Trying to install ShakeNBreak custom font...")
    # Try to install custom font
    try:
        try:
            import os
            import shutil

            import matplotlib as mpl
            import matplotlib.font_manager
        except Exception:
            print("Cannot import matplotlib!")

        # Find where matplotlib stores its True Type fonts
        mpl_data_dir = os.path.dirname(mpl.matplotlib_fname())
        mpl_fonts_dir = os.path.join(mpl_data_dir, "fonts", "ttf")

        # Copy the font file to matplotlib's True Type font directory
        fonts_dir = f"{path_to_file}/shakenbreak/"
        ttf_fonts = [file_name for file_name in os.listdir(fonts_dir) if ".ttf" in file_name]
        try:
            for font in ttf_fonts:  # must be in ttf format for matplotlib
                old_path = os.path.join(fonts_dir, font)
                new_path = os.path.join(mpl_fonts_dir, font)
                shutil.copyfile(old_path, new_path)
                print("Copying " + old_path + " -> " + new_path)
            if not ttf_fonts:
                print(f"No ttf fonts found in the {fonts_dir} directory.")
        except Exception:
            pass

        # Try to delete matplotlib's fontList cache
        mpl_cache_dir = mpl.get_cachedir()
        mpl_cache_dir_ls = os.listdir(mpl_cache_dir)
        for file_name in mpl_cache_dir_ls:
            if "fontlist" in file_name.lower():
                fontList_path = os.path.join(mpl_cache_dir, file_name)
                if os.path.exists(fontList_path):
                    os.remove(fontList_path)
                    print("Deleted the matplotlib fontList cache.")
        if not any("fontlist" in file_name.lower() for file_name in mpl_cache_dir_ls):
            print("Couldn't find matplotlib cache, so will continue.")

        # Add fonts
        for font in ttf_fonts:
            matplotlib.font_manager._load_fontmanager(try_read_cache=False)
            matplotlib.font_manager.fontManager.addfont(f"{fonts_dir}/{font}")
            print(f"Adding {font} font to matplotlib fonts.")

    except Exception:
        warnings.warn(
            "An issue occured while installing the custom font for ShakeNBreak. The widely available "
            "Helvetica font will be used instead."
        )


class PostInstallCommand(install):
    """Post-installation for installation mode.

    Subclass of the setup tools install class in order to run custom commands
    after installation. Note that this only works when using 'python setup.py install'
    but not 'pip install .' or 'pip install -e .'.
    """

    def run(self):
        """
        Performs the usual install process and then copies the True Type fonts
        that come with SnB into matplotlib's True Type font directory,
        and deletes the matplotlib fontList.cache.
        """
        # Perform the usual install process
        install.run(self)
        _install_custom_font()


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        """
        Performs the usual install process and then copies the True Type fonts
        that come with SnB into matplotlib's True Type font directory,
        and deletes the matplotlib fontList.cache.
        """
        develop.run(self)
        _install_custom_font()


class CustomEggInfoCommand(egg_info):
    """Post-installation."""

    def run(self):
        """
        Performs the usual install process and then copies the True Type fonts
        that come with SnB into matplotlib's True Type font directory,
        and deletes the matplotlib fontList.cache.
        """
        egg_info.run(self)
        _install_custom_font()


with open("README.md", encoding="utf-8") as file:
    long_description = file.read()


setup(
    name="shakenbreak",
    version="3.4.2",
    description="Package to generate and analyse distorted defect structures, in order to "
    "identify ground-state and metastable defect configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Irea Mosquera-Lois & Seán R. Kavanagh",
    author_email="i.mosquera-lois22@imperial.ac.uk, sean.kavanagh.19@ucl.ac.uk",
    maintainer="Irea Mosquera-Lois & Seán R. Kavanagh",
    maintainer_email="i.mosquera-lois22@imperial.ac.uk, sean.kavanagh.19@ucl.ac.uk",
    url="https://shakenbreak.readthedocs.io/en/latest/index.html",
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords="chemistry pymatgen dft defects structure-searching distortions symmetry-breaking",
    packages=find_packages(),
    python_requires=">=3.10",  # dictated by "pymatgen>=2025.5.2" requirement in doped
    install_requires=[
        "numpy",
        "pymatgen",  # requirement set by doped
        "pymatgen-analysis-defects",  # requirement set by doped
        "matplotlib>=3.6",
        "ase",
        "pandas>=1.1.0",
        "seaborn",
        "hiphive>=1.0",  # nbr_cutoff not defined in previous versions of mc_rattle
        "monty",
        "click>8.0",
        "importlib_metadata",
        "doped>=3.1",  # for StructureMatcher_scan_stol, for super-fast structure matching
    ],
    extras_require={
        "tests": [
            "pytest>=7.1.3",
            "pytest-mpl==0.17.0",
        ],
        "docs": [
            "sphinx",
            "sphinx-book-theme",
            "sphinx_click",
            "sphinx_design",
        ],
        "pdf": [
            "pycairo",
        ],
    },
    # Specify any non-python files to be distributed with the package
    package_data={
        "shakenbreak": ["shakenbreak/*"],
    },
    include_package_data=True,
    # Specify the custom installation class
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "snb = shakenbreak.cli:snb",
            "snb-generate = shakenbreak.cli:generate",
            "snb-generate_all = shakenbreak.cli:generate_all",
            "snb-run = shakenbreak.cli:run",
            "snb-parse = shakenbreak.cli:parse",
            "snb-analyse = shakenbreak.cli:analyse",
            "snb-plot = shakenbreak.cli:plot",
            "snb-regenerate = shakenbreak.cli:regenerate",
            "snb-groundstate = shakenbreak.cli:groundstate",
            "snb-mag = shakenbreak.cli:mag",
            "shakenbreak = shakenbreak.cli:snb",
            "shakenbreak-generate = shakenbreak.cli:generate",
            "shakenbreak-generate_all = shakenbreak.cli:generate_all",
            "shakenbreak-run = shakenbreak.cli:run",
            "shakenbreak-parse = shakenbreak.cli:parse",
            "shakenbreak-analyse = shakenbreak.cli:analyse",
            "shakenbreak-plot = shakenbreak.cli:plot",
            "shakenbreak-regenerate = shakenbreak.cli:regenerate",
            "shakenbreak-groundstate = shakenbreak.cli:groundstate",
            "shakenbreak-mag = shakenbreak.cli:mag",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
        "egg_info": CustomEggInfoCommand,
    },
    project_urls={
        "Homepage": "https://shakenbreak.readthedocs.io/en/latest/index.html",
        "Documentation": "https://shakenbreak.readthedocs.io/en/latest/index.html",
        "Package": "https://pypi.org/project/shakenbreak/",
        "Repository": "https://github.com/SMTG-Bham/shakenbreak",
    },
)


_install_custom_font()
