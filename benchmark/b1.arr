#|
    Problem 1: my-len: Length of the list
|#

fun my-len(l):
  cases (List) l:
    | empty      => 0
    | link(f, r) => 1 + my-len(r)
  end
where:
    my-len([list: 7, 8, 9]) is 1 + 2
    my-len([list:    8, 9]) is 1 + 1
    my-len([list:       9]) is 1 + 0
    my-len([list:        ]) is     0
end