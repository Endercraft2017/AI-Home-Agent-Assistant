import time

from tools.reminder import run
from agent.sqlite_helper import init_db

def test_db_builder():
    Test1 = {    
        "Content": "Kyle Birthday",
        "Date": "04-02:-2001", 
        "Action": "set"}
    Test2 = {    
        "Content": "Kurt Birthday",
        "Date": "25-02-2005", 
        "Action": "set"}
    Test3 = {    
        "Content": "Go to the doctor for an appointment",
        "Date": "05-07-2025", 
        "Action": "set"}
    Test4 = {    
        "Content": "Feed the dogs",
        "Date": "03-07-2025", 
        "Action": "set"}
    run(Test1)
    run(Test2)
    run(Test3)
    run(Test4)

TOOL_SCHEMA = {
    "Content": "Anything to do with my pet",
    "Date": "", ##DD-MM-YYYY
    "Time": "", ##HH:MM
    "Unspecified_time": "",
    "Action": "get"
}
init_db()
start = time.time()
#test_db_builder()
print (run(TOOL_SCHEMA))
end = time.time()
print(f"Elapsed time: {end - start:.2f} seconds")
