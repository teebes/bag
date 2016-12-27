#! /usr/bin/env python

import argparse
import filecmp
import os
import subprocess

installs = {
    'vim': ['.vimrc'],
    'bash': ['.bashrc'],
    'screen': ['.screenrc'],
    'git': ['.gitconfig'],
    'profile': ['.profile',]
}

HOME = os.getenv('HOME')
PWD = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))

def shell(cmd, verbose=True):
    if verbose:
        print('\t\t$ {0}'.format(cmd))

    output = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE).communicate()

    if verbose:
        print('\t\tOutput: %s\n' % str(output))

    return output


def install(verbose=True, symlink=True, backup=False):

    home = os.getenv('HOME')
    pwd = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
    if verbose:
        print('\nhome is {0}'.format(home))
        print('pwd is {0}\n'.format(pwd))

    for dir, files in installs.items():

        if verbose:
            print('\tInstalling {0}...'.format(dir))

        for file in files:
            source =  '{0}/{1}/{2}'.format(pwd, dir, file)
            destination = '{0}/{1}'.format(home, file)

            if os.path.exists(destination):
                if filecmp.cmp(source, destination): # no change
                    if verbose:
                        print('\tNo change.\n')
                    continue

            if backup:
                if verbose:
        			print('\t\tBacking up to %s.old' % destination)

                cmd = 'mv {0} {1}.old'.format(destination, destination)
                shell(cmd, verbose=verbose)

            if symlink:
                cmd = 'ln -s {0} {1}'.format(source, destination)
            else:
                cmd = 'cp {0} {1}'.format(source, destination)
            shell(cmd, verbose=verbose)

def main():
    parser = argparse.ArgumentParser(
        description='Install Terminal scripts')
    parser.add_argument(
        '-b', '--backup',
        action='store_true',
        help='Create backup of existing files before overwriting.')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print extra information.')
    parser.add_argument(
        '-s', '--symlink',
        action='store_true',
        help='Symlink the shell config files instead of copying them.')

    args = parser.parse_args()
    install(
        symlink=args.symlink,
        verbose=args.verbose,
        backup=args.backup)

if __name__ == "__main__":
    main()
    #install(symlink=False)

