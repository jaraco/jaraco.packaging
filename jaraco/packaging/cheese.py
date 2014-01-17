"""
A script for uploading already packaged sdists and eggs to a cheeseshop
"""

import os
import argparse
import collections
import re
import zipfile
import tarfile
import io
import itertools
import distutils.command.upload
import distutils.dist

import six
from six.moves import urllib

DistFile = collections.namedtuple('DistFile', 'command pyversion filename')

class TarGZAdapter(object):
    """
    Wrap a TarFile object to emulate a ZipFile object
    """
    def __init__(self, archive):
        self.archive = archive

    def open(self, filename):
        return self.archive.extractfile(filename)

    def namelist(self):
        return self.archive.getnames()

def looks_like_zip(stream):
    """
    Peek into the stream and tell me if it looks like a zip file
    """
    first_two_bytes = stream.read(2)
    stream.seek(0)
    return first_two_bytes == 'PK'

def is_targz(filename):
    return filename.endswith('.tar.gz') or filename.endswith('.tgz')

def force_zip_extension(filename):
    """
    If the file is named .tar.gz or .tgz, give it a zip extension
    """
    filename, ext = os.path.splitext(filename)
    if filename.endswith('.tar'):
        filename, ext = os.path.splitext(filename)
    return filename + '.zip'

def open_archive(stream, filename):
    """
    Open an archive (tarball or zip) and return the object.
    """
    name, ext = os.path.splitext(os.path.basename(filename))
    def targz_handler(stream):
        return TarGZAdapter(tarfile.open(fileobj=stream, mode='r:gz'))
    cls = [zipfile.ZipFile, targz_handler]['gz' in ext]
    archive = cls(stream)
    return archive

def get_prefix_dir(archive):
    """
    Often, all files are in a single directory. If so, they'll all have
    the same prefix. Determine any such prefix.
    archive is a ZipFile
    """
    names = archive.namelist()
    shortest_name = sorted(names, key=len)[0]
    candidate_prefixes = [
        shortest_name[:length]
        for length in range(len(shortest_name), -1, -1)
    ]
    for prefix in candidate_prefixes:
        if all(name.startswith(prefix) for name in names):
            return prefix
    return ''


class RevivedDistribution(distutils.dist.Distribution):
    def __init__(self, source_url):
        distutils.dist.Distribution.__init__(self)
        self.source_url = source_url
        self._load_metadata()
        self._update_dist_files()

    def _load_metadata(self):
        parsed = urllib.parse.urlparse(self.source_url)
        self.filename = parsed.path
        stream = io.BytesIO(urllib.request.urlopen(self.source_url).read())
        # a little workaround for the eggmonster filename munging
        if is_targz(self.filename) and looks_like_zip(stream):
            self.filename = force_zip_extension(self.filename)
        if self._is_remote():
            # distutils expects the file to be on the file system; make it so
            self.filename = os.path.basename(self.filename)
            with open(self.filename, 'wb') as sf:
                sf.write(stream.read())
            stream.seek(0)
        archive = open_archive(stream, self.filename)
        main_dir = get_prefix_dir(archive)
        if main_dir and not main_dir.endswith('/'):
            main_dir = main_dir + '/'
        pkg_info_file = archive.open(main_dir + 'PKG-INFO')
        self.metadata = distutils.dist.DistributionMetadata()
        stream = io.StringIO(pkg_info_file.read().decode('utf-8'))
        self.metadata.read_pkg_file(stream)
        self._clean_metadata()

    def _is_remote(self):
        parsed = urllib.parse.urlparse(self.source_url)
        return parsed.scheme.lower() != 'file'

    def _clean_metadata(self):
        """
        the long description doesn't load properly (gets unwanted indents),
        so fix it.
        """
        lines = io.StringIO(self.metadata.get_long_description())
        def trim_eight_spaces(line):
            if line.startswith(' '*8):
                line = line[8:]
            return line
        lines = itertools.chain(
            itertools.islice(lines, 1),
            six.moves.map(trim_eight_spaces, lines),
        )
        self.metadata.long_description = ''.join(lines)

    def _update_dist_files(self):
        if self.filename.endswith('.egg'):
            type = 'bdist_egg'
        if self.filename.endswith('.tgz') or self.filename.endswith('.zip') or self.filename.endswith('.tar.gz'):
            type = 'sdist'
        version_pattern = re.compile(r'py\d\.\d')
        res = version_pattern.search(self.filename)
        pyversion = res.group(1) if res else ''
        distfile = DistFile(type, pyversion, self.filename)
        self.dist_files.append(distfile)

    def get_name(self):
        return self.package.name

    def get_version(self):
        return self.package.version

    def has_ext_modules(self): return False

    def cleanup(self):
        if self._is_remote():
            os.remove(self.filename)

def upload_file(repository, source, **command_params):
    distribution = RevivedDistribution(source)
    cmd = distutils.command.upload.upload(distribution)
    cmd.initialize_options()
    cmd.repository = repository
    cmd.finalize_options()
    vars(cmd).update(**command_params)
    cmd.run()
    distribution.cleanup()

def URL(spec):
    """
    If spec already looks like a URL, just return it. Otherwise, assume
    it is a filename and return it as a file url.
    """
    if urllib.parse.urlparse(spec).scheme: return spec
    return 'file:'+spec

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=URL)
    parser.add_argument('-r', '--repository', default=None)
    return parser.parse_args()

def do_upload():
    args = get_args()
    upload_file(args.repository, args.source)

if __name__ == '__main__':
    do_upload()
