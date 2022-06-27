
from gnuradio import gr


class pass_thru( gr.sync_block ):
    def __init__( self , dtype ):
        gr.sync_block.__init__(self , name="pass thru" , in_sig= [dtype], out_sig=[dtype])
    def work( self , input_items , output_items ):
        output_items[0][:] = input_items[0]
        return len( output_items[0])