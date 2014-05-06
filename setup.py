from setuptools import setup, find_packages

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(
    name='htpwd',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    url='https://github.com/gcavalcante8808/htpwd',
    license='License :: OSI Approved :: Apache Software License',
    author='Gabriel Abdalla Cavalcante',
    author_email='gabriel.cavalcante88@gmail.com',
    description="""A web Interface for users change their own passwords on a
    htpasswd file.""",
)
