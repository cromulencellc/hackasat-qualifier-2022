
import socket
import os
import sys

class stdio_solve_helper:
    def __init__( self , host, port,prompt , solved, wrong, encoding ):
        self.challenge_info = []
        self.prompt = prompt
        self.solved = solved
        self.encoding = encoding
        self.wrong = wrong
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.complete = False
        self.tags = []
        pass
    def add_challenge_block( self , name, header ,  reset ):
        info = dict()
        info["name"] = name 
        info["header"] = header
        info["reset"] = reset 
        info["data"]= None
        info["header_loc"] =0
        self.challenge_info.append( info )
        pass
    def send_answer( self , text ):   
        print("sending text: {}".format(text) )
        self.s.send( text.encode('utf-8'))
    def reset( self ):
        for item in self.challenge_info:
            if( item["reset"] == True):
                item["data"] = None
                item["header_loc"] = 0
                
        self.tags = []
    def handle_ticket( self ):
        ticket = os.getenv("CHAL_TICKET")
        if( ticket  != None ):
            self.s.recv(1000)
            print("Sending ticket - {}".format( ticket ), flush=True)
            self.s.send( ticket.encode('utf-8'))
            self.s.send( "\n".encode('utf-8'))
            ticket_sent = True
    def get( self, key ):
        item = next(item for item in self.challenge_info if item["name"] == key ) 
        return item["data"]
    def is_complete(self):
        return self.complete
    def wait_for_single_challenge(self):
        keep_reading = True 
        challenge =""

        while( keep_reading ):
            
            data = self.s.recv(10000)
            
            chonk = data.decode("UTF-8")
            
            challenge = challenge + chonk
            # Search the total challenge statement 
            headers_found = 0 
            footers_found = 0
          
            # Search for the challenge prompt
            EOC = challenge.find(self.prompt) 
            SOLVED = challenge.find( self.solved ) 
            WRONG = challenge.find( self.wrong )
            if( EOC != -1  ):
                prompt_text = challenge[ EOC : EOC+len(self.prompt)]
                
                self.parse_challenge( challenge[0:EOC])
                print( challenge[0:EOC+len(self.prompt)])
                keep_reading = False
            if( SOLVED != -1 ):
                print("Solver succeeded!")
                solved_text = challenge[ SOLVED : ]
                print(solved_text)
                self.complete = True
                keep_reading = False
                sys.exit(0)
            if( WRONG != -1 ):
                print("Failed...solver exiting")
                sys.exit(0)
    def parse_challenge( self , text ):
        # find the header locations
        for item in self.challenge_info:
            
            H = text.find( item["header"] )
            if( (H == - 1) and (item["data"] == None) ):
                print("Challenge missing expected  key:\n {}".format(item["header"]))
                sys.exit(0)
            item["header_loc"] = H
        # Sort by header location
        sorted_list = sorted(self.challenge_info, key = lambda i: i['header_loc'])
        N = len(sorted_list)
        for idx in range( N):
            if( sorted_list[idx]["data"] == None ):
                start_idx = sorted_list[idx]["header_loc"] + len( sorted_list[idx]["header"])
                if( idx < N-1):
                    stop_idx = sorted_list[idx+1]["header_loc"]
                    sorted_list[idx]["data"] = text[ start_idx  : stop_idx]
                else:
                    sorted_list[idx]["data"] = text[ start_idx :]
        self.challenge_info = sorted_list