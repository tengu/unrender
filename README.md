unrender
========

Reverse engineer templated outputs

Status: proof of concept

### path

Summarize a stream of paths into patterns that could have produce them.

* Example

        $ unrender.py path --threashold=3 <<END

        /data/band/black-sabbath.json
        /data/band/judas-priest.json
        /data/band/deep-purple.json
        /data/band/iron-maiden.json
        /data/band/motörhead.json
        /www/favicon.ico
        /www/metal.css
        /www/html/black-sabbath.html
        /www/html/judas-priest.html
        /www/html/deep-purple.html
        /www/html/iron-maiden.html
        /www/html/motörhead.html
        END

        /www/html/*
        /data/band/*
        /www/favicon.ico
        /www/metal.css

### html

TODO

Reduce html tree by collapsing nodes with similar children.

For example:

        html
         body
          table
           tr
            th
             "item"
            th
             "price"
           tr
            td
             "foo"
            td
             "42"
           tr 
	    .. # repeated many times
          div
           "footer"

would be reduced to

        html
         body
          table
           tr
            th
             "item"
            th
             "price"
           tr
            td
             $1
            td
             $2
          div
           "footer"

because the tr nodes repeats with similar pattern below it. 

Values in collapsed nodes are extracted and are annotated with xpath leading to them.
