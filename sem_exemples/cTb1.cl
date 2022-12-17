class Main inherits IO {

    main() : Object {
        {sum(1,2);
        comp(1,2);}
    };

    sum(n1:Int, n2:Int): Int{
        n1 + n2
    };
    comp(n1:Int, n2:Int): Bool{
        n1 = n2
    };

    

};