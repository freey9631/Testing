import re, os, time

id_pattern = re.compile(r'^.\d+$') 

    # pyro client config
API_ID    = os.environ.get("API_ID", "")
API_HASH  = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")  
# database config
DB_NAME = os.environ.get("DB_NAME","Cluster0")    
DB_URL  = os.environ.get("DB_URL","")
 
    

