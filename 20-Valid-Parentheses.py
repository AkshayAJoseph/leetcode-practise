
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        brackets = {')': '(', '}': '{', ']': '['}

        for i in s:
            if i in brackets.values():
                stack.append(i)
            elif i in brackets:
                if not stack:
                    return False

                if stack.pop() != brackets[i]:
                    return False

        return not stack
