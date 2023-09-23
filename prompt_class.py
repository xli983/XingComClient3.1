class Prompt:
    def __init__(self, data):
        # Initialization flag
        self.__initializing = True
        
        # Store data
        self.data = data
        
        # Counter for each class type
        class_type_count = {}
        
        for key, value in data.items():
            class_type = value.get("class_type")
            
            # Count the occurrences of each class_type
            if class_type not in class_type_count:
                class_type_count[class_type] = 0
            else:
                class_type_count[class_type] += 1
            
            # Append a number to class_type if it has multiple occurrences
            class_type_name = f"{class_type}_{class_type_count[class_type]}" if class_type_count[class_type] > 0 else class_type
            
            if not hasattr(self, class_type_name):
                setattr(self, class_type_name, {})
            
            for input_key, input_value in value.get('inputs', {}).items():
                getattr(self, class_type_name)[input_key] = input_value
        
        # Turn off initialization flag
        self.__initializing = False

    def __setattr__(self, name, value):
        if hasattr(self, '__initializing') and self.__initializing:
            # Normal behavior during initialization
            super().__setattr__(name, value)
        else:
            paths = name.split('.')
            if len(paths) == 2:
                class_type_name, input_name = paths
                
                # Update self.data to reflect this change
                for key, val in self.data.items():
                    class_type = val.get("class_type")
                    class_type_name_base = class_type_name.split('_')[0]
                    
                    if class_type == class_type_name_base:
                        self.data[key]['inputs'][input_name] = value
                
                # Update the attribute
                if not hasattr(self, class_type_name):
                    super().__setattr__(class_type_name, {})
                
                getattr(self, class_type_name)[input_name] = value
            else:
                super().__setattr__(name, value)

    def update_attribute(self, class_type_name, input_name, value):
        # Update self.data to reflect this change
        print(f"Updating: {class_type_name}.{input_name} to {value}")
        for key, val in self.data.items():
            class_type = val.get("class_type")
            class_type_name_base = class_type_name.split('_')[0]
            
            if class_type == class_type_name_base:
                self.data[key]['inputs'][input_name] = value
        
        # Update the attribute
        if hasattr(self, class_type_name):
            getattr(self, class_type_name)[input_name] = value
        else:
            raise AttributeError(f"Invalid attribute {class_type_name}")

