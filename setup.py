from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pydci',
      version='0.0.3',
      description='PyDCI - Data Context Interaction framework for Python',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: MIT',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='dci, data, context, interaction, role, roles',
      url='https://github.com/lygav/pydci',
      author='Vladimir (Vladi) Lyga',
      author_email='lyvladi@gmail.com',
      license='proprietary',
      packages=['pydci', 'pydci.src'],
      install_requires=[],
      test_suite='',
      tests_require=[],
      entry_points={},
      include_package_data=True,
      zip_safe=False)