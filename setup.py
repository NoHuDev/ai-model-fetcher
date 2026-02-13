from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='ai-model-fetcher',
    version='0.1.0-beta',
    description='A Python GUI application for downloading AI model metadata and sample images',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='NoHuman',
    url='https://github.com/nohumangaming/ai-model-fetcher',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'requests==2.31.0',
        'Pillow==10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ai-model-fetcher=ui:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Internet',
    ],
    keywords='ai models download metadata documentation',
    project_urls={
        'Bug Reports': 'https://github.com/nohumangaming/ai-model-fetcher/issues',
        'Source': 'https://github.com/nohumangaming/ai-model-fetcher',
    },
)
