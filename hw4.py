import sys
from build_data import get_data


field_dict = {
    "Education.Bachelor's Degree or Higher": 0,
    "Education.High School or Higher": 0,
    "Ethnicities.American Indian and Alaska Native Alone": 1,
    "Ethnicities.Asian Alone": 1,
    "Ethnicities.Black Alone": 1,
    "Ethnicities.Hispanic or Latino": 1,
    "Ethnicities.Native Hawaiian and Other Pacific Islander Alone": 1,
    "Ethnicities.Two or More Races": 1,
    "Ethnicities.White Alone": 1,
    "Ethnicities.White Alone, not Hispanic or Latino": 1,
    "Income.Persons Below Poverty Level": 2}

def display(data):
    for user_input in data:
        print(user_input, "\n")

def filter_state(data, state_abbr):
    return [user_input for user_input in data if user_input.state == state_abbr]

def filter_gt(data, field, value):
    idx = field.find(".")
    idx+=1
    if field_dict[field] == 0: # Education
        return [user_input for user_input in data if user_input.education[field[idx:]] > value]
    if field_dict[field] == 1: # Ethnicitiy
        return [user_input for user_input in data if user_input.ethnicities[field[idx:]] > value]
    if field_dict[field] == 2: # Income
        return [user_input for user_input in data if user_input.income[field[idx:]] > value]

def filter_lt(data, field, value):
    idx = field.find(".")
    idx += 1
    if field_dict[field] == 0:  # Education
        return [user_input for user_input in data if user_input.education[field[idx:]] < value]
    if field_dict[field] == 1:  # Ethnicitiy
        return [user_input for user_input in data if user_input.ethnicities[field[idx:]] < value]
    if field_dict[field] == 2:  # Income
        return [user_input for user_input in data if user_input.income[field[idx:]] < value]

def population_total(data):
    total_population = sum(user_input.population['2014 Population'] for user_input in data)
    print(f'2014 population {total_population}')

def population(data, field):
    idx = field.find(".")
    idx += 1
    subtotal = 0
    for user_input in data:
        if field_dict[field] == 0:  # Education
            subtotal += (user_input.education[field[idx:]]/100) * user_input.population['2014 Population']
        if field_dict[field] == 1:  # Ethnicitiy
            subtotal += (user_input.ethnicities[field[idx:]] / 100) * user_input.population['2014 Population']
        if field_dict[field] == 2:  # Income
            subtotal += (user_input.income[field[idx:]] / 100) * user_input.population['2014 Population']
    print("2014", field[idx:], "population:", int(subtotal))

def percent(data,field):
    idx = field.find(".")
    idx += 1
    subtotal = 0
    total = 0
    for user_input in data:
        total += user_input.population['2014 Population']
        if field_dict[field] == 0:  # Education
            subtotal += (user_input.education[field[idx:]] / 100) * user_input.population['2014 Population']
        if field_dict[field] == 1:  # Ethnicitiy
            subtotal += (user_input.ethnicities[field[idx:]] / 100) * user_input.population['2014 Population']
        if field_dict[field] == 2:  # Income
            subtotal += (user_input.income[field[idx:]] / 100) * user_input.population['2014 Population']

    print("2014", field[idx:], "percentage:", (subtotal/total)*100)

def process_operations_file(name, data):
    try:
        with open(name, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                if parts[0] == 'display':
                    display(data)
                elif parts[0] == 'filter-state':
                    data = filter_state(data ,parts[1])
                    print(f"Filter: state == {parts[1]} ({len(data)} entries)")
                elif parts[0] == 'filter-gt':
                    data = filter_gt(data, parts[1],float(parts[2]))
                    print(f"Filter: {parts[1]} gt {parts[2]} ({len(data)} entries")
                elif parts[0] == 'filter-lt':
                    data = filter_lt(data, parts[1], float(parts[2]))
                    print(f"Filter: {parts[1]} lt {parts[2]} ({len(data)} entries")
                elif parts[0] == 'population-total':
                    population_total(data)

                elif parts[0] == 'population':
                    population(data, parts[1])

                elif parts[0] == 'percent':
                    percent(data, parts[1])
                else:
                    print(f"Error: Unsupported operation '{line}")
    except FileNotFoundError:
        print(f"Error:This file '{name}' does not exist")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Error: Please provide a file name as a command-line")
        sys.exit(1)
    name = sys.argv[1]
    data = sys.argv[2]
    print(f"number of entries: {len(data)}")
    r_data = get_data()
    process_operations_file(name, r_data)
