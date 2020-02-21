#|
    Problem 5: my-pos-nums: Given a list of numbers, generate a list of its positive numbers.
|#

fun my-pos-nums(l):
  cases (List) l:
    | empty      => empty
    | link(f, r) => 
        if f > 0:
            link(f, my-pos-nums(r))
        else:
            my-pos-nums(r)
        end
  end
where:
    my-pos-nums([list: 1, -2, 3, -4]) is [list: 1, 3]
    my-pos-nums([list:    -2, 3, -4]) is [list:    3]
    my-pos-nums([list:        3, -4]) is [list:    3]
    my-pos-nums([list:           -4]) is [list:     ]
    my-pos-nums([list:             ]) is [list:     ]
end