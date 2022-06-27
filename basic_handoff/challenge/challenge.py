import os
import values
from timeout import timeout,TimeoutError
import webinterface
import threading
to = int( os.getenv("TIMEOUT",120))

@timeout(to)

def challenge():
    web = threading.Thread(target=webinterface.run_web )
    web.setDaemon(True)
    web.start()


    service_host = os.getenv("SERVICE_HOST")
    service_port = os.getenv("SERVICE_PORT")
    print("Math problem available at: http://{}:{}/math".format( service_host,service_port))
    print("What is the solution to the math problem?")
    answer = int(input())
    expected = values.a+values.b
    if( answer == expected ):
        flag = os.getenv("FLAG", )
        print("Here is your flag")
        print(flag)
    else:
        print("WRONG!")

if __name__ == "__main__":
    try: 
        challenge()
    except TimeoutError:
        print("Timeout....bye")
