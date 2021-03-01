from lot import Lot
from lot_abutment import Lot_Abutment
from r_types import Type_Residential, Abutments_One_Opt, Abutments_RType, lot_type

def lot_computations():
    lot_a._area_normal_lot()
    lot_a._get_setbacks()
    _iterator('a')
    validator = [lot_a._checker_TOSL(), lot_a._checker_PSO(), lot_a._checker_USA(), lot_a._checker_ISA(), lot_a._checker_Lot_Type()]
    if False in validator:
        print('\n\nIt seems that the results do not follow what\'s required in the Building Code.\nHere\'s our suggested setback\n\n')
        lot_a._suggest_new_result()
        lot_a._add_increments()

def lot_firewall_comp():
        lot_f._area_normal_lot()
        lot_f._get_setbacks()
        _iterator('f')
        validator = [lot_f._checker_TOSL(), lot_f._checker_PSO(), lot_f._checker_USA(), lot_f._checker_ISA(), lot_f._checker_Lot_Type()]
        if False in validator and res_type.lower() not in Abutments_One_Opt:
            print('\n\nIt seems that the original results do not follow what\'s required in the Building Code.\nHere\'s our suggested setback:\n\n')
            lot_f._suggested_new_result()
        else:
            print('\n\nIt seems that the original results do not follow what\'s required in the Building Code.\nHere\'s our suggested setback:\n\n')
            lot_f._compute_repeat()
            lot_f._add_increments()

def _iterator(ch):
        eval('lot_'+ch+'._compute_AMBF')()
        eval('lot_'+ch+'._compute_PSO')()
        eval('lot_'+ch+'._compute_ISA')()
        eval('lot_'+ch+'._compute_USA')()
        eval('lot_'+ch+'._checker_PSO')()
        eval('lot_'+ch+'._checker_ISA')()
        eval('lot_'+ch+'._checker_USA')()
        eval('lot_'+ch+'._checker_TOSL')()
        eval('lot_'+ch+'._checker_Lot_Type')()

if __name__ == '__main__':
    option = 'yes'
    print('''\n\nArchitectural Computation Automator (AMBF, PSO, ISA, MACA, USA, TOSL)
    (Based from the Rule VIII of National Building Code of the Philippines)

    This code works only for square lots with assumption all angles are in 90 degrees.
    Irregular-shaped lots may be supported in future updates.''')
    while str(option).lower() == 'yes' or str(option).lower() == 'y':
        x = input('front size = ')
        while float(x) == ValueError:
            x = input('Sorry, I didn\'t get that\n(Type a number)')
        y = input('side size = ')
        while float(y) == ValueError:
            y = input('Sorry, I didn\'t get that\n(Type a number)\n')
        res_type = input('Residential type\n(type R1, basic R2, max R2, basic R3, max R3, R4, R5)\n')
        while res_type.lower() not in Type_Residential:
            res_type = input('It\'s not a residential type! \n(type R1, basic R2, max R2, basic R3, max R3, R4, R5)\n')
        l_type = input('Lot Type\n(Type interior, inside, corner, through, corner-through, corner+, end lot)\n')
        while l_type.lower() not in lot_type:
            l_type = input('It\'s not a lot type!\n(Typeinterior, inside, corner, through, corner-through, corner+, end lot)\n')
        if res_type.lower() in Type_Residential[1:]:
            abutments = input('With abutments?\n(Type Yes or No)\n')
            while abutments.lower() != 'yes' and abutments.lower() != 'no':
                abutments = input('(Type Yes or No only.)\n')
            if abutments.lower() == 'yes':
                for i in Abutments_RType:
                    if i == res_type.lower():
                        if len(Abutments_RType[i]) == 3:
                            a_opt = input(str(Abutments_RType[i][0]) + ' or ' + str(Abutments_RType[i][1]) + ' or ' + str(Abutments_RType[i][0])+'\n')
                            while a_opt not in Abutments_RType[i]:
                                a_opt = input('Not in options!\nType ' + Abutments_RType[i][0] + ' or ' + str(Abutments_RType[i][1]) + ' or ' + str(Abutments_RType[i][2]) + '\n')
                        else:
                            print('The only option is ' + Abutments_RType[i])
                            a_opt = Abutments_RType[i]
                lot_f = Lot_Abutment(float(x), float(y), res_type, l_type, a_opt)
                lot_firewall_comp()

        else:
            lot_a = Lot(float(x), float(y), res_type, l_type)
            lot_computations()
        option = input('\n\nDo you want to input more lots? (Type Yes or No)\n')