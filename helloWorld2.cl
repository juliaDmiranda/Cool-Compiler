class Bazz inherits IO {
 h : Int <- 1;
 g : Foo <- case self of
		 	n : Bazz => (new Foo);
		 	n : Razz => (new Bar);
			n : Foo => (new Razz);
			n : Bar => n;
		 esac;

 i : Object <- printh();

 printh() : Int { { out_int(h); 0; } };

 --doh() : Int { (let i: Int <- h in { h <- h + 1; i; } ) }; -- ERRO
};


class Bar inherits Razz {

 c : Int <- doh();

 d : Object <- printh();
};

class Main inherits IO {
 a : Bazz <- new Bazz;
 b : Foo <- new Foo;
 c : Razz <- new Razz;
 d : Bar <- new Bar;

 main(): String { { out_string("\n") ; "\t nothing" ; } };

};