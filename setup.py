from distutils.core import setup

setup(
    name='PyDSWS',
    version='0.03',
    packages=['PyDSWS'],
    url='https://github.com/hoenie-ams/PyDSWS',
    license='MIT',
    author='Joris Hoendervangers',
    author_email='j.h.hoendervangers@gmail.com',
    description='Python package for Datastream Webservices',
    long_description='Python package for Datastream Webservices',
    install_requires=[
        'pandas',
        'requests',
        'urllib',
        'datetime',
        'json'
      ],
    python_requires='>=3'

)
