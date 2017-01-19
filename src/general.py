'''
General functions for LFN project.
'''
import os
import pickle as pkl

def GetPkl(filepath):
    f = open(filepath, 'rb')
    obj = pkl.load(f)
    f.close()
    return obj

def SavePkl(obj, filepath):
    #if os.path.exists(filepath):
    #   raise IOError('File already exists')
    f = open(filepath, 'wb')
    pkl.dump(obj, f)
    f.close()

def CheckExistence(filepath, allow_overwrite=False):
    if os.path.exists(filepath):
        if allow_overwrite==False:
            raise IOError('File already exists at output location\n' + filepath)
        else: #I allow over-write if we are in test mode
            cont = 'n/a'
            while cont != 'y' and cont != 'n':
                cont = raw_input('Output file will overwrite existing file:\n'
                                    + filepath + '\nContinue? (y/n) ')
                if cont == 'y':
                    pass
                elif cont == 'n':
                    raise IOError('File already exists at output location\n'
                                    + filepath)
                else:
                    print('Must enter \'y\' or \'n\'')

def GetFlowYears(filename):
    '''Gets the 9 characters after the word 'flows', by my convention these
    are the flow years'''
    return filename.split('flows')[1][0:9]

def GetNrand(filename):
    '''Gets the 4 characters after the word 'nrand', by my convention this
    is the number of dead firms chosen completely at random in the Monte Carlo.
    If there is no nrand return an empty string.
    '''
    if 'nrand' in filename:
        return 'nrand' + filename.split('nrand')[1][:4]
    else:
        return ''


def GetDeathYears(filename):
    '''Gets the 9 characters after the word 'deaths' or gets 'all' if all.'''
    deathyears = filename.split('deaths')[1][0:3]
    if deathyears != 'all':
        deathyears = filename.split('deaths')[1][0:9]
    return deathyears

def CheckSameData(filename1, filename2):
    '''
    Checks that the two filnames inputted correspond to LFNs built from the
    same years of flows and the same firm deaths.
    '''
    #look for flow years (9 characters following 'flows')
    flowyears1 = GetFlowYears(filename1)
    flowyears2 = GetFlowYears(filename2)
    #look for deaths years ('all' or 9 characters follows 'deaths')
    deathyears1 = GetDeathYears(filename1)
    deathyears2 = GetDeathYears(filename2)
    try:
        assert flowyears1 == flowyears2
        assert deathyears1 == deathyears2
    except AssertionError:
        print(filename1, filename2)
        raise IOError
