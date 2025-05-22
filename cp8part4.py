import uuid
import math

class Account:
    def __init__(self, name, rate):
        self.name = name
        self.balance = 0.0
        self.rate = rate / 100.0
        self.res = 0.0

    def deposit(self, amt):
        if amt > 0:
            self.balance += amt

    def withdraw(self, amt):
        if amt > 0 and self.balance >= amt:
            self.balance -= amt
            return True
        return False

    def accrue_projection(self, days):
        bal = self.balance
        rem = self.res
        for _ in range(days):
            daily = bal * (self.rate / 365) if bal > 0 else 0.0
            total = daily + rem
            cred = math.floor(total * 100) / 100
            if cred >= 0.01:
                bal += cred
                rem = total - cred
            else:
                rem = total
        return round(bal, 2), round(bal - self.balance, 2)

class BoostPocket(Account):
    base_rate = 1.68
    boost_map = {30: 0.5, 90: 0.6}

    def __init__(self, name, tenure):
        super().__init__(name, self.base_rate)
        self.tenure = tenure
        self.boost_rate = self.boost_map.get(tenure, 0.0)
        self.init_dep = 0.0

    def simulate_tenure_projection(self):
        bal = self.balance
        rem = self.res
        base_int = 0.0
        for _ in range(self.tenure):
            daily = bal * (self.rate / 365) if bal > 0 else 0.0
            total = daily + rem
            cred = math.floor(total * 100) / 100
            if cred >= 0.01:
                bal += cred
                rem = total - cred
                base_int += cred
            else:
                rem = total
        boost_int = 0.0
        if self.tenure > 0 and self.boost_rate > 0:
            raw = self.init_dep * (self.boost_rate / 100.0) * (self.tenure / 365.0)
            boost_int = math.floor(raw * 100) / 100
            bal += boost_int
        return round(bal, 2), round(base_int + boost_int, 2)

class Customer:
    def __init__(self):
        self.main = None
        self.saves = []
        self.boosts = []

cust = Customer()

def test_setup():
    global cust
    cust.main = Account("main-acc", 2.08)
    cust.main.deposit(100000)
    for i in range(3):
        a = Account(f"save-{i+1}", 2.38)
        a.deposit(100000)
        cust.saves.append(a)

    b = BoostPocket(f"boost-{i+1}", 30)
    b.deposit(100000)
    b.init_dep = 100000
    cust.boosts.append(b)

    b = BoostPocket(f"boost-{i+1}", 90)
    b.deposit(100000)
    b.init_dep = 100000
    cust.boosts.append(b)

    print("yippee lol")

test_setup()

