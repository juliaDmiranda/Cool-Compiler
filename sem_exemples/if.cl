class Main inherits IO {
    n1: Int;
    n2: Int;
    n3: Int;
    div1: Object;
    div2: Int;
    main() : Object {
        {
            n1 <- sum(1, 2);
            n2 <- sub(5, 2);
            n3 <- mult(10,3);
            out_int(n1);
            out_int(n2);
            out_int(n3);
            div1 <- div(0, n1);
            div2 <- div(n3, n2);
            --out_int(div2);
            if div1 = 1 then out_string("Erro, division by 0!") else out_int(div1) fi; -- duplicado (!!)
            if div2 = 1 then out_string("Erro, division by 0!") else out_int(div2) fi;

        }
    };

    sum (v: Int,m: Int): Int{
        v + m
    };
    sub (v: Int,m: Int): Int{
        v - m
    };
    mult (v: Int,m: Int): Int{
        v * m
    };
    div (v: Int,m: Int): Object{
       { 
        
        if (v = 0) then 1 else v / m fi; -- as vezes operações precisam estar entre parêntesis
       }
        
    };
};