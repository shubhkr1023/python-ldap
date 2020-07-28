class Node:
    def __init__(self,data):
        self.data=data
        self.next=None
        
class LinkedList:
    def __init__(self):
        self.head=None
        self.last_node=None
    def append(self,data):
        if self.last_node is None:
            self.head=None(data)
            self.last_node=self.head
        else:
            self.last_node.next=Node(data)
            self.last_node=self.last_node.next
            
    def printList(self):
        current=self.head
        while current:
            print(current.data,end=' ')
            current=current.next
        
def reverse_list(llist):
    before=None
    current=llist.head
    if current is None:
        return
    after=current.next
    while after:
        current.next=before
        before=current
        current=after
        after=after.next
    current.next=before
    llist.head=current

a_llist=LinkedList()
data_list=input("Enter list:").split()
for x in data_list:
     a_llist.append(int(x))
print("Reverse:")
a_llist.printList()

