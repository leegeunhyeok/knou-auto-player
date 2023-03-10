from datetime import datetime

def string_to_second(time_string: str):
   if time_string.count(':') == 1:
      time_string = f'00:{time_string}'
   time_delta = datetime.strptime(time_string, "%H:%M:%S") - datetime(1900,1,1)
   return time_delta.total_seconds()
