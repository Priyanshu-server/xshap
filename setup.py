from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='xshap',         
    version='0.1.1',              
    packages=find_packages(),
    install_requires=required_packages, 
    author='xDoramming',
    author_email='priyanshuserver55@gmail.com',
    description='Package created as a wrapper for the original Shap package to simplify the learning process',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Priyanshu-server/xshap',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)