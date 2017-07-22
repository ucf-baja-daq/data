# import libraries
import threading
import time

# flag to exit the program
exitFlag = 0


class myThread (threading.Thread):
	# initiate myThread object
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    # threading run command    
    def run(self):
		# report threads starting
        print("Starting " + self.name)
        
        # run sample code to demonstrate both threads running simultaneously
        print_time(self.name, self.counter, 5)
        
        print("Exiting " + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        #print(str(threading.current_thread())) #printes current thread info
        print("%s: %s" % (threadName, time.ctime(time.time())))
        
        time.sleep(delay)
        counter -= 1

print(str(threading.current_thread()))

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")
