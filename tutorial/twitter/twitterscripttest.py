
def run(message):
    import os

    
    os.system(f"gnome-terminal -e 'python3 twitter/twitterScript.py {message} > twitter/output2.txt'")
    #print(f"gnome-terminal -- 'python3 twitterScript.py {message}'")