#|
    Problem: my-neg-sum: Given a list of numbers, calculate the sum of all the negative numbers
|#

fun my-neg-sum(l):

where:
    my-neg-sum([list: 1, -2, 3, -4]) is -6
    my-neg-sum([list:    -2, 3, -4]) is -6
    my-neg-sum([list:        3, -4]) is -4
    my-neg-sum([list:           -4]) is -4
    my-neg-sum([list:             ]) is 0
end