# ======================== CSV FILE: WHAT YOU HAVE TO DO ========================
# 1. In VS Code, create a NEW FILE in the SAME folder as this .py file.
# 2. Name it  exp5.csv
# 3. Copy the lines below into it (WITHOUT the '# ' at the start), save with Ctrl+S.
#
#    event_id,process_id,event_type,message_to,initial_clock
#    E1,P1,SEND,P2,0
#    E2,P2,LOCAL,-,0
#    E3,P2,RECV,P1,0
#    E4,P2,SEND,P3,0
#    E5,P3,LOCAL,-,0
#    E6,P3,RECV,P2,0
#    E7,P1,LOCAL,-,0
#    E8,P3,SEND,P1,0
#    E9,P1,RECV,P3,0
#
# RULES: event_type must be SEND, RECV or LOCAL (capitals).
#        For RECV, message_to = who SENT the message.
#        For LOCAL, put - in message_to.
#        A RECV row must come AFTER its SEND row.
#
# 4. Change DOMAIN below to your chit's domain.   5. Run:  python exp5.py
# ===============================================================================

# LAMPORT LOGICAL CLOCK - every process keeps a counter L
#   LOCAL : L = L + 1
#   SEND  : L = L + 1   (the message carries L)
#   RECV  : L = max(L, number on message) + 1

import csv

DOMAIN = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change to your chit
FILE = "exp5.csv"

clock = {}     # counter of each process, e.g. clock["P1"] = 3
msg = {}       # number on each message,  e.g. msg["P1->P2"] = 1
order = []     # every event with its L, for the final order

print("=== Lamport Clock for", DOMAIN, "===")
print()

for row in csv.DictReader(open(FILE)):
    e = row["event_id"]
    p = row["process_id"]
    kind = row["event_type"]
    other = row["message_to"]

    if p not in clock:                       # first time we see this process
        clock[p] = int(row["initial_clock"])

    old = clock[p]

    if kind == "SEND":
        clock[p] = old + 1
        msg[p + "->" + other] = clock[p]     # write L on the message
        print(e, p, "sends to", other, "  L =", clock[p])

    elif kind == "RECV":
        t = msg[other + "->" + p]            # read the number on the message
        clock[p] = max(old, t) + 1
        print(e, p, "receives from", other, "  msg =", t, "  L =", clock[p])

    else:                                    # LOCAL
        clock[p] = old + 1
        print(e, p, "local event", "  L =", clock[p])

    order.append([clock[p], p, e])

order.sort()                                 # smallest L first
print()
print("Final causal order:")
for item in order:
    print(item[2], "L =", item[0])