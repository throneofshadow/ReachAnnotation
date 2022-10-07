from setuptools import setup

with open("Readme.md", 'r') as f:
    long_description = f.read()


setup(
    name='ReachAnnotation',
    version='0.1.0',
    description=
    'A library intended to generate a GUI to annotate / label video files for the ReachMaster experimental'
    ' paradigm.Install on python using pip install ReachAnnotate -- Current published version is 0.1.0',
    url='https://github.com/throneofshadow/ReachAnnotation',
    author='Brett Nelson, Nicholas Chin',
    author_email='bnelson@lbl.gov',
    license='BSD-3-Clause-LBNL',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['tkinter', 'video', 'player', 'video player', 'tkvideoplayer', 'play video in tkinter', 'custom annotation'],
    packages=['ReachAnnotation'],
    install_requires=['pandas', 'tkinter', 'unittest', 'os', 'av', 'pillow'],
    include_package_data=True,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.6',
    ],
)
