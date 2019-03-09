from setuptools import setup, find_packages

setup(
        name='agile-scraper',
        packages=find_packages(),
        version='0.1',
        description='PyScraper on Agile Submissions.',
        author='Justin Beall',
        author_email='jus.beall@gmail.com',
        url='https://github.com/DEV3L/agile-scraper',
        keywords=['beautifulsoup', 'python'],
        install_requires=[
            'beautifulsoup4==4.6.3',
            'requests==2.20.0',
            'selenium==3.141.0'
        ],
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3'
        ]
)
