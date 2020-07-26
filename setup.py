from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='sample',
    version='0.0.1',
    description='transfer and manage music library.',
    long_description=readme,
    author='Abhijeet Mishra',
    author_email='dsisavi@gmail.com',
    url='https://github.com/disisavi/transferLib',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
