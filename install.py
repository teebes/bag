#! /usr/bin/envs python

import filecmp
import os
import subprocess

installs = { 
    'vim': ['.vimrc'],
    'bash': ['.bashrc'],
    'screen': ['.screenrc'],
    'git': ['.gitconfig'],
}

HOME = os.getenv('HOME')
PWD = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))

def shell(cmd, verbose=True):
    if verbose:
        print '\t\t$ {0}'.format(cmd)

    output = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE).communicate()

    if verbose:
        print '\t\t{0}'.format(output)
        print

    return output
    

def install(verbose=True, symlink=True):

    home = os.getenv('HOME')
    pwd = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
    if verbose:
        print
        print 'home is {0}'.format(home)
        print 'pwd is {0}'.format(pwd)
        print

    for dir, files in installs.items():

        if verbose:
            print '\tInstalling {0}...'.format(dir)

        for file in files:
            source =  '{0}/{1}/{2}'.format(pwd, dir, file)
            destination = '{0}/{1}'.format(home, file)

            if os.path.exists(destination):
                if filecmp.cmp(source, destination): # no change
                    if verbose: 
                        print 'already installed'
                        print
                    continue

                # backup
		if verbose:
			print '\t\tBacking up to {0}.old'.format(destination)
                cmd = 'mv {0} {1}.old'.format(destination, destination)
                shell(cmd)

            if symlink:
                cmd = 'ln -s {0} {1}'.format(source, destination)
            else:
                cmd = 'cp {0} {1}'.format(source, destination)
            shell(cmd)

if __name__ == "__main__":
    install()

    print
    print 'done'
