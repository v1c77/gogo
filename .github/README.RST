gogo
====

.. image:: https://travis-ci.com/v1c77/gogo.svg?branch=master
   :target: https://travis-ci.org/v1c77/gogo

.. image:: https://codecov.io/gh/v1c77/gogo/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/v1c77/gogo

The toolkit for grpcio dev.



**For development:**

.. code-block:: bash

    git clone git@github.com/v1c77/gogo.git
    cd gogo
    pip install --editable ./



**all in draft....**

grpcio start a server with threading pool type.

so even though grpc is write in c, and the serve and complete_queue is in
`nogil`, the server side handlers can only run one by one at a time.


License
--------
WTFPL_ .

.. _WTFPL: http://www.wtfpl.net/
