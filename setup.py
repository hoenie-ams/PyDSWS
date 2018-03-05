from distutils.core import setup

setup(
    name='PyDSWS',
    version='0.07',
    packages=['PyDSWS'],
    url='https://github.com/hoenie-ams/PyDSWS',
    license='MIT',
    author='Joris Hoendervangers',
    author_email='j.h.hoendervangers@gmail.com',
    description='Python package for Thomson Reuters Datastream Webservices (DSWS)',
    long_description='Python package for Thomson Reuters Datastream Webservices (DSWS)',
    install_requires=[
        'pandas',
        'requests',
      ],
    python_requires='>=3'

)
