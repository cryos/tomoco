import sys

import setuptools

# Use versioneer if available, otherwise just pass a dummy version.
try:
    import versioneer
    package_version = versioneer.get_version()
except ImportError:
    package_version = '0.1'


min_version = (3, 9)

if sys.version_info < min_version:
    error = """
Tomoco does not support Python {0}.{1}.
Python {2}.{3} and above is required.
""".format(*(sys.version_info[:2] + min_version))
    sys.exit(error)

with open('requirements.txt') as f:
    requirements = f.read().split()

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='tomoco',
    version=package_version,
    author='Marcus D. Hanwell',
    author_email='mhanwell@bnl.gov',
    description="Data acquisition and control GUI prototype.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="BSD (3-clause)",
    url="https://github.com/cryos/tomoco",
    packages=setuptools.find_packages(),
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        'console_scripts': [
            'tomoco = tomoco.app:run',
        ]
    },
)