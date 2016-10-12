Title: Setting up this blog
Date: 09/10/2016
Category: geek

Setting up this blog was pretty simple; Pelican is nice to work with!

I started out with [this article](https://michael.lustfield.net/nginx/blog-with-pelican-and-nginx) from [Michael Lustfield](https://michael.lustfield.net/)'s blog, which is a really clear intro and got me a running blog right off the bat. Then, it was just a question of shopping for a good theme -- here's a [good place to start](http://www.pelicanthemes.com/) -- and customization of the config, for which two good starting points are [Pelican's doc](http://docs.getpelican.com/en/3.6.3/quickstart.html)... and other people's configs [on GitHub](https://github.com/search?utf8=%E2%9C%93&q=filename%3Apelicanconf.py&type=Code&ref=searchresults).

Another thing that you'll probably want to do is install a few plugins. They can add some nice features, such as article summaries (and control over what gets in the summary), Flickr integration, LaTeX rendering, etc. [Here](https://github.com/getpelican/pelican-plugins)'s a nice library of plugins. To install a plugin, just download the python script, put it in a `plugins` folder at the root of your blog, and add it in the list of active plugins in your `pelicanconf.py` file.

So, why a static site? Well, why not? It's simpler, both conceptually and in terms of installation and maintenance. It's faster. It's cleaner. It consumes less CPU and storage space. For personal blogging purposes, there is no real downside - at least when you're self-hosted like me. And, in the case of Pelican, it's in Python, so if I want a feature that no plugin offers, I can always code it myself!

That's pretty much all there is to say about this blog's setup. Its whole code and config can be found on my [git repo](https://git.j11e.net/jd/blog.j11e.net).
