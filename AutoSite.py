from pathlib import Path
import bs4, os, shutil, glob
from bs4 import BeautifulSoup as bs

print('AUTOSITE')
print()

template = Path('template.html')
if template.is_file():
    print('template.html exists.')
else:
    print('template.html does not exist, creating default one..')
    defaulttemplate = '<!DOCTYPE html><html><head> <meta charset="utf-8"/> <title>[#title#]</title> <meta property="og:type" content="website"/> <meta property="og:image" content=""/> <meta name="og:site_name" content="AutoSite"/> <meta name="og:title" content="[#title#]"/> <meta name="og:description" content="[#description#]"> <meta name="theme-color" content="#333333"/></head><body><header><h2>[#title#]</h2></header><main>[#content#]</main><footer><hr/><p>Generated with AutoSite</p></footer></body></html>'
    with open('template.html', 'w') as f:
        f.write(bs(defaulttemplate, "html.parser").prettify())
        f.close()

indir = Path("in/")
if indir.is_dir():
    print('in folder exists.')
else:
    print('in folder does not exist, creating one..')
    os.mkdir("in")
    
includes = Path("includes/")
if includes.is_dir():
    print('includes folder exists.')
else:
    print('includes folder does not exist, creating one..')
    os.mkdir("includes")

print()
print('When you are ready to begin, press enter.')
input()
print('Gathering filenames')
files = []
for dirName, subdirList, fileList in os.walk('in/'):
    for filename in os.listdir(dirName):
        files.append((dirName + "/" + filename).replace('//','/').replace('in/', '', 1))
outdir = Path("out/")
if outdir.is_dir():
    print('Deleting out folder')
    shutil.rmtree('out/')
print('Copying includes folder to out folder')
shutil.copytree('includes', 'out')

print('Reading template')
f = open('template.html', 'r')
template = f.read()
f.close()

print('Going through input files')
print()

for filename in files:
    if os.path.isfile('in/' + filename):
        print('Filename: ' + filename)
        f = open('in/' + filename, 'r')
        filearray = f.readlines()
        f.close()
        
        if filearray[0].startswith('<!-- '):
            title = filearray[0].replace('<!--', '').replace('-->', '').strip()
            print('Title: ' + title)
            filearray = filearray[1:]
        else:
            print('First line did not have comment for title!')
            title = ""
            
        if filearray[0].startswith('<!-- '):
            description = filearray[0].replace('<!--', '').replace('-->', '').strip()
            print('Description: ' + description)
            filearray = filearray[1:]
        else:
            print('Second line did not have comment for description!')
            description = ""
            
        content = ''.join(filearray)

        os.makedirs(os.path.dirname('out/' + filename), exist_ok=True)
        
        f = open('out/' + filename, 'w')
        f.write(template.replace('[#content#]', content).replace('[#title#]', title).replace('[#description#]', description))
        f.close()
        print('Wrote to out/' + filename)
        print()
print('Finished.')
