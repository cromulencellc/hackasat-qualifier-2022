import jinja2
import datetime 
class CesiumOrbitTemplate:
    def __init__(self):
        self.time_format = "%Y-%m-%dT%H:%M:%SZ"
        pass
    def set_orbit( self , dataArray, decimation=1 ):
        self.orbit = []
        count = 0
        for item in dataArray:
            count = count+1
            entry = dict()
            entry["X"] = item["X"]*1000
            entry["Y"] = item["Y"]*1000
            entry["Z"] = item["Z"]*1000
            entry["time"] = item["time"].strftime( self.time_format )
            if(  (count  % decimation ) == 0 ):
                self.orbit.append(entry)
        pass
    def set_window( self ,startTime , stopTime):
        #"2014-07-22T11:29:11Z"
        
        self.start = startTime.strftime(self.time_format)
        self.stop = stopTime.strftime(self.time_format)
    def render( self  , template_directory, template_filename , out_path , name ):
        templateLoader = jinja2.FileSystemLoader(searchpath= template_directory )
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(template_filename)
        out_text = template.render( start_time=self.start, stop_time = self.stop , orbit=self.orbit , name=name)  
        new_file = open( out_path , "wt")
        new_file.write( out_text )
        new_file.close()