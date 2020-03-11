fun my-zeros(n):
  if n > 0:
    link(0, my-zeros(n - 1))
  else:
    empty
  end
where:
  my-zeros(0) is [list:]
  my-zeros(1) is [list: 0]
  my-zeros(2) is [list:0, 0]
  my-zeros(3) is [list: 0, 0, 0]
end