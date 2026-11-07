AccelAsc := function(n)
    local k, a, y, x, ell, result;

    if n < 1 then
        Error("n must be at least 1");
    fi;

    k := 2;
    a := [1..n];
		a[1]:= 0;
    y := n - 1;
    result := [];

    while k <> 1 do

        k := k - 1;
        x := a[k] + 1;

        while 2 * x <= y do
            a[k] := x;
            y := y - x;
            k := k + 1;
        od;

        ell := k + 1;

        while x <= y do
            a[k] := x;
            a[ell] := y;

            Add(result, a{[1..ell]});

            x := x + 1;
            y := y - 1;
        od;

        y := y + x - 1;
        a[k] := y + 1;

        Add(result, a{[1..k]});

    od;

    return result;
end;


Print(Length(AccelAsc(80)), "\n");
QUIT;
