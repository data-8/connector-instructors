"""Miscellaneous utility and IO functions."""
import os
import os.path as op
import numpy as np
from mne.utils import _fetch_file
from subprocess import check_output
from zipfile import ZipFile


def url_to_interact(url, url_type='datahub', https=False):
    """Create an interact link from a URL in github or data-8.org.

    Parameters
    ----------
    url : string
        The URL of the file/folder you want to convert to an interact link.
    url_type : one of 'datahub' | 'ds8' | 'data8'
        Whether the output URL should be attached to ds8 or data8.
    """
    # First define the repo name
    if not any([i in url for i in ['data-8', 'data8.org']]):
        raise ValueError('Provide a URL attached to a data-8 repository')
    if 'github.com' in url:
        repo_split = 'data-8/'
    elif 'data8.org' in url:
        repo_split = 'data8.org/'
    else:
        raise ValueError('Provide a URL for github.com or data8.org')
    repo = url.split(repo_split)[-1].split('/')[0]

    # Now pull file path/name
    name_split = 'gh-pages/' if 'github.com' in url else repo + '/'
    name = url.split(name_split)[-1]

    pre = 'https' if https is True else 'http'
    url_int = '{3}://{2}.berkeley.edu/hub/interact?repo={0}&path={1}'.format(
        repo, name, url_type, pre)
    print('Your interactive URL is:\n---\n{0}\n---'.format(url_int))
    return url_int


def download_file(url, name, root_destination='~/data/', zipfile=False,
                  replace=False):
    """Download a file from dropbox, google drive, or a URL.

    This will download a file and store it in a '~/data/` folder,
    creating directories if need be. It will also work for zip
    files, in which case it will unzip all of the files to the
    desired location.

    Parameters
    ----------
    url : string
        The url of the file to download. This may be a dropbox
        or google drive "share link", or a regular URL. If it
        is a share link, then it should point to a single file and
        not a folder. To download folders, zip them first.
    name : string
        The name / path of the file for the downloaded file, or
        the folder to zip the data into if the file is a zipfile.
    root_destination : string
        The root folder where data will be downloaded.
    zipfile : bool
        Whether the URL points to a zip file. If yes, it will be
        unzipped to root_destination + name.
    replace : bool
        If True and the URL points to a single file, overwrite the
        old file if possible.
    """
    # Make sure we have directories to dump files
    home = op.expanduser('~')
    tmpfile = home + '/tmp/tmp'
    if not op.isdir(home + '/data/'):
        print('Creating data folder...')
        os.makedirs(home + '/data/')

    if not op.isdir(home + '/tmp/'):
        print('Creating tmp folder...')
        os.makedirs(home + '/tmp/')

    download_path = _convert_url_to_downloadable(url)

    # Now save to the new destination
    out_path = root_destination.replace('~', home) + name
    if not op.isdir(op.dirname(out_path)):
        print('Creating path {} for output data'.format(out_path))
        os.makedirs(op.dirname(out_path))

    if zipfile is True:
        _fetch_file(download_path, tmpfile)
        myzip = ZipFile(tmpfile)
        myzip.extractall(out_path)
        os.remove(tmpfile)
    else:
        if len(name) == 0:
            raise ValueError('Cannot overwrite the root data directory')
        if replace is False and op.exists(out_path):
            raise ValueError('Path {} exists, use `replace=True` to '
                             'overwrite'.format(out_path))
        _fetch_file(download_path, out_path)
    print('Successfully moved file to {}'.format(out_path))


def install_package(name=None, url=None, update=True, userdir=True):
    """Use a shell command to update neurods."""
    if name is not None:
        packagecall = name
    elif url is not None:
        if not url.endswith('.git'):
            raise ValueError('Url must end with .git (must be a git repo)')
        packagecall = 'git+' + url
    s = 'pip install ' + packagecall
    if userdir is True:
        s = s + ' --user'
    if update is True:
        s = s + ' --upgrade'
    print('Installing with command: \n{}'.format(s))
    s = check_output(s.split(' '))
    s = s.decode('utf-8')
    print("Finished installing. Don't forget to restart the kernel!")


def group_students(n_students, n_per_group=2):
    """Create random pairs of indices for student groups.

    Parameters
    ----------
    n_students : int
        The number of students in the class
    n_per_group : int
        The number of students per group. If the number of students doesn't
        evenly split into groups, then a few groups will have an extra student.
    """
    # Shuffle indices
    ixs = np.arange(1, n_students + 1, 1)
    ixs_shuffled = np.random.permutation(ixs)
    remainder = n_students % n_per_group

    # Split so we can easily group
    extra = ixs_shuffled[:remainder]
    ixs_shuffled = ixs_shuffled[remainder:]

    # Now do the grouping and add the extras
    groups = ixs_shuffled.reshape([-1, n_per_group])
    groups = [list(grp) for grp in groups]
    for ii, ex in enumerate(extra):
        groups[ii].append(ex)
    return groups


def _convert_url_to_downloadable(url):
    """Convert a url to the proper style depending on its website."""

    if 'drive.google.com' in url:
        raise ValueError('Google drive links are not currently supported')
        # For future support of google drive
        file_id = url.split('d/').split('/')[0]
        base_url = 'https://drive.google.com/uc?export=download&id='
        out = '{}{}'.format(base_url, file_id)
    elif 'www.dropbox.com' in url:
        out = url.replace('www.dropbox.com', 'dl.dropboxusercontent.com')
    else:
        out = url
    return out
