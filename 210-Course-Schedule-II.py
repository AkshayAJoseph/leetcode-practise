class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        graph = {i: [] for i in range(numCourses)}

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
        
        result = []
        state = [0] * numCourses
        # 0- unvisited, 1-visiting, 2-visited
        def dfs(course):
            if state[course] == 1:
                return False
            if state[course] == 2:
                return True

            state[course] = 1
            for neighbor in graph[course]:
                if not dfs(neighbor):
                    return False
            
            state[course] = 2
            result.append(course)
            return True
        
        for course in range(numCourses):
            if not dfs(course):
                return []
            
        return result[::-1]