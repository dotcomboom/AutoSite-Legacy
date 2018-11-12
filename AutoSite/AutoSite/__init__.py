from pathlib import Path
import os, shutil
from bs4 import BeautifulSoup as bs
from markdown import markdown
import subprocess
import re
subprocess.call('', shell=True)

# https://stackoverflow.com/a/287944
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#

print(bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'AUTOSITE' + bcolors.ENDC)
print()

template = Path('templates/default.html')
if template.is_file():
    print(bcolors.OKBLUE + 'templates/default.html exists' + bcolors.ENDC)
else:
    print(bcolors.WARNING + 'templates/default.html does not exist' + bcolors.ENDC)
    os.makedirs(os.path.dirname(template), exist_ok=True)
    oldtemplate = Path('template.html')
    if oldtemplate.is_file():
        print(bcolors.OKBLUE + 'Legacy template.html exists, migrating' + bcolors.ENDC)
        shutil.copyfile('template.html', 'templates/default.html')
    else:
        print(bcolors.WARNING + 'Creating one' + bcolors.ENDC)
        defaulttemplate = '<!DOCTYPE html><html><head> <meta charset="utf-8"/> <title>[#title#]</title> <meta property="og:type" content="website"/> <meta property="og:image" content=""/> <meta name="og:site_name" content="AutoSite"/> <meta name="og:title" content="[#title#]"/> <meta name="og:description" content="[#description#]"> <meta name="theme-color" content="#333333"/></head><body><header><h2>[#title#]</h2></header><main>[#content#]</main><footer><hr/><p>Generated with AutoSite</p></footer></body></html>'
        with open(template, 'w') as f:
            f.write(bs(defaulttemplate, "html.parser").prettify())
            f.close()

indir = Path("in/")
if indir.is_dir():
    print(bcolors.OKBLUE + 'in folder exists' + bcolors.ENDC)
else:
    print(bcolors.WARNING + 'in folder does not exist, creating one' + bcolors.ENDC)
    os.mkdir("in")

includes = Path("includes/")
if includes.is_dir():
    print(bcolors.OKBLUE + 'includes folder exists' + bcolors.ENDC)
else:
    print(bcolors.WARNING + 'includes folder does not exist, creating one' + bcolors.ENDC)
    os.mkdir("includes")

print()
print(bcolors.HEADER + bcolors.BOLD + 'When you are ready to begin, press enter.' + bcolors.ENDC)
input()
print(bcolors.HEADER + bcolors.BOLD + 'Gathering file paths' + bcolors.ENDC)
files = []
for dirName, subdirList, fileList in os.walk('in/'):
    for path in os.listdir(dirName):
        if '.' in path:
            if '.DS_Store' not in path:
                if 'Thumbs.db' not in path:
                    files.append((dirName + "/" + path).replace('//', '/').replace(
                'in/', '', 1))
print(files)
outdir = Path("out/")
if outdir.is_dir():
    print(bcolors.HEADER + bcolors.BOLD + 'Deleting out folder' + bcolors.ENDC)
    shutil.rmtree('out/')
print(bcolors.HEADER + bcolors.BOLD + 'Copying includes folder to out folder' + bcolors.ENDC)
shutil.copytree('includes', 'out')

print(bcolors.HEADER + bcolors.BOLD + 'Going through input files' + bcolors.ENDC)
print()

