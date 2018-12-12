#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup as bs
from markdown import markdown
from dirsync import sync
import os, shutil, subprocess, re, sys, argparse

def main():
    # Default parameters
    # Set these and they will always be active whether parameters are passed or not
    prettify = False
    auto = False
    silent = False
    directory = False # Set to path

    # Enable colors
    subprocess.call('', shell=True)
    
    # Class of colors
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

    def dirname(path):
        # Replacement for os.path.dirname() which is broken on some versions of Python (3.5.2 and maybe others)
        return '/'.join(str(path).split('/')[:-1])
    
    # Define arguments, help
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-p', '--prettify', action='store_true', help='enables BeautifulSoup4 prettifying on output pages (experimental)')
    parser.add_argument('-a', '--auto', action='store_true', help='skips user input, for use in scripts etc')
    parser.add_argument('-s', '--silent', action='store_true', help='runs silently, skipping user input')
    parser.add_argument('-d', '--dir', action='store', help='run AutoSite at a specific location')
    # Parse
    args = parser.parse_args()

    if args.prettify:
        prettify = True
    if args.auto:
        auto = True
    if args.silent:
        silent = True
    if args.dir:
        directory = args.dir
    
    # Disable printing to console and enable auto mode with silent argument
    if silent:
        sys.stdout = open(os.devnull, 'w')
        auto = True

    # Change working directory if called for
    if directory:
        os.chdir(directory)

    # Set and prettify default template
    defaulttemplate = bs('<!DOCTYPE html><html><head><meta charset="utf-8"><title>[#title#]</title><meta property="og:type" content="website"><meta property="og:image" content=""><meta name="og:site_name" content="AutoSite"><meta name="og:title" content="[#title#]"><meta name="og:description" content="[#description#]"><meta name="theme-color" content="#333333"></head><body><header><h2>[#title#]</h2></header><main>[#content#]</main><footer><hr><p>Generated with AutoSite</p></footer></body></html>', "html.parser").prettify()

    # Blatant self-advertising
    print(bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'AUTOSITE' + bcolors.ENDC)
    print()
    print(bcolors.BOLD + 'Path: ' + bcolors.ENDC + bcolors.HEADER + os.getcwd() + bcolors.ENDC)

    # Use default template
    template = Path('templates/default.html')
    # Check if exists
    if template.is_file():
        # It does
        print(bcolors.OKBLUE + 'templates/default.html exists' + bcolors.ENDC)
    else:
        # It doesn't
        print(bcolors.WARNING + 'templates/default.html does not exist yet' + bcolors.ENDC)

    indir = Path("in/")
    # Check if indir exists
    if indir.is_dir():
        # It does
        print(bcolors.OKBLUE + 'in folder exists' + bcolors.ENDC)
    else:
        # It doesn't
        print(bcolors.WARNING + 'in folder does not exist yet' + bcolors.ENDC)

    includes = Path("includes/")
    # Check if includes folder exists
    if includes.is_dir():
        # It does
        print(bcolors.OKBLUE + 'includes folder exists' + bcolors.ENDC)
    else:
        # It doesn't
        print(bcolors.WARNING + 'includes folder does not exist yet' + bcolors.ENDC)
    
    if prettify:
        print(bcolors.BOLD + bcolors.WARNING + 'Prettifying is enabled' + bcolors.ENDC)

    if auto:
        print(bcolors.BOLD + bcolors.WARNING + 'User input is being skipped' + bcolors.ENDC)

    print()

    # Ask for user input before continuing if not being run with auto (silent enables auto too)
    if not auto:
        print(bcolors.HEADER + bcolors.BOLD + 'When you are ready to begin, press enter.' + bcolors.ENDC)
        input()

    # Create template file if it doesn't exist
    if not template.is_file():
        # It doesn't
        # Make templates directory
        if not Path('templates/').is_dir():
            os.mkdir('templates')
        # Check if there is an old template.html file and migrate it
        oldtemplate = Path('template.html')
        if oldtemplate.is_file():
            print(bcolors.OKBLUE + 'Legacy template.html exists, migrating' + bcolors.ENDC)
            # Copy template.html to templates/default.html
            shutil.copyfile('template.html', 'templates/default.html')
        else:
            print(bcolors.WARNING + 'Creating templates/default.html' + bcolors.ENDC)
            with open(str(template), 'w') as f:
                # Write default template to file
                f.write(defaulttemplate)
                f.close()

    # Create in folder if it doesn't exist
    if not indir.is_dir():
        # It doesn't
        print(bcolors.WARNING + 'Creating in folder' + bcolors.ENDC)
        # Make it
        os.mkdir("in")

    # Create includes folder if it doesn't exist
    if not includes.is_dir():
        # It doesn't
        print(bcolors.WARNING + 'Creating includes folder' + bcolors.ENDC)
        # Make it
        os.mkdir("includes")

    # Gather files
    print(bcolors.HEADER + bcolors.BOLD + 'Gathering file paths' + bcolors.ENDC)
    files = []
    # Go through each file in input folder
    for dirName, subdirList, fileList in os.walk('in/'):
        for path in os.listdir(dirName):
            # Check if file has extension
            if '.' in path:
                # Check if it isn't common meta files used by OS X and Windows
                if '.DS_Store' not in path:
                    if 'Thumbs.db' not in path:
                        # Add the file to the list
                        files.append((dirName + "/" + path).replace('\\', '/').replace('//', '/').replace(
                    'in/', '', 1))
    # Print it out
    print(files)

    outdir = Path("out/")
    # Create output directory if it doesn't exist
    if not outdir.is_dir():
        # It doesn't
        print(bcolors.WARNING + 'Creating out folder' + bcolors.ENDC)
        # Make it
        os.mkdir("out")

    # Sync includes folder to out folder first of all
    print(bcolors.HEADER + bcolors.BOLD + 'Syncing includes to out folder' + bcolors.ENDC)
    sync('includes/', 'out/', 'sync', purge=True)

    # Process input files
    print(bcolors.HEADER + bcolors.BOLD + 'Going through input files' + bcolors.ENDC)
    print()

    # For each file
    for path in files:
        # Check if it exists
        if os.path.isfile('in/' + path):
            # If it's markdown let user know it'll be translated into html
            if path.endswith('.md'):
                print(bcolors.BOLD + 'Path: ' + bcolors.ENDC + bcolors.OKBLUE + path + bcolors.ENDC + ' ==> ' + bcolors.OKBLUE + path[:-2] + 'html' + bcolors.ENDC)
            else:
                print(bcolors.BOLD + 'Path: ' + bcolors.ENDC + bcolors.OKBLUE + path + bcolors.ENDC)
            
            # Open, read file
            f = open('in/' + path, 'r', encoding="utf8")
            filearray = f.readlines()
            contentarray = filearray
            # Filter out attributes from contentarray
            if len(contentarray) > 0:
                while contentarray[0].startswith('<!-- '):
                    if len(contentarray) > 0:
                        contentarray = contentarray[1:]
                        if len(contentarray) < 1:
                            break
            # Set the content to everything in the contentarray
            content = ''.join(contentarray)
            # Close the file
            f.close()

            # Check if a markdown file
            if path.endswith('.md'):
                # If it is, run it through markdown to translate it into html
                content = markdown(content)

            # Default attributes
            attribs = {'title': '', 'description': '', 'template': 'default'}

            # Handle legacy attributes (also known as a mess)

            # These would work like:
            #    1st line: title
            #    2nd line: description
            #    3rd line: template

            # Check if it is a legacy title
            if filearray[0].startswith('<!-- ') and not filearray[0].startswith('<!-- attrib'):
                # Set title variable
                attribs['title'] = filearray[0].replace('<!--', '').replace('-->', '').strip()
                print(bcolors.BOLD + 'Legacy Title: ' + bcolors.ENDC + bcolors.OKBLUE + attribs['title'] + bcolors.ENDC)
                filearray = filearray[1:]

            # Check if it is a legacy description
            if filearray[0].startswith('<!-- ') and not filearray[0].startswith('<!-- attrib'):
                # Set description variable
                attribs['description'] = filearray[0].replace('<!--', '').replace('-->', '').strip()
                print(bcolors.BOLD + 'Legacy Description: ' + bcolors.ENDC + bcolors.OKBLUE + attribs['description'] + bcolors.ENDC)
                filearray = filearray[1:]

            # Check if it is a legacy template
            if filearray[0].startswith('<!-- ') and not filearray[0].startswith('<!-- attrib'):
                # Set template variable
                attribs['template'] = filearray[0].replace('<!--', '').replace('-->', '').strip()
                print(bcolors.BOLD + 'Legacy Template: ' + bcolors.ENDC + bcolors.OKBLUE + attribs['template'] + bcolors.ENDC)
                filearray = filearray[1:]

            # Handle new attributes

            # Open, read file
            f = open('in/' + path, 'r', encoding="utf8")
            filearray = f.readlines()
            f.close()

            # For each line
            while len(filearray) > 0:
                # Check if it is an attribute
                if filearray[0].startswith('<!-- attrib '):
                    # Get the attribute being set
                    attrib = filearray[0].replace('<!-- attrib ', '').replace('-->', '').strip().split(': ')[0]
                    # Get the value it's being set to
                    value = filearray[0].replace('<!-- attrib ', '').replace('-->', '').strip().split(': ')[1]
                    print(bcolors.BOLD + 'Attribute ' + attrib + ': ' + bcolors.ENDC + bcolors.OKBLUE + value + bcolors.ENDC)
                    # Add to attributes
                    attribs[attrib] = value
                filearray = filearray[1:]

            # Get the template's path
            template = 'templates/' + attribs['template'] + '.html'

            # If it doesn't exist, then create it from the default
            if not Path(template).is_file():
                print(bcolors.WARNING + 'Creating ' + template + bcolors.ENDC)
                # Write to file
                with open(template, 'w') as f:
                    f.write(defaulttemplate)
                    f.close()

            # Read template file
            f = open(template, 'r', encoding="utf8")
            template = f.read()
            f.close()

            # Create subdirectories
            os.makedirs(dirname('out/' + path), exist_ok=True)

            # If there aren't any subdirectories between root and the file, use ./ as the slash so it doesn't refer to the root of the server for file:// compatibility
            if path.count('/') == 0:
                slash = './'
            else:
                slash = '/'

            # Set content, path, and root attributes
            attribs['content'] = content
            attribs['path'] = path
            attribs['root'] = (('../' * path.count('/')) + slash).replace('//', '/')

            # These special attributes still have higher priority, do them first anyway just in case ¯\_(ツ)_/¯
            template = template.replace('[#content#]', attribs['content']).replace('[#path#]', attribs['path']).replace('[#root#]', attribs['root'])

            # For each attribute
            for key, value in attribs.items():
                # Slot it into the template
                template = template.replace('[#' + key + '#]', value)

            # Now let's handle conditional text
            # Conditional text is an experimental feature.
            # Only one is supported per line because of some regex whatever, and stuff might make it trip up
            # Example:

            # [path!=pages/link.html]<a href="[#root#]pages/link.html">[/path!=]
            #    Linking
            # [path!=pages/link.html]</a>[/path!=]
            
            # This works with any attribute.

            for atteql, value, text in re.findall(r'\[(.*)=(.*?)\](.*)\[\/\1.*\]', template):
                # Add equal sign to =
                # atteql is the combination of the attribute and the equal sign
                # If atteql was !, for (if not) then it would be !=, if it was nothing, it'd be =. absolute genius!!!
                atteql += '='
                # Get the attribute
                attribute = atteql.replace('!=', '').replace('=', '')
                # Get the equal sign
                equals = atteql.replace(attribute, '')

                # Whether to display
                trigger = False

                # For each attribute
                for key, val in attribs.items():
                    # If it's the one we're looking for
                    if key == attribute:
                        # If the value is equal
                        if val == value:
                            # Trigger
                            trigger = True

                # Check if we're going to display if it is NOT equal
                if equals == '!=':
                    # Reverse the trigger
                    trigger = not trigger

                # If triggered
                if trigger:
                    # Set it to the text
                    template = template.replace('[' + atteql + value + ']' + text + '[/' + atteql + ']', text)
                else:
                    # Make it blank
                    template = template.replace('[' + atteql + value + ']' + text + '[/' + atteql + ']', '')

            # If this is a markdown file
            if path.endswith('.md'):
                # Trim the md from it and make the output extension html
                path = path[:-2] + 'html'

            # If prettifying is enabled, do that
            if prettify:
                template = bs(template, 'html.parser').prettify()

            # Check if there is a plugin directory
            if Path('plugins/').is_dir():
                # For each plugin
                for plugin in os.listdir('plugins/'):
                    # Execute the code inside
                    print(bcolors.BOLD + bcolors.WARNING + 'Running plugin', plugin + bcolors.ENDC)
                    lcls = locals()
                    ran = exec(open('plugins/' + plugin).read(), globals(), lcls)
                    template = lcls['template']

            # Open file and write our contents
            f = open('out/' + path, 'w', encoding="utf8")
            f.write(template)
            f.close()

            # We are done!
            print(bcolors.BOLD + bcolors.OKGREEN + 'Wrote to out/' + path + bcolors.ENDC)
            print()

    # All files processed
    print(bcolors.BOLD + bcolors.HEADER + bcolors.OKGREEN + 'Finished.' + bcolors.ENDC)
    # Terminate to avoid repeats
    sys.exit()

# If not run through package script "autosite" (in that case the script would already have run and terminated itself), but from the file directly run
main()
