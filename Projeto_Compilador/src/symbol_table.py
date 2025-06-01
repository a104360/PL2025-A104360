class SymbolTable:

    def __init__(self, other=None):
        if other is not None:
            self.symbol_table = dict(other.symbol_table)
            self.current_stack_position = other.current_stack_position
            self.func_pointer = other.func_pointer
            self.current_state = other.current_state
        else:
            self.symbol_table = {}
            self.current_stack_position = 0
            self.func_pointer = 0
            self.current_state = "global"
            self._ensure_state_exists("global")

    def _ensure_state_exists(self, state):
        if state not in self.symbol_table:
            self.symbol_table[state] = {}

    def set_state(self, state):
        self.current_state = state
        self._ensure_state_exists(state)



    def add_variable(self, name, var_type,getter=None):

        state = self.current_state
        if name in self.symbol_table[state]:
            raise ValueError(f"Variable '{name}' already declared in state '{state}'.")


        if getter is not None:
            self.symbol_table[state][name] = {
                "type": var_type,
                "position": -1,
                "getter": getter
            }

        else:
            self.symbol_table[state][name] = {
                "type": var_type,
                "position": self.current_stack_position,
            }

            self.current_stack_position += 1

        return self.symbol_table[state][name]

    def add_array(self, name, var_type, lower, upper):
        state = self.current_state
        if name in self.symbol_table[state]:
            raise ValueError(f"Array '{name}' already declared in state '{state}'.")

        size = upper - lower + 1

        self.symbol_table[state][name] = {
            "type": f"array_{var_type}",
            "position": self.current_stack_position,
            "lower_bound": lower,
            "upper_bound": upper,
            "size": size,
            "base_type": var_type
        }

        self.current_stack_position += size
        return self.symbol_table[state][name]

    def add_function(self, name, return_type, argument_types):
        global_scope = "global"
        if name in self.symbol_table[global_scope]:
            raise ValueError(f"Function '{name}' already declared.")

        self.symbol_table[global_scope][name] = {
            "type": "Func",
            "position": self.func_pointer,
            "arguments": list(map(str.lower, argument_types)),
            "return": return_type.lower(),
            "code_of_return": ""
        }

        self.func_pointer += 1
        self._ensure_state_exists(name)  # create scope for function body
        return self.symbol_table[global_scope][name]
    
    def set_func_return_code(self,func,code):
        if func not in self.symbol_table["global"]:
            raise KeyError(f"Função '{func}' não encontrada para atribuir código de retorno.")

        # Atualiza somente a chave "code_of_return", sem apagar as demais
        self.symbol_table["global"][func]["code_of_return"] = code
        return self.symbol_table["global"][func]["code_of_return"]    
    
    def get_variable(self, name):
        """Looks up variable first in current scope, then in global scope."""
        state = self.current_state
        if name in self.symbol_table.get(state, {}):
            return self.symbol_table[state][name]
        elif name in self.symbol_table.get("global", {}):
            return self.symbol_table["global"][name]
        else:
            raise KeyError(f"Variable '{name}' not found in current or global scope.")

    def get_func_args(self,func):
        return self.symbol_table["global"][func]["arguments"]
    
    def get_func_return_code(self,func):
        return self.symbol_table["global"][func]["code_of_return"]
    
    def get_func_return(self,func):
        return self.symbol_table["global"][func]["return"]
    
    def get_position(self, name):
        return self.get_variable(name)["position"]
    
    def get_type(self, name):
        return self.get_variable(name)["type"]
    
    def get_getter(self, name):
        return self.get_variable(name)["getter"]
    
    def is_array(self, name):
        try:
            return self.get_type(name).startswith("array_")
        except:
            return False
        
    def get_array_base_type(self, name):
        return self.get_variable(name)["base_type"]
    
    def get_array_lower_bound(self, name):
        return self.get_variable(name)["lower_bound"]
    
    def get_array_upper_bound(self, name):
        return self.get_variable(name)["upper_bound"]
    
    def get_array_size(self, name):
        return self.get_variable(name)["size"]
    

    def has_variable(self, name):
        for state in self.symbol_table:
            if name in self.symbol_table[state] or name in self.symbol_table["global"]:
                return True
        return False

    
    def reset(self):
        """Clears the symbol table and resets the stack position."""
        self.symbol_table.clear()
        self.current_stack_position = 0
        self.func_pointer = 0
        self.current_state = "global"
        self._ensure_state_exists("global")

    def dump(self):
        print(f"=== Symbol Table ===")
        for state, entries in self.symbol_table.items():
            print(f"[State: {state}]")
            for name, info in entries.items():
                print(f"  {name}: {info}")
        print("====================")

generalSTable = SymbolTable()