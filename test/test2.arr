fun sum(l):
  cases (List) l:
    | empty => 0
    | link(first, rest) => cases (List) rest:
        | empty => first
        | link(second, second_rest) => sum(second_rest) + first
      end
  end
where:
  sum([list: ]) is 0
  sum([list: 1]) is 1
  sum([list: 1, 2]) is 1
  sum([list: 1, 2, 3]) is 4
  sum([list: 1, 2, 3, 4]) is 4
end