import random
import uuid 

def generate_rule_value(field,row_index):
     field_name =field.field_name.lower()
     if "employee" in field_name and "id" in field_name:
          return f"EMP{row_index+1:05d}"
     elif "uuid" in field_name:
          return str(uuid.uuid4())
     elif"department_code" in field_name:
          return random.choice([
               "HR",
               "IT",
               "FIN",
               "OPS",
               "SALES",
          ])
     return None