from setuptools import setup

setup(name='pieorg',
      version='1.0.0',
      description='A Python CLI app to organise every story you read on the internet.',
      author='Yash Prakash',
      author_email="yashprakash13@gmail.com",
      py_modules=['app'],
      license="MIT",
      packages=["pieorg"],
      install_requires=['click', 'art'],
      entry_points='''
        [console_scripts]
        pieorg=pieorg.app:begin
    ''')
