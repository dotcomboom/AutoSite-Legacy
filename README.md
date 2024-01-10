# AutoSite [![PyPI version](https://badge.fury.io/py/AutoSite.svg)](https://badge.fury.io/py/AutoSite)
AutoSite helps you keep all of your website's pages in the same basic template. Managing a navigation bar, a footer, and even meta/OpenGraph tags across several pages is simple.

This repository is home to the original AutoSite Python script, updated to functional parity with its .NET-based sibling, [AutoSite](https://github.com/dotcomboom/AutoSite). AutoSite Legacy is cross-platform and aims to provide an elegant CLI option.

- [PyPI package](https://pypi.org/project/AutoSite/) (currently out of date)
- [AutoSite Legacy GitHub](https://github.com/dotcomboom/AutoSite-Legacy/) (Python)
- [AutoSite GitHub](https://github.com/dotcomboom/AutoSite/) (VB.NET)

## Installation
### As a package
You can install AutoSite Legacy as a package. You can `cd` to the directory where you're building your site and build with the `autosite` command. It can be installed with the command `pip install autosite` or `pip3 install autosite` depending on your configuration.

Hacking on the script and want to install from the current master branch? You can also install with `pip3 install .`.

<!--
### As a prebuilt executable
If your platform supports it, the GitHub Releases page has/will have prebuilt executables that can be run in the console with arguments, or just double clicked in your site's working folder. Whichever you prefer!
-->

### As a standalone script
[`__init__.py`](https://github.com/dotcomboom/AutoSite-Legacy/blob/master/AutoSite/__init__.py) can be run directly, without installing the package. Just copy it into wherever you're working and you can run it from there. You'll need to install the requirements manually, which are in [the requirements.txt file](https://github.com/dotcomboom/AutoSite-Legacy/blob/master/requirements.txt) with the `pip install -r requirements.txt` or `pip3 install -r requirements.txt` commands (provided that you downloaded or wrote that file to the same directory).

## Basic Usage
0. Run `autosite`. It will create a basic `default.html` template, and the `pages`, `includes` folders.
1. Edit templates/default.html, filling in with these tags:

           [#content#] - The page's content.
           [#path#] - The relative file path from root.
           [#root#] - Use this to point to the site's root folder. Helpful for linking to files in `includes`.
           [#modified#] - The page's last modified date.
           
   You can also use any other attributes, like [#title#] or [#description#], provided that you define them in each page as below.
           
2. Add your pages to the "pages" folder.
      You can define a title and description, or any other attributes you wish, and tell AutoSite which template to use for the page at the top of the file like so:
           
           <!-- attrib title: Your title -->
           <!-- attrib description: Your description -->
           <!-- attrib template: default -->
           <p>Everything under the above lines will replace [#content#] in template.html.</p>
              
    Put other site files in the "includes" folder. Input pages can be HTML or Markdown files, and use the same attribute syntax.
    
3. Run the script. How long it takes depends on how large your site is. Your pages will be in the "out" folder.

Hungry for more? Try these helpful guides on how AutoSite works, contributed by [mariteaux](http://mariteaux.somnolescent.net):
- [The original AutoSite Legacy guide](http://archives.somnolescent.net/web/autosite_legacy/)
- [The official AutoSite Manual](http://autosite.somnolescent.net/manual/)

## Customization
Run `autosite --help` for more options (see below)!

    usage: autosite [-h] [-p] [-a] [-q] [-s] [-d DIR] [-m MODIFIED]

    options:
    -h, --help            show this help message and exit
    -p, --prettify        enables BeautifulSoup4 prettifying on output pages (affects whitespace)
    -a, --auto            skips user input, for use in scripts etc; non-interactive mode
    -q, --quiet           runs silently, skipping user input
    -s, --silent          alias for --quiet
    -d DIR, --dir DIR     run AutoSite at a specific location
    -m MODIFIED, --modified MODIFIED
                            specify date format for the [#modified#] attribute (strftime format; i.e. %Y-%m-%d for 1984-01-19 or %-m/%-d/%Y (*nix) or %#m/%#d/%Y (Windows) for 1/19/1984)

> **Date format note**: This version defaults to YYYY-MM-DD date format. .NET AutoSite uses the system locale as of 1.0, though this behavior may change. The --modified flag allows for a different [time format](https://www.strfti.me/) to be used.

> **Site path note**: AutoSite Core uses the site location as a parameter on its own (no flag behind it). This currently isn't the case with Legacy; --dir currently must be used to build a site outside of the current working directory.

### Example Command

    autosite --auto --modified "%#m/%#d/%Y" --dir "C:\Users\dcb\Desktop\AutoSite.1.0.Gold\SampleSite"

## Conditional text
Many sites have a navigation where if you're on a page, that page's name in the navigation is not a link. AutoSite has a feature that lets you replicate this. Consider the following example:
	
      [path!=index.html]<a href="[#root#]index.html">[/path!=]
          Home
      [path!=index.html]</a>[/path!=]
	
You can also omit the `!` symbol and it will only show if it is that page, like this:

      [path=index.html]<p>[/path=]
          This is the index page.
      [path=index.html]<p>[/path=]
	
Conditional text is not limited to just file paths! Nearly any attribute can be used with conditional text. 

As of 1.4, it is also possible to check for emptiness, like AutoSite (.NET). For example:

      [ready=]This page is not ready (its ready attribute is not set)[/ready=]
      [subtitle!=]<h2>[#title#]</h2>[/subtitle!=]

However, conditional text still has some limitations. You can only have one instance of conditional text per line, it is not nestable, and not multiline either.
