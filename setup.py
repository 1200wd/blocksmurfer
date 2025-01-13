# -*- coding: utf-8 -*-
#
#    Blocksmurfer
#    PyPi Setup Tool
#    © 2020 May - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
version = '1.2'

# Get the long description from the relevant file
readmetxt = ''
try:
      with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
          readmetxt = f.read()
except:
      pass

kwargs = {}

install_requires = [
    'bitcoinlib>=0.6.10',
    'Flask==2.3.2',
    'flask_babel==3.1.0',
    'flask_qrcode==3.1.0',
    'flask_restful==0.3.10',
    'flask_wtf==1.1.0',
    'Werkzeug==2.3.6',
    'WTForms==3.0.1',
    'gunicorn==20.1.0',
]


kwargs['install_requires'] = install_requires

setup(
      name='blocksmurfer',
      version=version,
      description='Bitcoin blockchain explorer',
      long_description=readmetxt,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry',
            'Intended Audience :: Information Technology',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Security :: Cryptography',
            'Topic :: Office/Business :: Financial :: Accounting',
      ],
      url='http://github.com/1200wd/blocksmurfer',
      author='1200wd',
      author_email='info@1200wd.com',
      license='GNU3',
      packages=['blocksmurfer'],
      test_suite='tests',
      include_package_data=True,
      keywords='bitcoin blockchain explorer transactions keys blocks utxos inputs outputs scripts',
      zip_safe=False,
      **kwargs
)
