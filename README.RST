gogo
====

toolkit for grpcio dev.

grpcio start a server with threading pool type.

so even though grpc is write in c, and the serve and complete_queue is in 
`nogil`, the server side handlers can only run one by one at a time.



all in draft....

