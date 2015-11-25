import os
filelist = map(lambda x: x.split('.')[0], filter(lambda x: x.endswith('intro'), os.listdir('tmpfile')))

