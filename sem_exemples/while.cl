class Main inherits IO {
    n1: Int <- 0;
    n2: Int <- 3;
    n3: Int;
    main() : Object {
       { 
        out_string("n1 =");
        out_int(n1);
        while n1 < n2 loop   n1 <- n1 + 1 pool;
        out_string("n1 =");
        out_int(n1);
       }
    };
};