fun my-count-occurrence(a):
	cases (List) a:
		| empty =>
			0
		| link(head, tail) =>
			if head > 0:
				my-count-occurrence(tail)
			else:
				head + (my-count-occurrence(tail) + 1)
			end
	end
where:
	my-count-occurrence([list: 0,0,0,4]) is 3
	my-count-occurrence([list: 0,2,0,1]) is 2
	my-count-occurrence([list: ]) is 0
end