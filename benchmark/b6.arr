#|
    Problem 6: my-alternating: Given a list of numbers, generate a list of alternating numbers
|#

fun my-alternating(l):
    cases (List) l:
      | empty       => empty
      | link(f, r1) => 
      cases (List) r1:
        | empty       => [list: f]
        | link(s, r2) => link(f, my-alternating(r2))
       end
    end
where:
    my-alternating([list: 1, 2, 3, 4, 5, 6]) is [list: 1, 3, 5]
    my-alternating([list:    2, 3, 4, 5, 6]) is [list: 2, 4, 6]
    my-alternating([list:       3, 4, 5, 6]) is [list:    3, 5]
    my-alternating([list:          4, 5, 6]) is [list:    4, 6]
end