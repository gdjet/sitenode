
from django import template
from ..models import Node

register = template.Library()

class SiteNodeNode(template.Node):

    def __init__(self, slug, as_var=None):
        self.slug = template.Variable(slug)
        self.as_var = as_var

    def render(self, context):
        try:
            node = Node.objects.get(slug=self.slug)
        except:
            return ''
        node = node.as_leaf()
        if self.as_var:
            context[self.as_var] = node
            return ""
        return node.as_html()


@register.tag(name="include_node")
def do_include_node(parser, token):
    """
    Example usage::

        {% include_node 'slug/of/node' %}

    or if you need to use in a variable or {% blocktrans %}::

        {% include_node 'slug/of/node' as my_var %}
        {{ my_var.title }}

    """
    bits = token.split_contents()
    if len(bits) == 2:
        slug = bits[1]
        as_var = None
    elif len(bits) == 4:
        slug = bits[1]
        as_var = bits[3]
    else:
        raise template.TemplateSyntaxError("'%s' takes either two or four arguments" % bits[0])

    return SiteNodeNode(slug, as_var)
