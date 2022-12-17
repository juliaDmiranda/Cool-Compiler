class Main inherits IO {
    main(): Object {
        let 
            name: String <- "",
            age: Int <- 0,
            sub:String
        in {
            out_string("Please enter your name:\n");
            name <- in_string();                                
            out_string("Please enter your age:\n");
            age <- in_int();                                    
            out_string("Your name is ");
            out_string(name);
            out_string("And you have ");
            out_int(age);
        }
    };
};
