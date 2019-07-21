import yaml



class readable_css: 
    def __init__(self, theme='minimal', page='plain'): 
        self.dir = 'theme/' + theme + '/' + page + '.yaml' 
     
    def file(self): 
        with open(self.dir, 'r') as f: 
           F = yaml.safe_load(f) 
        return F 
    
    def dimension(self):
        return self.file()['dimension']

    def template_raw(self):
        return self.file()['template']

    def template_ncol(self): 
        for n in range(len(self.template_raw())-1): 
            if self.template_raw()[n] == '+' and self.template_raw()[n+1] == ' ': 
                return(n) 
                break 
     
    def template_nrow(self): 
        return int(len(self.template_raw()) / (self.template_ncol()+1)) 

    def template_matrix(self):
        n0 = 1
        n1 = n0 + self.template_ncol()
        matrix = []
        while n0 < len(self.template_raw()):
            line = self.template_raw()[n0:n1]
            matrix.append(line)
            n0 += self.template_ncol() + 1
            n1 = n0 + self.template_ncol()
        return matrix
    
    def template_matrix_col(self, m):
        col = [x[m] for x in self.template_matrix()]
        return col

    def template_matrix_row(self, n):
        row = self.template_matrix()


