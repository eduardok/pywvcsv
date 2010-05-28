from distutils.core import setup, Extension
from subprocess import Popen, PIPE

WVBUILD='../wvbuild'
WVSTREAMS="%s/wvstreams/include" % WVBUILD
WVSTREAMSLIB="%s/%s-linux" % (WVBUILD,
    Popen(['uname', '-m'], stdout=PIPE).communicate()[0].rstrip())
includes = [WVSTREAMS, "%s/include" % WVSTREAMSLIB]

pywvcsv_mod = Extension('pywvcsv',
                        sources=['pywvcsvmodule.cc',
                                 '../cli/wvcsv.cc'],
                        include_dirs=includes + ['../cli'],
                        library_dirs=[WVSTREAMSLIB],
                        libraries=['wvbase', 'wvutils', 'wvstreams'])

setup(name='Python_WvCsv',
      version='0.1',
      description='WvCsv bindings for Python',
      ext_modules=[pywvcsv_mod])
