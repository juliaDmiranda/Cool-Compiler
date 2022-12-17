class Main inherits IO {
    n: Int;
    initMsg: String;
    main() : Object {
    {
        let     n1: Int <- 2,
                n2: Int <- 89,
                result: Int,
                result2: Int
        in {
           result2 <- calc(n1, n2); 
           result <- (new Calculadora).calc(n1, n2);      
           out_int(result2);                           
           out_int(result);                  
           if result2 = 91 then out_string("result2 is equal to 91") else out_string("result2 is not equal to 91") fi;
        };

        if n = 0 then out_string("'n' not initialized!") else out_string("'n' was initialized") fi; -- Implime duas vezes 
        n <- 2;
        if true then n else 0 fi;
        out_int(2);

        }
    };

    calc (v: Int,m: Int): Int{
        ((m + v) * 2) / 2
    };
};

class Calculadora {
    n: Int <- 5;
    calc(n1: Int, n2: Int): Int{
        {
        if true then (n1 + n2) * 5 else 4 fi;
        }
    };
};
