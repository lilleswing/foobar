def print_dict(memoize):
    fout = open('answer.py','w')
    for key, value in memoize.iteritems():
        s = "memoize[%s] = %s" % (key, value)
        fout.write("%s\n" % s)
    fout.close()

