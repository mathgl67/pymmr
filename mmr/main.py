import sys
import mmr
from optparse import OptionParser

class Main:
  def __init__(self):
    self.welcome()
    self.parse_args()
    self.load_config()
    self.test()

  def welcome(self):
    print "Welcome to My Music Renamer version %s" % (mmr.MMR['version'])
    print "Copyright (C) 2007 mathgl67@gmail.com"
    print "My Music Renamer comes with ABSOLUTELY NO WARRANTY;"
    print "This is free software; Release under GPL;"
    print


  def parse_args(self):
    """Parse commande line arguments"""

    #init argv parser
    usage = "usage: %prog [options] <music_directory>"
    parser = OptionParser(usage=usage, version="%s %s" % (
      mmr.MMR['prog'],
      mmr.MMR['version']
    ))

    #add option
    parser.add_option(
      "-v", "--verbose", action="store_true", dest="verbose", default=False,
      help="make lot of noise"
    )

    parser.add_option(
      "-c", "--config", dest="config", default="pymmr.cfg",
      help="Use a specific config file"
    )

    #parse
    (self.options, self.args) = parser.parse_args()
  
    #check args
    if len(self.args) < 1:
      parser.print_help()
      sys.exit(1)

  def load_config(self):
    #load config file
    try:
      self.config = mmr.Config()
      self.config.load_file(self.options.config)
    except:
      print 'could not load/parse config file (%s)' % self.options.config
      sys.exit(1)


  def test(self):
    folder = mmr.folder.Folder(self.args[0])
    print folder
    print
    
    investigate_album = mmr.InvestigateAlbum(folder)
    investigate_album.investigate()
    investigate_album.sort()

    print investigate_album.__repr__().encode('UTF-8')
    print

    investigate_track = mmr.InvestigateTrack(folder)
    investigate_track.investigate()
    
    print investigate_track.__repr__().encode('UTF-8') 

