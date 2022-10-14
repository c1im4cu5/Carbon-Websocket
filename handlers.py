
def convert_carbon_divide(string, index):
    return float(float(string) / (10 ** index))

def convert_carbon_multiply(string, index):
    return float(round(float(string) * (10 ** index), 5))
