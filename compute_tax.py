# ----------------------------------------------------------------------
# Parent class TaxBracket with compute_tax function, implementing template method pattern.
# ----------------------------------------------------------------------
class TaxBracket:
    TAX_PERCENTAGE = 0
    LOWER_BOUND = 0
    UPPER_BOUND = 0
    # init function
    def __init__(self):
        pass
    # helper function for printing result.
    def get_description(self):
        return "parent class TaxBracket"
    # getter setter
    def get_rate(self):
        return self.TAX_PERCENTAGE
    # the 2 functions below are to be modified per TaxBracket class that implements this template class.
    # since a lot of them share similar implementation, i decided to put the implementation in the parent class.
    def compute_tax(self,taxable_income: float):
        return self.compute_taxable_amount(taxable_income) * self.TAX_PERCENTAGE
    def compute_taxable_amount(self,taxable_income: float):
        return min( max(taxable_income - self.LOWER_BOUND, 0) ,self.UPPER_BOUND -  self.LOWER_BOUND)
    
# ----------------------------------------------------------------------
# First Tax Bracket to Highest
# ----------------------------------------------------------------------
class FirstTaxBracket(TaxBracket):
    TAX_PERCENTAGE = 0
    LOWER_BOUND = 0
    UPPER_BOUND = 20000
    def get_description(self):
        return "first 0 - 20000"
    
class SecondTaxBracket(TaxBracket):
    LOWER_BOUND = 20000
    UPPER_BOUND = 40000
    TAX_PERCENTAGE = 10 / 100
    def get_description(self):
        return "next 20001-40000"
    
class ThirdTaxBracket(TaxBracket):
    LOWER_BOUND = 40000
    UPPER_BOUND = 80000
    TAX_PERCENTAGE = 20 / 100
    def get_description(self):
        return "next 40001-80000"

class FourthTaxBracket(TaxBracket):
    LOWER_BOUND = 80000
    UPPER_BOUND = 180000
    TAX_PERCENTAGE = 30 / 100
    def get_description(self):
        return "next 80001-180000"

class HighestTaxBracket(TaxBracket):
    LOWER_BOUND = 180000
    TAX_PERCENTAGE = 40 / 100
    def get_description(self):
        return "180001 and above"
    # implement a different way to calculate taxable_amount since it has no UPPER_BOUND.
    def compute_taxable_amount(self,taxable_income: float):
        return max(taxable_income - self.LOWER_BOUND, 0)
    
# ----------------------------------------------------------------------
# Composite Class To Create Aggregates
# ----------------------------------------------------------------------
class TaxBracketComposite:
    def __init__(self):
        # The list to hold child components (TaxBracket instances)
        self._children:list[TaxBracket] = []
    
    def add_tax_bracket(self, tax_bracket: TaxBracket):
        """Adds a new bracket to the composite."""
        self._children.append(tax_bracket)
    
    def remove_tax_bracket(self, tax_bracket: TaxBracket):
        """Removes a bracket from the composite."""
        self._children.remove(tax_bracket)
    
    def compute_total_tax(self, taxable_income: float):
        """
        Aggregates the tax computed by all individual child brackets. Returns result only, no print output.
        """
        return sum(bracket.compute_tax(taxable_income) for bracket in self._children)
    
    def compute_tax_printable(self, name:str, taxable_income: float) -> float:
        """
        Aggregates the tax computed by all individual child brackets, with prints to stdout.
        """
        printable_result: list[tuple[str, float, float]] = []
        total_tax: float = 0.0
        for tax_bracket in self._children:
            # expects each _children to have both compute_taxable_amount and compute_tax callable method. 
            taxable_amount = tax_bracket.compute_taxable_amount(taxable_income)
            income_taxed = tax_bracket.compute_tax(taxable_income)
            # for debugging
            # print('tx', taxable_amount , 'income taxd',income_taxed , 'from ', tax_bracket.get_description() )
            printable_result.append([tax_bracket.get_description(), tax_bracket.get_rate(), taxable_amount, income_taxed])
            total_tax += income_taxed
        print(f"\nName: {name} | Annual Salary {taxable_income:,.2f}\n")
        
        # column formatting widths
        COL_WIDTH_DESC = 25
        COL_WIDTH_RATE = 10
        COL_WIDTH_INCOME = 15
        COL_WIDTH_TAX = 15
        
        separator = f"+{'-' * COL_WIDTH_DESC}+{'-' * COL_WIDTH_RATE}+{'-' * COL_WIDTH_INCOME}+{'-' * COL_WIDTH_TAX}+"
        
        # print header
        print(separator)
        print(f"|{'Salary Bracket':<{COL_WIDTH_DESC}}|{'Rate':^{COL_WIDTH_RATE}}|{'Taxable Amount':>{COL_WIDTH_INCOME}}|{'Total Tax':>{COL_WIDTH_TAX}}|")
        print(separator)
        
        # print data
        for desc, rate, taxable_amount, tax in printable_result:
            print(f"|{desc:<{COL_WIDTH_DESC}}|{rate * 100:^{COL_WIDTH_RATE-1}.2f}%|{taxable_amount:>{COL_WIDTH_INCOME},.2f}|{tax:>{COL_WIDTH_TAX},.2f}|")

        # print total
        print(separator)
        print(f"|{'**Total**':<{COL_WIDTH_DESC}}|{'':^{COL_WIDTH_RATE}}|{taxable_income:>{COL_WIDTH_INCOME},.2f}|{total_tax:>{COL_WIDTH_TAX},.2f}|")
        print(separator)

# ----------------------------------------------------------------------
# Reusable Initialization Function
# ----------------------------------------------------------------------

def init_tax_system() -> TaxBracketComposite:
    """
    Initializes and returns a new TaxBracketComposite instance configured
    with all tax brackets.
    """
    tax_system = TaxBracketComposite()
    
    # add all tax brackets
    tax_system.add_tax_bracket(FirstTaxBracket())
    tax_system.add_tax_bracket(SecondTaxBracket())
    tax_system.add_tax_bracket(ThirdTaxBracket())
    tax_system.add_tax_bracket(FourthTaxBracket())
    tax_system.add_tax_bracket(HighestTaxBracket())

    return tax_system

# ------------------------------------------------
#               Main Execution Block
# ------------------------------------------------
if __name__ == "__main__":
    # instantiate the Composite object with all of its children
    tax_system = init_tax_system()

    # Composite object is ready, now we can test it. 
    tax_system.compute_tax_printable('Gilbert' , 60000.20)
    tax_system.compute_tax_printable('Maymay' , 80150.15)
    tax_system.compute_tax_printable('Anton' , 200000.80)
    tax_system.compute_tax_printable('Ronald' , -5)