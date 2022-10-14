-- Passou no comp
-- example of static and dynamic type differing for a dispatch

Class Book -- sem chaves
    print() : Book {
        {
            out_string("title:      ").out_string(title).out_string("\n");
            out_string("author:     ").out_string(author).out_string("\n");
            self;
        }
    };
};