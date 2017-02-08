'''
Want to repeat what I had before except now introduce classes.
'''

#create class of LFN
#add methods:
#MakeLFN - from the MakeLFN function
#give plot degree distribution method
#give save info and get info method that gives out a string that can be used
#in a file name: so of the form 'flowsyear1-year2'

#create class of dead nodes
#get dead IDs

class LFN:
    '''
    Class of Labour Flow Networks.

    - Inherit from the class of networkx networks.
    - Make method: Create an LFN for the years specified
    - FilepathInfo method: return a string to be used as part of a filename
    specifying the key details of the LFN
    '''
