#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup as bs
from commonmark import commonmark
from dirsync import sync
import os, time, shutil, subprocess, re, sys, argparse

def main():
    # Default parameters
    # Set these and they will always be active whether parameters are passed or not
    prettify = False
    auto = False
    quiet = False
    directory = False # Set to path
    modified_format = "%m/%d/%Y"  # <-- Adjust this for other regions


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
    parser.add_argument('-p', '--prettify', action='store_true', help='enables BeautifulSoup4 prettifying on output pages (affects whitespace')
    parser.add_argument('-a', '--auto', action='store_true', help='skips user input, for use in scripts etc; non-interactive mode')
    parser.add_argument('-q', '--quiet', action='store_true', help='runs silently, skipping user input')
    parser.add_argument('-s', '--silent', action='store_true', help='alias for --quiet')
    parser.add_argument('-d', '--dir', action='store', help='run AutoSite at a specific location')
    parser.add_argument('-m', '--modified', action='store', help='specify date format for the [#modified#] attribute (Python-style; i.e. ﹪Y-﹪m-﹪d for 1984-01-19)')
    # Parse
    args = parser.parse_args()

    if args.prettify:
        prettify = True
    if args.auto:
        auto = True
    if args.quiet or args.silent:
        quiet = True
    if args.dir:
        directory = args.dir
    if args.modified:
        modified_format = args.modified
    
    # Disable printing to console and enable auto mode with silent argument
    if quiet:
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

    indir = Path("pages/")
    # Check if indir exists
    if indir.is_dir():
        print(bcolors.OKBLUE + 'pages folder exists' + bcolors.ENDC)
    else:
        print(bcolors.WARNING + 'pages folder does not exist yet' + bcolors.ENDC)

    if Path("in/").is_dir():
        print(bcolors.WARNING + 'i This version of AutoSite Legacy uses pages/ as the folder for input pages.\n  Please rename or merge your in/ folder to pages/ if you intend to use these files.' + bcolors.ENDC)

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
        print(bcolors.WARNING + 'Creating pages folder' + bcolors.ENDC)
        # Make it
        os.mkdir("pages")

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
    for dirName, subdirList, fileList in os.walk('pages/'):
        for path in os.listdir(dirName):
            # Check if file has extension
            if '.' in path:
                # Check if it isn't common meta files used by OS X and Windows
                if '.DS_Store' not in path:
                    if 'Thumbs.db' not in path:
                        # Add the file to the list
                        files.append((dirName + "/" + path).replace('\\', '/').replace('//', '/').replace(
                    'pages/', '', 1))
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

    template_cache = {}

    # For each file
    for path in files:
        # Check if it exists
        if os.path.isfile('pages/' + path):
            # If it's markdown let user know it'll be translated into html
            if path.endswith('.md'):
                print(bcolors.BOLD + 'Path: ' + bcolors.ENDC + bcolors.OKBLUE + path + bcolors.ENDC + ' ==> ' + bcolors.OKBLUE + path[:-2] + 'html' + bcolors.ENDC)
            else:
                print(bcolors.BOLD + 'Path: ' + bcolors.ENDC + bcolors.OKBLUE + path + bcolors.ENDC)
            
            # Open, read file
            f = open('pages/' + path, 'r', encoding="utf8")
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
                # If it is, run it through commonmark to translate it into html
                content = commonmark(content)

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
            f = open('pages/' + path, 'r', encoding="utf8")
            filearray = f.readlines()
            f.close()

            # If there aren't any subdirectories between root and the file, use ./ as the slash so it doesn't refer to the root of the server for file:// compatibility
            if path.count('/') == 0:
                slash = './'
            else:
                slash = '/'
            attribs['path'] = path
            attribs['root'] = (('../' * path.count('/')) + slash).replace('//', '/')
            modified = os.path.getmtime('pages/' + path)
            attribs['modified'] = time.strftime(modified_format, time.localtime(modified))
            attribs['content'] = content
            # These attributes are set earlier so that they could be overriden if needed
            # (for example, setting the root attribute to / for a not found page 
            #  where relative paths would be impossible to predict)


            # For each line
            while len(filearray) > 0:
                line = filearray[0]
                # Check if it is an attribute
                if line.startswith('<!-- attrib '):
                    # Get the attribute being set
                    attrib = line[12:].split(':')[0].strip()
                    # Get the value it's being set to
                    value = line[(12 + len(attrib) + 2):].strip()
                    # Remove trailing -->
                    if value.endswith('-->'):
                        value = value[:-3].strip()
                    print(bcolors.BOLD + 'Attribute ' + attrib + ': ' + bcolors.ENDC + bcolors.OKBLUE + value + bcolors.ENDC)
                    # Add to attributes
                    attribs[attrib] = value
                filearray = filearray[1:]

            template = ''
            
            # Check if template is cached
            if attribs['template'] in template_cache.keys():
                template = template_cache[attribs['template']]
            else:
                # If not then load it;
                # Get the template's path
                print('Caching template', attribs['template'])
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
                # Cache
                template_cache[attribs['template']] = template

            # Create subdirectories
            os.makedirs(dirname('out/' + path), exist_ok=True)

            # Slot in content first so attributes within work
            template = template.replace('[#content#]', content)

            # For each attribute
            for key, value in attribs.items():
                # Slot it into the template
                template = template.replace('[#' + key + '#]', value)
            # Remove non-existing attributes
            # template = re.sub(r"\[\#.*\#\]", "", template)

            # Now let's handle conditional text
            # Conditional text is an experimental feature.
            # Only one is supported per line because of some regex whatever, and stuff might make it trip up
            # Example:

            # [path!=pages/link.html]<a href="[#root#]pages/link.html">[/path!=]
            #    Linking
            # [path!=pages/link.html]</a>[/path!=]
            
            # This works with any attribute.

            for atteql, value, text in re.findall(r'\[(.*)=(.*?)\](.*)\[\/\1.*\]', template):
                # Get attribute to check
                attribute = atteql

                # Check if ! is at the end ('not' conditional), trim from attribute
                check_not = (atteql[-1] == "!")
                if check_not:
                    attribute = atteql[:-1]

                # Note: at this stage all attributes will have been slotted in
                # TODO: DeMorgan's Law, more rigorous testing
                trigger = False
                if check_not and value == "" and attribute in attribs.keys():
                    # example: [bgcolor!=] style="background-color: #;"[/bgcolor!=]
                    trigger = True
                elif check_not and value == "" and attribute not in attribs.keys():
                    trigger = False
                elif not check_not and value == "" and attribute not in attribs.keys():
                    # example: [ready=partial]<div class="noticebox"><p><img src="../icon_brick.png"> This page is a work in progress, but some content is available.</p></div>[/ready=]
                    trigger = True
                elif not check_not and value == "" and attribute in attribs.keys() and attribs[attribute] != "":
                    # example: [ready=partial]<div class="noticebox"><p><img src="../icon_brick.png"> This page is a work in progress, but some content is available.</p></div>[/ready=]
                    trigger = False
                elif check_not and (attribute not in attribs.keys() or attribs[attribute] != value):
                    # example: [pizza!=pepperoni]this is not a pepperoni pizza[/pizza!=]
                    trigger = True
                elif not check_not and attribute in attribs.keys() and attribs[attribute] == value:
                    # example: [html_summary=]<p><i>HTML summary is empty</i></p>[/html_summary=]
                    trigger = True

                conditional = '[' + atteql + "=" + value + ']' + text + '[/' + atteql + '=]'
                # If triggered
                if trigger:
                    # Set it to the text
                    template = template.replace(conditional, text)
                else:
                    # Make it blank
                    template = template.replace(conditional, '')

            # If this is a markdown file, trim the md from it and make the output extension html
            if path.endswith('.md'):
                path = path[:-2] + 'html'

            # If prettifying is enabled, do that
            if prettify:
                template = bs(template, 'html.parser').prettify()

            # Check if there is a plugin directory, for each plugin execute its code
            if Path('plugins/').is_dir():
                for plugin in os.listdir('plugins/'):
                    print(bcolors.BOLD + bcolors.WARNING + 'Running plugin', plugin + bcolors.ENDC)
                    # TODO: use 'import' instead
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
