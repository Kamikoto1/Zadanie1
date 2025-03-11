from typing import List


def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    if not nums:
        return 0  # Если список пустой, сумма подмассива = 0

    max_sum = float('-inf')  # Минимальное значение для хранения максимума

    # Перебираем все возможные подмассивы длиной от 1 до k
    for size in range(1, k + 1):
        for i in range(len(nums) - size + 1):
            current_sum = sum(nums[i:i + size])
            max_sum = max(max_sum, current_sum)

    return max_sum


# Примеры использования:
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(find_maximal_subarray_sum(nums, k))  # 16