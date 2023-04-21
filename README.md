# Producer-Consumer problem

This is a small program that solve the classic synchronization problem in operating systems. Python 3.11.1 and Tkinter was used.

How does this work? The Producer process creates an item and adds it to the shared buffer. The Consumer process takes items out of the shared buffer and “consumes” them. In this case, this problem is represented by an old Spongebob episode called "Pickles" from season 1.

How are the processes synchronized? There are two semaphores:

* producerSemaphore: This is initialized to zero since the consumer class will increment it. Thus synchronizing the processes.
* consumerSemaphore: This is initialized to zero since the producer class will increment it. Thus synchronizing the processes.