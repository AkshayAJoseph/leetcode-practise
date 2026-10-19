# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: ListNode | None, left: int, right: int) -> ListNode | None:
        if left == right:
            return head
        dummy = ListNode(0, head)
        prev = dummy

        for _ in range(left - 1):
            prev = prev.next
        
        curr = prev.next

        for _ in range(right - left):
            nextnode = curr.next
            curr.next = nextnode.next
            nextnode.next = prev.next
            prev.next = nextnode

        return dummy.next