fun my-count-occurrence(l):
	cases (List) l:
		| empty      => 0
		| link(f, r) => 
      if f == 0:
				1 + my-count-occurrence(r)
			else:
				my-count-occurrence(r)
			end
	end
where:
	my-count-occurrence([list: 0,0,0,4]) is 3
	my-count-occurrence([list: 0,0,2,1]) is 2
	my-count-occurrence([list: 5,0,0,5,0,1,0,2]) is 4
	my-count-occurrence([list: ]) is 0
end