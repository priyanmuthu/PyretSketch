fun my-double(l):
	cases (List) l:
    | empty => empty
    | link(f, r) => 
        link(f * 2, my-double(r))
	end
where:
    my-double([list: 1,2]) is [list:2,4]
    my-double([list: 3,-2,-4,7]) is [list: 6, -4, -8, 14]
    my-double([list: 0]) is [list:0]
    my-double([list: ]) is [list: ]
end