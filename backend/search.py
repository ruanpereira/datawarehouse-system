from file_main import DataFileManagement

# print(f"{index+1}. {value}")
# 
class SearchingFile(DataFileManagement):
    def __init__(self):
        super().__init__()
        self.column_name = str()
        self.unique_values= None
    def apresentacao(self):
        print("informe os campos que voce deseja pesquisar: ")
        for index, value in enumerate(self.columns_list):
            print(f"{index+1}. {value}")
        columm_number = int(input("Sua resposta: "))
        self.column_name = self.columns_list[columm_number-1]
        
    def get_unique_values(self,):
        self.unique_values = self.dataset[self.column_name].unique().tolist()
        self.unique_values = sorted(self.unique_values) if isinstance(self.unique_values[0], (str, int, float)) else self.unique_values
        for index, value in enumerate(self.unique_values):
            print(f"{index+1}. {value}.")
test = SearchingFile()
test.apresentacao()
print(test.get_unique_values())
