def compute_tax_simple(person: str, value: str):
    LOWER_BOUND_FIRST_BRACKET = 20000
    LOWER_BOUND_SECOND_BRACKET = 40000
    LOWER_BOUND_THIRD_BRACKET = 80000
    LOWER_BOUND_FOURTH_BRACKET = 180000

    print('name', person)

    first_bracket_tax =  min( max(value - LOWER_BOUND_FIRST_BRACKET, 0) ,LOWER_BOUND_SECOND_BRACKET -  LOWER_BOUND_FIRST_BRACKET)  * 10 / 100 
    print('1st bracket tax', f"{first_bracket_tax:.2f}")
    second_bracket_tax =  min( max(value - LOWER_BOUND_SECOND_BRACKET, 0) ,LOWER_BOUND_THIRD_BRACKET -  LOWER_BOUND_SECOND_BRACKET)  * 20 / 100
    print('2nd bracket tax', second_bracket_tax)
    third_bracket_tax =  min( max(value - LOWER_BOUND_THIRD_BRACKET, 0) ,LOWER_BOUND_FOURTH_BRACKET -  LOWER_BOUND_THIRD_BRACKET)  * 30 / 100
    print('3rd bracket tax', third_bracket_tax)
    highest_bracket_tax =   max(value - LOWER_BOUND_FOURTH_BRACKET, 0) * 40 / 100
    print('highest bracket tax', highest_bracket_tax)

    print('total', highest_bracket_tax + third_bracket_tax + second_bracket_tax + first_bracket_tax )


    return highest_bracket_tax + third_bracket_tax + second_bracket_tax + first_bracket_tax 
    

    
compute_tax_simple('Gilbert' , 60000)
compute_tax_simple('Maymay' , 80150)

compute_tax_simple('Anton' , 200000)

compute_tax_simple('Ronald' , -5)
