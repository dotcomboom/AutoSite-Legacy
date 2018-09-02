# AutoSite
AutoSite helps you keep all of your website's pages in the same basic template. Managing a navigation bar, a footer, and even meta/OpenGraph tags across several pages is simple.
### [You can try AutoSite right in your browser!](https://repl.it/@dotcomboom/AutoSite)
## Prerequisites
   - Python 3
   - BeautifulSoup 4 (pip3 install beautifulsoup4)
## Usage
0. Run the script, AutoSite.py. It will create a basic `template.html` page and the `in` and `includes` folders.
1. Edit template.html, filling in with these tags:

           [#title#] - The title of the page.
           [#description#] - The page's description.
           [#content#] - The page's content.
           [#path#] - The relative file path from root.
           
2. Add your pages to the "in" folder.
      You can define the title and description of the page with the first two lines like so:
           
           <!-- Your title -->
           <!-- Your description -->
           <p>Everything under these two lines will replace [#content#] in template.html.</p>
              
    Put other site files in the "includes" folder.
3. Run the script. How long it takes depends on how large your site is. Your pages will be in the "out" folder.
