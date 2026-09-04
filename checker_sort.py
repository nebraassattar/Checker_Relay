"""
Checker Sort
============

Given a row of 2n checkers -- n red (0) followed by n black (1) -- transform
it into an alternating row [0, 1, 0, 1, ..., 0, 1] using only swaps of
adjacent checkers.

Two equivalent implementations are provided:

  transform_checkers(n)             -- recursive
  transform_checkers_iterative(n)   -- iterative

Both perform the same n(n-1)/2 swaps, in the same order, and both are
swap-optimal: n(n-1)/2 is exactly the number of red/black pairs that start
out of order, and one adjacent swap can fix at most one such pair, so no
sequence of adjacent swaps can do it in fewer moves.

Complexity (both versions):
    Time:  O(n^2)  -- n(n-1)/2 swaps, each O(1) to perform
    Space: O(n^2)  -- the swaps list records every swap

The recursive version additionally uses O(n) call-stack space (one frame
per layer of recursion), which the iterative version avoids -- see the
docstrings below for details.
"""


def transform_checkers(n):
    """
    Recursive version.

    Turns [0]*n + [1]*n into [0,1,0,1,...,0,1] using only
    adjacent swaps, via recursion.

    Returns:
        swaps  -- list of (left, right) index pairs, in the order they
                  were applied
        arr    -- the final (alternating) array
    """
    arr = [0] * n + [1] * n
    swaps = []

    def solve(n_pairs, offset):
        # Base case: subarray of size 0 needs no work.
        if n_pairs <= 0:
            return

        # Invariant: arr[offset : offset + 2*n_pairs] == [0]*n_pairs + [1]*n_pairs
        # Walk the checker at (offset + n_pairs) -- the first black one --
        # left, one adjacent swap at a time, until it reaches (offset + 1).
        for i in range(n_pairs - 1, 0, -1):
            left, right = offset + i, offset + i + 1
            arr[left], arr[right] = arr[right], arr[left]
            swaps.append((left, right))

        # Now arr[offset] == 0 and arr[offset+1] == 1 are permanently correct.
        # Recurse on the inner subarray, which has the identical shape.
        solve(n_pairs - 1, offset + 2)

    solve(n, 0)
    return swaps, arr


def transform_checkers_iterative(n):
    """
    Iterative version -- same result and same swap order as
    transform_checkers, but with an explicit loop instead of recursion.

    Recursion depth in the recursive version grows with n (one stack
    frame per layer), so it will hit Python's default recursion limit
    (~1000) somewhere around n ~ 990-1000. This version uses O(1)
    auxiliary space beyond the arr/swaps lists, so it scales to any n.

    Returns:
        swaps -- list of (left, right) index pairs, in the order they
                 were applied
        arr   -- the final (alternating) array
    """
    arr = [0] * n + [1] * n
    swaps = []
    offset = 0

    # Each pass through this loop does the work of one recursive call:
    # walk the first black checker in the current slice home, then
    # shrink the slice by moving offset two slots to the right.
    for n_pairs in range(n, 0, -1):
        for i in range(n_pairs - 1, 0, -1):
            left, right = offset + i, offset + i + 1
            arr[left], arr[right] = arr[right], arr[left]
            swaps.append((left, right))
        offset += 2

    return swaps, arr


def main():
    while True:
        try:
            n = int(input("Enter n (number of red/black pairs): "))
            if n < 1:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("That's not a valid integer, try again.")

    target = [0, 1] * n
    print("\nstart :", [0] * n + [1] * n)

    if n == 1:
        print("Already alternating -- no swaps needed.")
        print("final :", [0, 1])
        return

    swaps, final = transform_checkers(n)

    working = [0] * n + [1] * n
    for i, j in swaps:
        working[i], working[j] = working[j], working[i]
        print(f"swap({i},{j}) -> {working}")

    assert working == target == final
    print("\ntarget:", target)
    print(f"n={n}: used {len(swaps)} swaps "
          f"(theoretical minimum = n(n-1)/2 = {n * (n - 1) // 2})")

    # Sanity check: the iterative version should produce the exact same
    # swap sequence and final array.
    swaps_iter, final_iter = transform_checkers_iterative(n)
    assert swaps_iter == swaps and final_iter == final
    print("iterative version verified: identical swaps and final array.")


if __name__ == "__main__":
    main()
