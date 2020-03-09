#|
    Problem 8: my-reverse-list: Given a list of numbers, reverse it
|#

fun my-reverse-list(l, out):
  cases (List) l:
    | empty => out
    | link(f, r1) => my-reverse-list(r1, link(f, out))
  end
where:
  my-reverse-list([list: 1, 2, 3, 4, 5], empty) is [list: 5, 4, 3, 2, 1]
  my-reverse-list([list: 1, 2, 3], empty) is [list: 3, 2, 1]
  my-reverse-list([list: ], empty) is [list: ]
end