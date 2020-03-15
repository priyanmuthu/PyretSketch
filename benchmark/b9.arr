fun my-fibo(n):
    if n == 0:
        1
    else:
        if n == 1:
            1
        else:
            my-fibo(n - 1) + my-fibo(n - 2)
        end
    end
where:
    my-fibo(0) is 1
    my-fibo(1) is 1
    my-fibo(2) is 2
    my-fibo(3) is 3
    my-fibo(4) is 5
    my-fibo(5) is 8
    my-fibo(6) is 13
end