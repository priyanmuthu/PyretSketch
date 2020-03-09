#|
    Problem 7: my-count-occurrence: Given a list of numbers and a target, count the number of occurrences of the target
|#

fun my-count-occurrence(l, t):
	cases (List) l:
		| empty      => 0
		| link(f, r) => 
			if f == t:
				1 + my-count-occurrence(r, t)
			else:
				my-count-occurrence(r, t)
			end
	end
where:
	my-count-occurrence([list: 0,0,0,4], 0) is 3
	my-count-occurrence([list: 0,0,2,1], 0) is 2
	my-count-occurrence([list: 5,0,0,5,0,1,0,2], 0) is 4
	my-count-occurrence([list: ], 0) is 0
end