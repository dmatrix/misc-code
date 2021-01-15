#
# Function to demonstrate various argument types
# to a function: positional, variable, and keyword-named.

def tag(name, *content, cls=None, **attrs):
    """Generate one or more HTML Tags. This function could be used for other purposes too"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                           for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                         (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


def f(a, *, b):
    """
    :param a: regular argument
    :param b: keyword-only argument
    :return: tuple of arugments
    """

    return a, b


if __name__ == '__main__':
    print(tag('br'))
    print(tag('p', 'hello'))
    print(tag('p', 'hello', 'world'))
    print(tag('p', 'hello', 'world', cls='sidebar'))
    print(tag(content='testing', name='img'))
    my_tags = {'name':'img',
              'title':'Sunset Boulevard',
              'src':'sunset.jpg',
              'cls':'framed'
              }
    print(tag(**my_tags))
    print("=" * 80)
    print(f(1, b=2))
    print(f(3, b=5))
    print(f(0, b=5))

