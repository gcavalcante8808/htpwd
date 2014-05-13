from setuptools import setup, find_packages

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(
    name='htpwd',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    url='https://github.com/gcavalcante8808/htpwd',
    license='License :: OSI Approved :: Apache Software License',
    author='Gabriel Abdalla Cavalcante',
    author_email='gabriel.cavalcante88@gmail.com',
    description="""A web Interface for users change their own passwords on a
    htpasswd file.""",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
    ],
)
