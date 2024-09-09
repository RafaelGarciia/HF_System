# Translation matrix

ptbr_translation = {
    "window.title"              : 'Sistema HF'   ,

    "word.companie"             : 'Empresa'     ,
    "word.companies"            : 'Empresas'    ,
    "word.employee"             : 'Funcionario' ,
    "word.employees"            : 'Funcionarios',
    "word.date"                 : 'Data'        ,
    "word.sicknote"             : 'Atestado'    ,
    "word.sicknotes"            : 'Atestados'   ,
    "word.new"                  : 'Novo'        ,
    "word.list"                 : 'Lista'       ,
    "word.save"                 : 'Salvar'      ,
    "word.delete"               : 'Excluir'     ,
    "word.name"                 : 'Nome'        ,
    "word.system"               : 'Sistema'     ,
    "word.home"                 : 'Home'        ,
    "word.language"             : 'Linguagem'   ,
    "word.exit"                 : 'Sair'        ,
    "word.register"             : 'Cadastro'    ,

    "phrase.human-resources"    : 'Recursos humanos'    ,
    "phrase.employee-name"      : 'Nome do funcionario' ,
    
    "acronym.RH"                : 'RH'  ,

    "error.name-empty"                  : 'O nome não pode ser vazio'   ,
    "error.companie-empty"              : 'A empresa não pode ser vazia',
    
    "error.companie-already-registered" : 'Empresa já registrada'       ,
    "error.employee-already-registered" : 'Funcionario já registrado'   ,
    
    "error.Company-not-found"           : 'Empresa não encontrada'      ,
    
    "report.companie-success-registered"    : 'Empresa registrada com sucesso'    ,
    "report.employee-success-registered"    : 'Funcionario registrado com sucesso',

    "report.companie-success-deleted"       : 'Empresa excluida com successo'     ,

    "warning.select-an-item"            : 'Selecione um item'              ,
    
    "msg.welcome"               : 'Bem vindo',
}

en_translation = {
    "window.title"              : 'System HF'   ,

    "word.companie"             : 'Companie'    ,
    "word.companies"            : 'Companies'   ,
    "word.employee"             : 'Employee'    ,
    "word.employees"            : 'Employees'   ,
    "word.date"                 : 'Date'        ,
    "word.sicknote"             : 'Sick Note'   ,
    "word.sicknotes"            : 'Sick Notes'  ,
    "word.new"                  : 'New'         ,
    "word.list"                 : 'List'        ,
    "word.save"                 : 'Save'        ,
    "word.delete"               : 'Delete'      ,
    "word.name"                 : 'Name'        ,
    "word.system"               : 'System'      ,
    "word.home"                 : 'Home'        ,
    "word.language"             : 'Language'    ,
    "word.exit"                 : 'Exit'        ,
    "word.register"             : 'Register'    ,
    
    "phrase.human-resources"    : 'Human resources',
    "phrase.employee-name"      : 'Employee name'  ,
    
    "acronym.RH"                : 'HR'  ,

    "error.name-empty"                  : 'The name cannot be empty'    ,
    "error.companie-empty"              : 'The companie cannot be empty',
    
    "error.companie-already-registered" : 'Companie already registered' ,
    "error.employee-already-registered" : 'Employee already registered' ,
    
    "error.Company-not-found"           : 'Company not found'           ,

    "report.companie-success-registered"    : 'Companie successfully registered',
    "report.employee-success-registered"    : 'Employee successfully registered',

    "report.companie-success-deleted"       : 'Companie successfully deleted'   ,
    
    "warning.select-an-item"            : 'Select an item'              ,

    "msg.welcome"               : 'Welcome',
}

translation_matrix = {
    "en"    : en_translation,
    "pt_br" : ptbr_translation
}

class Translate():
    def __init__(self) -> None:
        self.locale = 'en'
        self.active = translation_matrix[self.locale]

    def set_locale_en(self, updates:list = []):
        self.locale = 'en'
        self.active = translation_matrix[self.locale]
        
        for item in updates:
            item()
        
    def set_locale_ptbr(self, updates:list = []):
        self.locale = 'pt_br'
        self.active = translation_matrix[self.locale]
        
        for item in updates:
            item()