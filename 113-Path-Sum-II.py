# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: TreeNode | None, targetSum: int) -> list[list[int]]:
        result = []
        path = []

        def dfs(node, csum):
            if not node:
                return
            
            path.append(node.val)
            csum += node.val
            if node.left == None and node.right == None:
                if csum == targetSum:
                    result.append(path.copy())
            else:
                dfs(node.left, csum)
                dfs(node.right, csum)
            
            path.pop()
        
        dfs(root, 0)
        return result
