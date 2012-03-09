"""
    Simple Site Management
    
    Node -- represents a node you can reach at an url.
        user - can be null - user sites are different and not to implement right now.
        slug - the url part
        title - the title - can be null
        subtitle - the subtitle - can be null
        icon - different icon? - can be null
        image - the main image - can be null
        date_created
        date_modified
        parent - the parent node. 
                note: a node with his parent will not be accessible thru 
                the website, but thru its parent node.
                respective: children
        options - json dictionary. saves node options to be retrieved thru the
                respective software.
    
    NodeHtml -- represents a node that holds one bit of html (a site)
        as_html - the function should be called by the template
        source - the actual input source, like html or wiki syntax
        source_type - the actual source type. integer. refers to the source type of the node.
            0 - plain text
            1 - html
            2 - 
    
    views:
    NodeView -- represents the basic gateway to see a node.
        in its "view" function, the nodeview decides which other view to use
        for it.
        @todo: this is crucial for optimization.
    
    
    How are we realizing blogs?
        - the basic blog realized allows no comments, only to have multiple entries
        on one node.
        - it shows up, that every node has to have the option to have a default template
        basicly, the system to tell which edit/view template a user gets displayed
        has to be added.
        - we are doing this programmaticly for now.
    
    BlogEntry(NodeHtml)
        slug : parent.slug + # + id
    
    # main view for the blog:
    # - NodeHtml 'blog'
      - children: [ BlogEntry(parent=blog, ... ), ... ]
      - view cascade runs to "blogview"
      - "blogview" type iterates its children in the template
      - displays children in wanted state.
      - blogentry has an own url catcher for detailed view (read more)
    
    # i view a node:
    - nodeview gets the url
    - nodeview displays node with its respected template.
    
    lets try out if default template mechanism allows us to differentiate between
    blogentry and nodehtml per default first.
    if yes, each custom type of display could be made as its own class
    very efficient, very fast, endless pagination for importing previews for the blogs, etcetera.
    
    
    
    
    
"""