while True:
    print("\nMenu:\nPlease select a function to perform:\n[a] Create a Main Saving Account (only 1)\n[b] Create a Saving Pocket (max 3)\n[c] Create a Boost Pocket (max 2)\n[d] Add fund to Main Account\n[e] Add fund to Saving Pocket\n[f] Add fund and select tenure to Boost Pocket\n[g] Print interest of my Boost Pocket\n[h] Print interest of my Main Account or Saving Pocket\n[i] Print all accounts\n[q] Quit")
    op = input("> ").strip().lower()

    if op == "a":
        if cust.main:
            print("Exists.")
        else:
            id = str(uuid.uuid4().int)[:10]
            cust.main = Account(id, 2.08)
            print(f"Main created: {cust.main.name}")

    elif op == "b":
        if len(cust.saves) >= 3:
            print("Max Save.")
        else:
            n = input("Name: ")
            cust.saves.append(Account(n, 2.38))
            print(f"Save '{n}' made.")

    elif op == "c":
        if len(cust.boosts) >= 2:
            print("Max Boost.")
        else:
            n = input("Name: ")
            cust.boosts.append(BoostPocket(n, 0))
            print(f"Boost '{n}' made.")

    elif op == "d":
        if not cust.main:
            print("No Main.")
        else:
            amt = float(input("Amt: "))
            if amt <= 0: print("> 0"); continue
            cust.main.deposit(amt)
            print(f"${amt:.2f} added. Bal: ${cust.main.balance:.2f}")

    elif op == "e":
        if not cust.main: print("No Main"); continue
        if not cust.saves: print("No Save"); continue
        for i, s in enumerate(cust.saves): print(f"[{i}] {s.name} (${s.balance:.2f})")
        i = int(input("Pick: "))
        if not (0 <= i < len(cust.saves)): print("Bad"); continue
        amt = float(input(f"Amt Main->{cust.saves[i].name}: "))
        if amt <= 0: print("> 0"); continue
        if cust.main.withdraw(amt):
            cust.saves[i].deposit(amt)
            print(f"${amt:.2f} OK. Main: ${cust.main.balance:.2f}, {cust.saves[i].name}: ${cust.saves[i].balance:.2f}")
        else:
            print("No $.")

    elif op == "f":
        if not cust.main: print("No Main"); continue
        if not cust.boosts: print("No Boost"); continue
        for i, b in enumerate(cust.boosts): print(f"[{i}] {b.name} (${b.balance:.2f}, {b.tenure}d)")
        i = int(input("Pick: "))
        if not (0 <= i < len(cust.boosts)): print("Bad"); continue
        m = int(input("Tenure 1/3 mo: "))
        if m not in [1, 3]: print("Bad"); continue
        days = m * 30
        amt = float(input(f"Amt Main->{cust.boosts[i].name} ({m}mo): "))
        if amt <= 0: print("> 0"); continue
        n = cust.boosts[i].name
        if cust.main.withdraw(amt):
            b = BoostPocket(n, days)
            b.deposit(amt)
            b.init_dep = amt
            cust.boosts[i] = b
            print(f"${amt:.2f} OK. Main: ${cust.main.balance:.2f}, {b.name}: ${b.balance:.2f}")
        else:
            print("No $.")

    elif op == "g":
        if not cust.boosts: print("No Boost"); continue
        for i, b in enumerate(cust.boosts): print(f"[{i}] {b.name} ({b.tenure}d)")
        i = int(input("Pick: "))
        if not (0 <= i < len(cust.boosts)): print("Bad"); continue
        b = cust.boosts[i]
        if b.tenure == 0:
            print(f"'{b.name}' has no tenure. Bal: ${b.balance:.2f}")
            continue
        final_bal, total_int = b.simulate_tenure_projection()
        print(f"{b.name} | Init: ${b.init_dep:.2f} | Interest: ${total_int:.2f} | Final: ${final_bal:.2f}")

    elif op == "h":
        lst = []
        if cust.main: lst.append(("Main", cust.main))
        for s in cust.saves: lst.append((s.name, s))
        if not lst: print("No Accs"); continue
        for i, (n, _) in enumerate(lst): print(f"[{i}] {n}")
        i = int(input("Pick: "))
        if not (0 <= i < len(lst)): print("Bad"); continue
        d = int(input("Days: "))
        if d < 0: print("Bad"); continue
        _, acc = lst[i]
        final_bal, total_int = acc.accrue_projection(d)
        print(f"{lst[i][0]} | After {d}d: ${final_bal:.2f} | Interest: ${total_int:.2f} | Now: ${acc.balance:.2f}")

    elif op == "i":
        d = int(input("Days: "))
        total = 0
        print()
        if cust.main:
            final_bal, total_int = cust.main.accrue_projection(d)
            total += final_bal
            print(f"Main {cust.main.name} | ${final_bal:.2f} | Interest: ${total_int:.2f}")
        print()
        for s in cust.saves:
            final_bal, total_int = s.accrue_projection(d)
            total += final_bal
            print(f"Save {s.name} | ${final_bal:.2f} | Interest: ${total_int:.2f}")
        print()
        for b in cust.boosts:
            print(f"Boost {b.name} | Init: ${b.init_dep:.2f} | {b.tenure}d")
            if b.tenure > 0:
                final_bal, total_int = b.simulate_tenure_projection()
                total += final_bal
                print(f"  Final: ${final_bal:.2f} | Interest: ${total_int:.2f}")
            else:
                print(f"  No tenure | Bal: ${b.balance:.2f}")
        print()
        print(f"TOTAL MONEY ${total}")

    elif op == "q":
        print("Bye")
        break

    else:
        print("bro im gonna touch u watchout")