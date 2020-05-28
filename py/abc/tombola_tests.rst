==============
Tombola tests
==============

Every concrete sublcass of Tombola should pass these tests:

Create and load instance from iterable::

>>> balls = list(range(3))
>>> globe = ConcreteTombola(balls)
>>> globe.loaded()
True
>>> globe.inspect()
(0, 1, 2)

Pick and collect balls::

>>> picks = []
>>> picks.append(globe.pick())
>>> picks.append(globe.pick())
>>> picks.append(globe.pick())

Check state and results::

>>> globe.loaded()
False
>>> sorted(picks) == balls
True

Reloaded::

>>> globe.load(balls)
>>> globe.loaded()
True
>>> picks = [globe.pick() for i in balls]
>>> globe.loaded()
False

Check that `LookupError` (or a sublclass) is the exception
thrown when the device is empty::

>>> globe = ConcreteTombola([])
>>> try:
...   globe.pick()
... except LookupError as exc:
...   print('OK')
OK

Load and pick 100 balls to verify that they all come out::

>>> balls = list(range(100))
>>> globe = ConcreteTombola(balls)
>>> picks = []
>>> while globe.inspect():
...   picks.append(globe.pick())
>>> len(picks) == len(balls)
True
>>> set(picks) == set(balls)
True

Check that the order has changed and it's not simply revesed::

>>> picks != balls
True
>>> picks[::-1] != balls
True

THE END
