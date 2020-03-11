fun my-repeat(l):
  cases (List) l:
    | empty => empty
    | link(f, r) => link(f, link(f, my-repeat(r)))
  end
where:
  my-repeat([list:]) is [list:]
  my-repeat([list: 0]) is [list: 0, 0]
  my-repeat([list:1]) is [list:1, 1]
  my-repeat([list:1,2,3]) is [list:1,1,2,2,3,3]
  my-repeat([list:-3,5,0,1,4]) is [list: -3,-3,5,5,0,0,1,1,4,4]
end
