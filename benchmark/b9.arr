#|
    Problem 9: my-running-sum: Given a list of numbers, return a list showing with running sum
|#

fun my-running-sum(l, cursum):
	cases (List) l:
		| empty => empty
    | link(f, r) => link(f + cursum, my-running-sum(r, (f + cursum)))
	end
where:
  my-running-sum([list: 1, 2, 3, 4, 5], 0) is [list: 1, 3, 6, 10, 15]
  my-running-sum([list: 1, 2, 3], 0) is [list: 1, 3, 6]
  my-running-sum([list: ], 0) is [list: ]
end