#|
    Problem 4: my-str-len: Given a list of numbers, generate a list of its positive numbers.
|#

fun my-str-len(l):
  cases (List) l:
    | empty      => empty
    | link(f, r) => link(string-length(f), my-str-len(r))
  end
where:
    my-str-len([list: "hello", "world", "here", "are", "examples"]) is [list: 5, 5, 4, 3, 8]
    my-str-len([list: "world", "here", "are", "examples"]) is [list: 5, 4, 3, 8]
    my-str-len([list: "here", "are", "examples"]) is [list: 4, 3, 8]
    my-str-len([list: "are", "examples"]) is [list: 3, 8]
    my-str-len([list: "examples"]) is [list: 8]
    my-str-len([list: ]) is [list: ]
end