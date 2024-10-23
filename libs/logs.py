import datetime as dt


def l(key, text, tag=None, date_tag=True):
    log_filename = "logs/"+ key+f"_{dt.date.today()}" + ".txt"
    with open(log_filename,"a") as log:
        log.write(f"\n{dt.datetime.now()}: {tag} - {text}\n")

def log_conversation(text:str, tag=None):
    l("conversation", text, tag)

def log_error(text:str, tag=None):
    l("error", text, tag)

def log_response(text:str, tag=None):
    l("response", text, tag)

def log_trace(text:str, tag=None):
    l("trace", text, tag)

def log_info(text:str, tag=None):
    l("info", text, tag)





if __name__ == "__main__":
    l("test", "This is a test log", tag="INFO")
