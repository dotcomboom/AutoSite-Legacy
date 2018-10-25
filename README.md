# AutoSite
AutoSite helps you keep all of your website's pages in the same basic template. Managing a navigation bar, a footer, and even meta/OpenGraph tags across several pages is simple.
### [You can try AutoSite right in your browser!](https://repl.it/@dotcomboom/AutoSite)
## Prerequisites
   - Python 3
   - BeautifulSoup 4 (pip3 install beautifulsoup4)
## Usage
-1. Install the prerequisites with pip. `pip3 install -r requirements.txt`

0. Run the script, AutoSite.py. It will create a basic `default.html` template and the `in` and `includes` folders.
1. Edit templates/default.html, filling in with these tags:

           [#content#] - The page's content.
           [#path#] - The relative file path from root.
           [#root#] - Use this to point to the site's root folder.
           
   You can also use any other attributes, like [#title#] or [#description#], provided that you define them in each page as below.
           
2. Add your pages to the "in" folder.
      You can define a title and description, or any other attributes you wish, and tell AutoSite which template to use for the page at the top of the file like so:
           
           <!-- attrib title: Your title -->
           <!-- attrib description: Your description -->
           <!-- attrib template: default -->
           <p>Everything under the above lines will replace [#content#] in template.html.</p>
              
    Put other site files in the "includes" folder. Input pages can be HTML or Markdown files, and use the same attribute syntax.
    
3. Run the script. How long it takes depends on how large your site is. Your pages will be in the "out" folder.
## Conditional text
Many sites have a navigation where if you're on a page, that page's name in the navigation is not a link. AutoSite has a feature that lets you replicate this. Consider the following example:
	
      [path!=index.html]<a href="../index.html">[/path!=]
          Home
      [path!=index.html]</a>[/path!=]
	
You can also omit the `!` symbol and it will only show if it is that page, like this:

      [path=index.html]<p>[/path!=]
          This is the index page.
      [path=index.html]<p>[/path!=]
	
Conditional text is not limited to just file paths! Nearly any attribute can be used with conditional text.

However, Conditional text still has some issues. You can only have one instance of conditional text per line, it is not nestable, and not multiline either.
