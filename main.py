from xmlrpc.client import FastMarshaller
from typing import Optional
from typing import Any
from collections import deque
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:
    # 先查询是否存在再存入值
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        rmap: dict[int, int] = {}
        for i, n in enumerate(nums):
            if target - n in rmap:
                return [rmap[target - n], i]
            rmap[nums[i]] = i

    # 注意语法的使用
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        rmap: dict[str, list[str]] = {}
        for s in strs:
            rmap.setdefault("".join(sorted(s)), []).append(s)
        return list(rmap.values())

    # 只知道单个队列队列初始节点即可，使用其 head - 1 判断是否在头部
    # 长度可以当增加的长度和最大值两个值的功能，由于单执行语句while可以当if来使用
    def longestConsecutive(self, nums: list[int]) -> int:
        nums = set(nums)
        rmax = 0
        for n in nums:
            if n - 1 in nums:
                continue
            length = 1
            while n + length in nums:
                length += 1
            rmax = max(rmax, length)
        return rmax

    # 快慢指针，慢指针为迭代i - 0的个数,一直迭代到第一个0的位置
    def moveZeroes(self, nums: list[int]) -> None:
        slow = 0
        for fast, n in enumerate(nums):
            if n != 0:
                nums[slow] = n
                slow += 1
        for i in range(slow, len(nums)):
            nums[i] = 0
        return nums

    # 从宽到窄，矮的一侧要继续往里移动，新的一根只有比之前一对都高才有可能变宽，这里为了简便一次只移动一次导致多算了几次面积
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        area = 0
        while left < right:
            area = max((right - left) * min(height[left], height[right]), area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return area

    # 先排序，从左到右是i，每个i都有left和right向中间靠近，小了放大，大了放小, 注意重复使用while去重
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        res: list[list[int]] = []
        nums.sort()
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left = i + 1
            right = len(nums) - 1
            while left < right:
                if nums[i] + nums[left] + nums[right] == 0:
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif nums[i] + nums[left] + nums[right] > 0:
                    right -= 1
                else:
                    left += 1

        return res

    # 接雨水，单调栈，维护一个递减的单调栈，弹出的值可以正好形成凹槽，while每次前面比现在矮小弹出一次
    # 还有俩做法
    def trap(self, height: list[int]) -> int:
        s = [0]
        res = 0
        for i, n in enumerate(height):
            while s and n > height[s[-1]]:
                mid = s.pop()
                if s:
                    w = i - s[-1] - 1
                    h = min(height[s[-1]], n) - height[mid]
                    res += w * h
            s.append(i)
        return res

    # 无重复字符的最长子串，用set来去重，慢指针一直清除到集合没有自己位置,别忘了加入自己
    def lengthOfLongestSubstring(self, s: str) -> int:
        tset = set()
        maxlen, slow = 0, 0
        for i in range(len(s)):
            while s[i] in tset:
                tset.remove(s[slow])
                slow += 1
            tset.add(s[i])
            maxlen = max(maxlen, i - slow + 1)
        return maxlen

    # s在窗口当中的的切片作为set和目标set比较，窗口大小始终为len(p),移动时收入和抛弃窗口当中的内容
    def findAnagrams(self, s: str, p: str) -> list[int]:
        n, m = len(s), len(p)
        res = []
        if m > n:
            return []
        target = [0] * 26
        window = [0] * 26
        for c in p:
            target[ord(c) - ord("a")] += 1
        for i, ch in enumerate(s):
            window[ord(ch) - ord("a")] += 1
            if i - m >= 0:
                window[ord(s[i - m]) - ord("a")] -= 1
            if window == target:
                res.append(i - m + 1)

        return res

    # 和为k的子数组
    # 注意这个题目要是连续的序列，使用前缀和的形式解出，两个前缀和的差是任意的子串
    def subarraySum(self, nums: list[int], k: int) -> int:
        mp = {0: 1}
        res = cur = 0
        for n in nums:
            cur += n
            res += mp.get(cur - k, 0)
            mp[cur] = mp.get(cur, 0) + 1
        return res

    # 滑动窗口最大值
    # 先检查左边的值有没有出界
    # while弹出比入栈的值小的值来维护单调队列
    # 窗口满了以后才开始计入结果
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq: deque[int] = deque()
        res: list[int] = []
        for i in range(len(nums)):
            while dq and dq[0] < i - k + 1:
                dq.popleft()
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()
            dq.append(i)
            if i >= k - 1:
                res.append(nums[dq[0]])
        return res

    # 最小覆盖子串，使用数组接受，注意使用count表示需求的总数，需求数达到后左移
    # 需求只有当缺少这个数而且得到的才行
    # 这里的兜底必须写的不然会出问题
    # 不需要的数字的值恒为负数
    # 先右后左，count够了停下,当扔出左边界数字时记录最小值
    def minWindow(self, s: str, t: str) -> str:
        target = [0] * 256
        count = len(t)
        left = start = right = 0
        min_len = len(s) + 1
        for c in t:
            target[ord(c)] += 1
        while right < len(s):
            if target[ord(s[right])] > 0:
                count -= 1
            target[ord(s[right])] -= 1
            right += 1

            while count == 0:
                if right - left < min_len:
                    min_len = right - left
                    start = left
                target[ord(s[left])] += 1
                if target[ord(s[left])] > 0:
                    count += 1
                left += 1

        return s[start : start + min_len] if min_len <= len(s) else ""

    # 依旧前缀和，每次循环取最大最小值，做差即可
    def maxSubArray(self, nums: list[int]) -> int:
        max_num = nums[0]
        pr = [nums[0]] * len(nums)
        min_n = min(0, nums[0])  # 前缀和最小值的初值，0 代表空前缀
        for i, n in enumerate(nums[1:], 1):
            pr[i] = pr[i - 1] + n
            max_num = max(pr[i] - min_n, max_num)
            min_n = min(min_n, pr[i])
        return max_num

    # 先排序，每次合并只找右边界即可
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort()
        res = []
        i = 0
        while i < len(intervals):
            l = 1
            max_right = intervals[i][1]
            while i + l < len(intervals) and max_right >= intervals[i + l][0]:
                l += 1
                max_right = max(max_right, intervals[i + l - 1][1])
            res.append([intervals[i][0], max_right])
            i += l
        return res

    # 死记硬背，全部翻转，k翻转，剩下的翻转
    def rotate(self, nums: list[int], k: int) -> None:

        def reverse_range(nums: list, l: int, r: int) -> None:
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l, r = l + 1, r - 1

        n = len(nums)
        k %= n
        reverse_range(nums, 0, n - 1)   # 整段翻
        reverse_range(nums, 0, k - 1)   # 前 k 个翻回来
        reverse_range(nums, k, n - 1)  # 后 n-k 个翻回来

    # 原是仨队列，前缀队列后缀队列，结果队列，但是可以统一放到结果队列里面，算一个O(1)的空间复杂度
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        head = 1
        tail = 1
        res: list[int] = [1] * len(nums)
        for i in range(len(nums) - 1):
            head: int = nums[i] * head
            tail: int = nums[len(nums) - 1 - i] * tail
            res[i + 1] = res[i + 1] * head
            res[len(nums) - 2 - i] = res[len(nums) - 2 - i] * tail

        return res

    # 答案不可能超出s的长度，因此结果在1-n当中，为了不引入额外的空间使用正负号原地标记
    def firstMissingPositive1(self, nums: list[int]) -> int:
        n: int = len(nums)
        # 负数转换为无效的数字
        for i in range(n):
            if nums[i] <= 0:
                nums[i] = n + 1

        # 将出现过的数字n对应的index_n-1标记为负数
        for num in nums:
            if 1 <= abs(num) <= n:
                nums[abs(num) - 1] = -abs(nums[abs(num) - 1])


        # 遍历index找到最小非负index
        for i in range(n):
            if nums[i] > 0:
                return i + 1

        return n + 1

    # 思路本质相同，但是节省空间使用位置移动的方式
    def firstMissingPositive2(self, nums: list[int]) -> int:
        n: int = len(nums)
        # 负数转换为无效的数字
        for i in range(n):
            while(1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]):
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]

        # 遍历index找到数字没对应好的
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        return n + 1
    # 将矩阵的首行和首列置0作为标记即可，注意标记过后直接遍历修改非首行内容防止污染标记，标记位最后处理
    def setZeroes(self, matrix: list[list[int]]) -> None:

        row_zero = False
        col_zero = False

        #特殊处理首行的0是否存在进行标记
        for j in range(len(matrix[0])):
            if matrix[0][j] == 0:
                row_zero = True
                break

        # 特殊处理首列的0是否存在进行标记
        for i in range(len(matrix)):
            if matrix[i][0] == 0:
                col_zero = True
                break

        #第一步找到0的位置
        for i in range(1,len(matrix)):
            for j in range(1,len(matrix[0])):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # 第一步找到0的位置
        for i in range(1, len(matrix)):
            for j in range(1, len(matrix[0])):
                if matrix[0][j] == 0 or matrix[i][0] == 0:
                    matrix[i][j] = 0

        if row_zero:
            for j in range(len(matrix[0])):
                matrix[0][j] = 0

        if col_zero:
            for i in range(len(matrix)):
                matrix[i][0] = 0

    # 按照圈来计数，没一圈矩阵的行和宽-2，起始点行列+1，边界条件复杂需要注意
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        r: list[int] = []
        m, n = len(matrix), len(matrix[0])
        round = 0

        while round < min(m, n) / 2:
            for j in range(round, n - round):
                r.append(matrix[round][j])

            for i in range(round + 1, m - round):
                r.append(matrix[i][n - round - 1])

            if m - 2 * round > 1:
                for j in range(n - round - 2, round - 1, -1):
                    r.append(matrix[m - round - 1][j])

            if n - 2 * round > 1:
                for i in range(m - round - 2, round, -1):
                    r.append(matrix[i][round])

            round += 1
    # 先转置后翻转
    def rotate(self, matrix: list[list[int]]) -> None:
        # 转置
        for i in range(len(matrix)):
            for j in range(i,len(matrix[0])):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for m in matrix:
            m.reverse()

    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        i = 0
        j = len(matrix[0]) - 1
        while True:

            n = matrix[i][j]
            if n == target:
                return True
            elif n < target:
                i += 1
            else:
                j -= 1
            if i >= len(matrix) or j < 0:return False
    #路径和加起来是相同的 A + C + B = B + C + A 其中A为A链表，B为B链表，C为公共剩余部分
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        p = headA
        q = headB
        while p is not q:
            p = p.next if p is not None else headB
            q = q.next if q is not None else headA

        return p
    #翻转链表，三个指针，4个步骤，先标记将丢失的指针(1)后直接改链(1)并转移(2)
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        return prev
    #细节很麻烦，思路很简单就是快指针走两步慢指针走一半，慢指针边走边翻转，最后慢指针和prev便利比对
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        prev = None
        while fast and fast.next:
            fast = fast.next.next

            nxt = slow.nexthello
            slow.next = prev
            prev = slow
            slow = nxt

        if fast:
            slow = slow.next

        while prev and slow:
            if prev.val != slow.val:
                return False
            prev = prev.next
            slow = slow.next

        return True
    # 快指针不为空一直跑就行，相遇判断为环
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast = slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                return True
        return False

    # 因为在慢指针超越1圈前快指针走完两圈，因此慢指针不可能走完一圈，剩余路程到到环入口是初始节点到环入口差几圈，该圈数等于快指针走的圈数
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                fast = head
                while fast != slow:
                    fast = fast.next
                    slow = slow.next
                return slow
        return None

    # 标准的merge非常简单
    def mergeTwoLists(self, list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
        head = ListNode()
        p = head
        while list1 and list2:
            if list1.val < list2.val:
                p.next = list1
                list1 = list1.next
            else:
                p.next = list2
                list2 = list2.next
            p = p.next
        p.next = list1 if list1 else list2
        return head.next

    # 两数相加，留个进位一起判0循环加就完了
    def addTwoNumbers(self, l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
        carry = 0
        p = head = ListNode()
        while l1 or l2 or carry:
            s = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
            carry, d = divmod(s, 10)
            p.next = ListNode(d)
            p = p.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return head.next

    #来个先走几步的节点就行，依旧水题，可能删掉头结点加个yum
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        fast = slow = yum = ListNode()
        yum.next = head
        while n:
            n -= 1
            fast = fast.next
        while fast.next:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return yum.next
    # 两个一组翻转链表
    def swapPairs(self, head: ListNode | None) -> ListNode | None:
        p = yum = ListNode()
        yum.next = head
        while p.next and p.next.next:
            end = p.next.next
            p.next.next = end.next
            end.next = p.next
            p.next = end
            p = p.next.next
        return yum.next
    # 比较麻烦一步一步画图分析需要，先让一个指针跑n步(和删除类似)，然后将中间的链表翻转，随后跳转到之前标记的新的开头，这里就是之前开头的第二个节点
    def reverseKGroup(self, head: ListNode | None, k: int) -> ListNode | None:
        begin = end = yum = ListNode()
        yum.next = head
        for _ in range(k):
            end = end.next if end else None
        while end:
            next_begin = p = begin.next
            begin.next = end
            mid = p.next
            p.next = end.next
            while p != end:
                nxt = mid.next
                mid.next = p
                p = mid
                mid = nxt
            end = begin = next_begin
            for _ in range(k):
                end = end.next if end else None

        return yum.next

    # 深拷贝并维护关系，现实最优解是借助hash表，但是演示要求通过临时修改原链表完成，遍历三遍链表，第一遍复制第二遍改随机引用第三遍拆分
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None
        # 第一次遍历，复制一份
        p = head
        while p:
            nxt = p.next
            p.next = Node(p.val)
            p.next.next = nxt
            p = nxt

        # 标记开头
        res = head.next

        # 第二次遍历，注意处理随机关系
        p = head
        while p:
            p.next.random = p.random.next if p.random else None
            p = p.next.next

        p = head
        while p.next:
            nxt = p.next
            p.next = p.next.next if p.next else None
            p = nxt

        return res
