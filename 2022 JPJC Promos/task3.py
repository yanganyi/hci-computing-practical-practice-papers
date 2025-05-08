# Task 3.1

class COEBid:
    def __init__(self, cust_id: str, reserve_price: int):
        self.cust_id = cust_id
        self.reserve_price = reserve_price
        self.status = "Bidding in progress"

    def get_cust_id(self) -> str:
        return self.cust_id

    def get_reserve_price(self) -> int:
        return self.reserve_price

    def get_status(self) -> str:
        return self.status

    def set_status(self, s: str):
        self.status = s

    def display(self):
        print(f"{self.cust_id}, ${self.reserve_price}, {self.status}")



# Task 3.2

class Node:
    def __init__(self, data: COEBid):
        self.data = data
        self.next = None

class COELinkedList:
    def __init__(self):
        self.head = None

    def insert_bid(self, data: COEBid):
        new_node = Node(data)

        if self.head is None or new_node.data.get_reserve_price() > self.head.data.get_reserve_price():
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.data.get_reserve_price() > new_node.data.get_reserve_price():
                current = current.next
            
            new_node.next = current.next
            current.next = new_node

    def display_list(self):
        if self.head is None:
            print("No bids in the list.")
            return
        
        current = self.head
        while current is not None:
            current.data.display()
            current = current.next

    # Task 3.3
    
    def calculate_COEPrice(self, quota: int) -> int:
        if self.head is None:
            return 0 

        first_unsuccessful_node = self.head
        for _ in range(quota):
            if first_unsuccessful_node is None:
                return 0
            first_unsuccessful_node = first_unsuccessful_node.next
        
        if first_unsuccessful_node is None:
            return 0
            
        return first_unsuccessful_node.data.get_reserve_price() + 1

    def update_status(self, quota: int):
        current = self.head
        count = 0
        while current is not None:
            if count < quota:
                current.data.set_status("Successful")
            else:
                current.data.set_status("Unsuccessful")
            current = current.next
            count += 1



# # === TEST SECTION ===
# bid1 = COEBid("T00X", 50)
# bid1.display()
# bid1.set_status("Successful")
# bid1.display()

# print("=== Task 3.2 ===")
# coe_LL = COELinkedList()

# bids_data = [
#     ("T001", 41),
#     ("T002", 88),
#     ("T003", 67),
#     ("T004", 70),
#     ("T005", 100)
# ]

# for cust_id, reserve_price in bids_data:
#     bid = COEBid(cust_id, reserve_price)
#     coe_LL.insert_bid(bid)
#     print(f"Inserted: {cust_id}, ${reserve_price}")

# coe_LL.display_list()
# print("=" * 30)

# # === TASK 3.3 ===
# print("\n=== Task 3.3 ===")
# coe_LL_task3_3 = COELinkedList()

# bids_for_task3_3 = [
#     COEBid("B001", 100),
#     COEBid("B002", 88),
#     COEBid("B003", 70),
#     COEBid("B004", 67),
#     COEBid("B005", 41)
# ]

# for bid_obj in bids_for_task3_3:
#     coe_LL_task3_3.insert_bid(bid_obj)
#     bid_obj.display()
# print("\n")
# coe_LL_task3_3.display_list()

# quota = 3
# coe_price = coe_LL_task3_3.calculate_COEPrice(quota)
# print(f"\nprice is ${coe_price}") # Expected: $68 (67+1)

# coe_LL_task3_3.update_status(quota)
# coe_LL_task3_3.display_list()
# # Expected output:
# # B001, $100, Successful
# # B002, $88, Successful
# # B003, $70, Successful
# # B004, $67, Unsuccessful
# # B005, $41, Unsuccessful