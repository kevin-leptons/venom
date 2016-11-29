import os
import shutil

from logger import stdlog, stat_done


def diff_file(odir, sdir, dest):
    '''
    Create new directory with same structrure with odir, contains files in
    odir and not in sdir. If dest directory is not exist, create it. If dest
    directory is exist, terminate

    :param str odir: Original directory
    :param str sdir: Directory to compare with odir
    :param str dest: New directory
    :raise RuntimeError: On dest directory is exist
    '''

    if os.path.isdir(dest):
        raise RuntimeError('{} is early exists', dest)

    for root, dirs, files in os.walk(odir):
        rroot_odir = root[len(odir):].strip('/')
        root_sdir = os.path.join(sdir, rroot_odir)
        root_ddir = os.path.join(dest, rroot_odir)

        root_ddir_exist = False

        for fname in files:

            s_file = os.path.join(root_sdir, fname)
            if os.path.exists(s_file):
                continue

            if not root_ddir_exist:
                root_ddir_exist = True
                if not os.path.isdir(root_ddir):
                    os.makedirs(root_ddir)

            o_file = os.path.join(root, fname)
            d_file = os.path.join(root_ddir, fname)

            if os.path.islink(o_file):
                link = os.readlink(o_file)
                os.symlink(link, d_file)
            else:
                shutil.copyfile(o_file, d_file)

            stdlog(stat_done, 'copied', fname)
