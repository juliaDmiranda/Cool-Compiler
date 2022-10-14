---COMPILADOR js ACEITA
---O MEU NÃO aceitava
class Main  inherits                          -- sem TYPE e sem {
    main(pi:Int) : Object {
        {
        out_string("Hello, world.\n");
        variable;
        }
    };
}                                               -- sem ;

class Main inherits OI{
    main(pi:Int) : Object {
    {
        out_string("Hello, world.\n");
        let exame: IO in 2                  -- aqui falta ;
                                  -- falta } (erros para frente que não existem 
                                            --mas por consequência do meu tratamento de erros)
    };
};