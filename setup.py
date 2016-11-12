import setuptools

setuptools.setup(
    name='muhblog',
    version='0.1',
    license='MIT',
    author='elcr',
    author_email='elcr@outlook.com',
    url='https://bitbucket.org/elcr/muhblog',
    packages=['muhblog'],
    include_package_data=True,
    entry_points={'console_scripts': ['muhblog=muhblog:main']},
    platforms='any',
    install_requires=['click', 'Flask', 'python-slugify',
                      'mistune', 'Frozen-Flask', 'pyScss'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Framework :: Flask',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6'],
    zip_safe=False
)
