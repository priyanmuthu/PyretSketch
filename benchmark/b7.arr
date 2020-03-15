fun my-countdown(n):
    if n >= 0:
        link(n, my-countdown(n - 1))
    else:
        empty
    end
where:
    my-countdown(0) is [list: 0]
    my-countdown(1) is [list: 1, 0]
    my-countdown(2) is [list: 2,1, 0]
    my-countdown(3) is [list: 3,2,1, 0]
end