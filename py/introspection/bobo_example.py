import bobo

@bobo.query('/')
def hello(person):
    return f'Hello {person}'