for path in files:
    if os.path.isfile('in/' + path):
        if path.endswith('.md'):
            print(bcolors.BOLD + 'Path: ' + bcolors.ENDC + bcolors.OKBLUE + path + bcolors.ENDC + ' ==> ' + bcolors.OKBLUE + path[:-2] + 'html' + bcolors.ENDC)
        else:
            print(bcolors.BOLD + 'Path: ' + bcolors.ENDC + bcolors.OKBLUE + path + bcolors.ENDC)
        f = open('in/' + path, 'r', encoding="utf8")
        filearray = f.readlines()
        contentarray = filearray
        while contentarray[0].startswith('<!-- '):
            contentarray = contentarray[1:]
        content = ''.join(contentarray)
        f.close()

        if path.endswith('.md'):
            content = markdown(content)

        attribs = {'title': '', 'description': '', 'template': 'default'}

        # legacy

        if filearray[0].startswith('<!-- ') and not filearray[0].startswith('<!-- attrib'):
            title = filearray[0].replace('<!--', '').replace('-->', '').strip()
            print(bcolors.BOLD + 'Legacy Title: ' + bcolors.ENDC + bcolors.OKBLUE + title + bcolors.ENDC)
            filearray = filearray[1:]
        else:
            title = ""

        if filearray[0].startswith('<!-- ') and not filearray[0].startswith('<!-- attrib'):
            description = filearray[0].replace('<!--', '').replace('-->',
                                                                   '').strip()
            print(bcolors.BOLD + 'Legacy Description: ' + bcolors.ENDC + bcolors.OKBLUE + description + bcolors.ENDC)
            filearray = filearray[1:]
        else:
            description = ""

        if filearray[0].startswith('<!-- ') and not filearray[0].startswith('<!-- attrib'):
            template = filearray[0].replace('<!--', '').replace('-->', '').strip()
            print(bcolors.BOLD + 'Legacy Template: ' + bcolors.ENDC + bcolors.OKBLUE + template + bcolors.ENDC)
            filearray = filearray[1:]
        else:
            template = "default"

        attribs['title'] = title
        attribs['description'] = description
        attribs['template'] = template

        # handle new attributes
        f = open('in/' + path, 'r', encoding="utf8")
        filearray = f.readlines()
        f.close()

        while len(filearray) > 0:
            if filearray[0].startswith('<!-- attrib '):
                attrib = filearray[0].replace('<!-- attrib ', '').replace('-->', '').strip().split(': ')[0]
                value = filearray[0].replace('<!-- attrib ', '').replace('-->', '').strip().split(': ')[1]
                print(bcolors.BOLD + 'Attribute ' + attrib + ': ' + bcolors.ENDC + bcolors.OKBLUE + value + bcolors.ENDC)
                attribs[attrib] = value
            filearray = filearray[1:]

        # cool

        template = 'templates/' + attribs['template'] + '.html'

        if not Path(template).is_file():
            print(bcolors.WARNING + 'Creating ' + template + bcolors.ENDC)
            defaulttemplate = '<!DOCTYPE html><html><head> <meta charset="utf-8"/> <title>[#title#]</title> <meta property="og:type" content="website"/> <meta property="og:image" content=""/> <meta name="og:site_name" content="AutoSite"/> <meta name="og:title" content="[#title#]"/> <meta name="og:description" content="[#description#]"> <meta name="theme-color" content="#333333"/></head><body><header><h2>[#title#]</h2></header><main>[#content#]</main><footer><hr/><p>Generated with AutoSite</p></footer></body></html>'
            with open(template, 'w') as f:
                f.write(bs(defaulttemplate, "html.parser").prettify())
                f.close()

        f = open(template, 'r', encoding="utf8")
        template = f.read()
        f.close()

        os.makedirs(os.path.dirname('out/' + path), exist_ok=True)

        if path.count('/') == 0:
            slash = './'
        else:
            slash = '/'

        attribs['content'] = content
        attribs['path'] = path
        attribs['root'] = (('../' * path.count('/')) + slash).replace('//', '/')
        # these still have higher priority, do them first anyway just in case
        template = template.replace('[#content#]', attribs['content']).replace('[#path#]', attribs['path']).replace('[#root#]', attribs['root'])

        for key, value in attribs.items():
            template = template.replace('[#' + key + '#]', value)

        # now let's handle conditional text
        # conditional text is an experimental feature.
        # only one is supported per line because of some regex whatever, and stuff might make it trip up
        # example:

        # [path!=pages/link.html]<a href="[#root#]pages/link.html">[/path!=]
        #    Linking
        # [path!=pages/link.html]</a>[/path!=]
        
        # this works with any attribute.
        for atteql, value, text in re.findall(r'\[(.*)=(.*?)\](.*)\[\/\1.*\]', template):
            atteql += '='
            attribute = atteql.replace('!=', '').replace('=', '')
            equals = atteql.replace(attribute, '')

            trigger = False

            if attribute == 'path':
                if path == value:
                    trigger = True
            else:
                for key, val in attribs.items():
                    if key == attribute:
                        if val == value:
                            trigger = True

            if equals == '!=':
                trigger = not trigger

            if trigger:
                template = template.replace('[' + atteql + value + ']' + text + '[/' + atteql + ']', text)
            else:
                template = template.replace('[' + atteql + value + ']' + text + '[/' + atteql + ']', '')

        if path.endswith('.md'):
            path = path[:-2] + 'html'

        f = open('out/' + path, 'w', encoding="utf8")
        f.write(template)
        f.close()
        print(bcolors.BOLD + bcolors.OKGREEN + 'Wrote to out/' + path + bcolors.ENDC)
        print()
print(bcolors.BOLD + bcolors.HEADER + bcolors.OKGREEN + 'Finished.' + bcolors.ENDC)