import time

from tools.note import run
from agent.sqlite_helper import init_db

def test_db_builder():
    Test1 = {
        "Content": "Poop when stomach hurts",
        "Action": "set"}
    Test2 = {
        "Content": "No poop no stomach aches",
        "Action": "set"}
    Test3 = {
        "Content": "No food = no poop",
        "Action": "set"}
    Test4 = {
        "Content": "Kurt",
        "Action": "set"}
    run(Test1)
    run(Test2)
    run(Test3)
    run(Test4)

TOOL_SCHEMA = {
    "Content": "note on game making",
    "Action": "delete"
}
init_db()
start = time.time()
#test_db_builder()
print (run(TOOL_SCHEMA))
end = time.time()
print(f"Elapsed time: {end - start:.2f} seconds")
