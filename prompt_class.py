from collections import defaultdict

class Prompt:
    def __init__(self, data):
        self.__initializing = True
        self.data = data
        class_type_count = defaultdict(int)

        for key, value in data.items():
            class_type = value.get("class_type")
            class_type_name = self._get_class_type_name(class_type, class_type_count)
            
            if not hasattr(self, class_type_name):
                setattr(self, class_type_name, {})

            for input_key, input_value in value.get('inputs', {}).items():
                getattr(self, class_type_name)[input_key] = input_value
        self.__initializing = False

    def _get_class_type_name(self, class_type, class_type_count):
        class_type_count[class_type] += 1
        return f"{class_type}_{class_type_count[class_type]-1}" if class_type_count[class_type] > 1 else class_type

    def __setattr__(self, name, value):
        if hasattr(self, '__initializing') and self.__initializing:
            super().__setattr__(name, value)
        else:
            paths = name.split('.')
            if len(paths) == 2:
                self._update_data_and_attribute(paths[0], paths[1], value)
            else:
                super().__setattr__(name, value)

    def _update_data_and_attribute(self, class_type_name, input_name, value):
        self._update_data(class_type_name, input_name, value)

        if not hasattr(self, class_type_name):
            super().__setattr__(class_type_name, {})
            
        getattr(self, class_type_name)[input_name] = value

    def _update_data(self, class_type_name, input_name, value):
        for key, val in self.data.items():
            class_type = val.get("class_type")
            class_type_name_base = class_type_name.split('_')[0]
            
            if class_type == class_type_name_base:
                if 'inputs' in val:
                    val['inputs'][input_name] = value
                else:
                    raise KeyError(f"No 'inputs' key for class_type: {class_type}")

    def update_attribute(self, class_type_name, input_name, value):
        print(f"Updating: {class_type_name}.{input_name} to {value}")
        self._update_data(class_type_name, input_name, value)

        if hasattr(self, class_type_name):
            getattr(self, class_type_name)[input_name] = value
        else:
            raise AttributeError(f"Invalid attribute {class_type_name}")
        
    def append_attribute(self, class_type_name, input_name, value):
            if hasattr(self, class_type_name) and input_name in getattr(self, class_type_name):
                existing_value = getattr(self, class_type_name)[input_name]
                new_value = f"{existing_value}, {value}"
                getattr(self, class_type_name)[input_name] = new_value
            else:
                raise AttributeError(f"Invalid attribute {class_type_name} or {input_name}")
            
    def add_section(self, section_id, section_data):
        self.data[section_id] = section_data

    def add_lora(self, input_lora):
        base_model_clip = 4  # Starting model and clip value
        current_id = 22  # Starting ID

        for lora_entry in input_lora:
            lora_name = lora_entry['name']
            intensity = lora_entry['intensity']

            lora_item = {
                "inputs": {
                    "lora_name": f"{lora_name}.safetensors",
                    "strength_model": intensity,
                    "strength_clip": 1.0,
                    "model": [str(base_model_clip), 0],
                    "clip": [str(base_model_clip), 1]
                },
                "class_type": "LoraLoader"
            }

            self.add_section(str(current_id), lora_item)  # Use the new method

            # Update values for the next iteration
            base_model_clip = current_id
            current_id += 1


    def link_lora(self, LoraList):
        if LoraList is not None and LoraList != []:
            LoraNum = len(LoraList)
            self.update_attribute("CLIPTextEncode", "clip", [str(22+LoraNum-1), 1])
            self.update_attribute("KSampler", "model", [str(22+LoraNum-1), 0])

    def update_prompt(self, node_pos, value):
        self.data[node_pos]['inputs']['text'] = value

    def get_prompt_position(self, input_name):
        for key, val in self.data.items():
            class_type = val.get("class_type")
            if class_type == "KSampler":
                if 'inputs' in val:
                    return val['inputs'][input_name][0]
                else:
                    raise KeyError(f"No 'inputs' key for class_type: {class_type}")
    
