#|
    Problem 2: my-sum: Sum of all the elements in the list
|#

fun my-sum(l):
  cases (List) l:
    | empty      => 0
    | link(f, r) => f + my-sum(r)
  end
where:
    my-sum([list: 7, 8, 9]) is 7 + 8 + 9
    my-sum([list:    8, 9]) is     8 + 9
    my-sum([list:       9]) is         9
end