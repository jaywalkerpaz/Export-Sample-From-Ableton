#EXPORT AUDIO SAMPLE FROM ABLETON

#USAGE: CD to the directory containing this script and run 'python exportAudio.py [name]'. The [name] argument can be unique and is used to create a new directory for the resulting file.

#PURPOSE: Exporting sample clips from Ableton involves selecting an audio clip, clicking 'export audio', setting the export settings with a dialog box, renaming the file, and placing it in a specific folder. Samples may have the beginning milliseconds chopped off, or include unnecessary silence at the beginning or end of the file. This script processes audio files and automates all of these processes.

#DESCRIPTION:
#After setting the Ableton project directory in this script, the latest sample file is found. Using SOX, the file is processed to remove any silence before and after the sample. The file is moved to a temp folder, where it can be transferred back to Ableton for further processing. Optionally, the sample can be stored in a "COLLECTION' folder to build a sample library.

#VARIABLES:
#The 'vSampleDir' is used to place the temp file and COLLECTION folder and can be modified.
#The 'vAbletonFiles' variable references the chosen Ableton project's 'Recorded' folder.

#NOTE:
#A different directory is created for each unique argument (ex: 'python exportAudio.py "Kick"' creates a "Kick" directory, and the resulting filename may be Kick/Kick01.wav).
#SOX must be installed (brew install sox).
###

import subprocess, os, glob, sys, re
from pathlib import Path
from tkinter import *
from tkinter import simpledialog
home = str(Path.home())

class exportAudio():
    #Vars
    def __init__(self):
        self.arg1 = sys.argv[1]
        self.vSamplesDir = home+'/Music/AUDIO/ABLETON/ABLETON USER LIBRARY/SETSAMPLES/PYRESA/' # MODIFY THE SAMPLES DIRECTORY IF NEEDED
        self.vSampleFolder = self.vSamplesDir+self.arg1
        self.vCollectionDir = home+self.vSamplesDir+'COLLECTION/'+self.arg1
        self.vAbletonFiles = glob.glob(home+'/Music/AUDIO/ABLETON/SETS/JSBUILD Project/Samples/Recorded/*') # MODIFY THE ABLETON PROJECT DIR IF NEEDED
        self.i = []

    #Check for directories
    def createDirs(self):
        if not os.path.exists(self.vSamplesDir):
            os.system('mkdir '+self.vSamplesDir)
        if not os.path.exists(self.vSampleFolder+'/'):
            os.system('mkdir "'+self.vSampleFolder+'"/')
        if not os.path.exists(self.vCollectionDir):
            os.system('mkdir "'+self.vCollectionDir+'"')
        
    #Process latest recorded file
    def processLatestFile(self):
        #check for file size or exits
        self.vLatestFile = max(self.vAbletonFiles, key=os.path.getctime)
        if os.path.exists(self.vLatestFile):
            self.vFileStat = os.stat(self.vLatestFile)
            self.vFileSize = self.vFileStat.st_size
            if self.vFileSize<=80:
                print('FILE DELETED: file size is zero')
                os.system('rm "'+self.vLatestFile+'"')
                sys.exit()
            os.system('mv "' +self.vLatestFile+ '" "'+self.vSamplesDir+'"test.wav')
            os.system('cd "'+self.vSamplesDir+'" && sox "'+self.vSamplesDir+'"test.wav "'+self.vSamplesDir+'"test2.wav silence 1 0 0 reverse silence 1 0 0 reverse')

    #Get file number suffix in sample folder
    def getNumberSuffix(self):
        self.fileList = os.listdir(self.vSampleFolder+'/')
        for self.filename in self.fileList:
            if filename.endswith('.wav'):
            #if '-' in self.filename:
                self.files = (self.filename.split('-'))[1]
                self.i+=re.findall(r'\d+', self.files)
        if not self.i:
            self.i = [0]
        self.i = int(max(self.i))
        if self.i == 0:
            print('folder sample started at 0, self.i= '+str(self.i))

    #Increase new file suffix by 1
    def increaseNumberSuffix(self):
        if os.path.exists(self.vSampleFolder+'/'+self.arg1+'%s.wav' % self.i):
            os.system('rm "'+self.vSampleFolder+'"/"'+self.arg1+'"%s.wav' % self.i)
            self.i += 1

    #Move test2.wav and rename
    def moveSamples(self):
        os.system('mv "'+self.vSamplesDir+'"test2.wav "'+self.vSampleFolder+'"/"'+self.arg1+'"%s.wav' % self.i)
        os.system('cd ~ && play "'+self.vSampleFolder+'"/'+self.arg1+'%s.wav' % self.i)

    def promptForCollection(self):
        root = Tk()
        root.withdraw()
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        self.vTyped = simpledialog.askstring(title="Save to Collection?",
                                  prompt="Type a key to save to Collection..")
        
    def moveToCollection(self):
    #copy moved file to Collection
        if self.vTyped != '':
            print('saved')
            os.system('cp "'+self.vSampleFolder+'"/"'+self.arg1+str(self.i)+'".wav "'+self.vCollectionDir+'"/"'+self.arg1+'"%s.wav' % self.i)

def main():
    X = exportAudio()
    X.__init__()
    X.createDirs()
    X.processLatestFile()
    X.getNumberSuffix()
    X.increaseNumberSuffix()
    X.moveSamples()
    X.promptForCollection()
    X.moveToCollection()

if __name__ == "__main__":
    main()

# EOF
