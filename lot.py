import os
import openpyxl
import math
from sympy import Symbol, Eq, solve, simplify
from excel_grabber import Excel_Grabber

class Lot:
    def __init__(self, d1, d2, r_type, l_type):
        self.r_type = r_type
        self.d1 = d1
        self.d2 = d2
        self.l_type = l_type
        self._Type_Residential = ['r1', 'basic r2', 'max r2', 'basic r3', 'max r3', 'r4', 'r5']
        self._lot_type = ['interior', 'inside', 'corner', 'through', 'corner-through', 'corner+', 'end lot']
        self.Setbacks = [
        Excel_Grabber().Setback_R1, 
        Excel_Grabber().Setback_basic_R2, 
        Excel_Grabber().Setback_max_R2, 
        Excel_Grabber().Setback_basic_R3, 
        Excel_Grabber().Setback_max_R3, 
        Excel_Grabber().Setback_R4,
        Excel_Grabber().Setback_R5
        ]
    def _area_normal_lot(self): 
        ans = self.d1 * self.d2
        return ans
    def _get_setbacks(self):
        for i in range(0, 7):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.front = self.Setbacks[i][0]
                self.rear = self.Setbacks[i][1]
                self.sides = self.Setbacks[i][2]
                break
        self.x_dim = self.d1 - (2*float(self.sides))
        self.y_dim = self.d2 - float(self.front) - float(self.rear)
        return self.x_dim, self.y_dim
    def _find_front(self):
        a = Symbol('a')
        eq1 = self.PSO_Check / 100
        eq2 = (((self.d1 - 2*(self.sides))*(self.d2 - a - self.rear))/self._area_normal_lot())
        self.front = round(float(solve(eq1 - eq2, a)[0]), 2)
        return self.front
    def _set_new_setback(self):
        self.x_dim = self.d1 - (2*float(self.sides))
        self.y_dim = self.d2 - float(self.front) - float(self.rear)
        return self.x_dim, self.y_dim
    def _compute_AMBF(self):
        AMBF = self.x_dim * self.y_dim
        return round(AMBF, 2) 
    def _compute_PSO(self):
        PSO = (self._compute_AMBF() / self._area_normal_lot()) * 100
        return round(PSO, 2)
    def _compute_ISA(self):
        ISA = (2*self.sides*self.y_dim)+(self.d1*self.rear)
        return round(ISA, 2)
    def _lot_percent_ISA(self):
        Lot_Percent = (float(self._compute_ISA()) / float(self._area_normal_lot())) * 100
        return round(Lot_Percent, 2)
    def _compute_MACA(self):
        MACA = float(self._compute_PSO()) + float(self._lot_percent_ISA())
        return round(MACA, 2)
    def _compute_USA(self):
        USA = self.d1 * self.front
        return round(USA, 2)
    def _lot_percent_USA(self):
        USA_p = (self._compute_USA() / self._area_normal_lot()) * 100
        return round(USA_p, 2)
    def _suggest_new_result(self):
        self._find_front()
        self._set_new_setback()
        self._compute_AMBF()
        self._compute_PSO()
        self._compute_ISA()
        self._compute_USA()
        self._checker_PSO()
        self.validate = [self._checker_TOSL(), self._checker_PSO(), self._checker_USA(), self._checker_ISA(), self._checker_Lot_Type()]
    def _compute_repeat(self):
        self._compute_PSO()
        self._compute_ISA()
        self._compute_USA()
        self.validate = [self._checker_TOSL(), self._checker_PSO(), self._checker_USA(), self._checker_ISA(), self._checker_Lot_Type()]
    def _add_increments(self):
        add_num = 0
        while False in self.validate:
            add_num += 0.05
            new_front = self.front + add_num
            self._incremented_setback(new_front)
            self._compute_AMBF()
            self._compute_repeat()
        self._print_results()
    def _checker_TOSL(self):
        self.TOSL = self._compute_USA() + self._compute_ISA()
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.TOSL_Check = Excel_Grabber().Max_TOSL[i]
                break
        if self.TOSL >= self.TOSL_Check:
            return True
        else:
            return False
    def _checker_PSO(self):
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.PSO_Check = Excel_Grabber().Max_PSO[i]
                break
        if self._compute_PSO() <= self.PSO_Check:
            return True
        else:
            return False
    def _checker_ISA(self):
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.ISA_Check = Excel_Grabber().Max_ISA[i]
                break
        if self._lot_percent_ISA() <= self.ISA_Check:
            return True
        else:
            return False
    def _checker_USA(self):
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.USA_Check = Excel_Grabber().Min_USA[i]
                break
        if self._lot_percent_USA() >= self.USA_Check:
            return True
        else:
            return False
    def _checker_Lot_Type(self):
        for i in range(len(self._lot_type)):
            if self.l_type.lower() == self._lot_type[i]:
                self._lot_type_check = Excel_Grabber().Open_Space_Pct[i]
                break
        if self.l_type.lower() == 'end lot' and self.TOSL <= 50:
            return True
        elif self.TOSL >= self._lot_type_check:
            return True
        else:
            return False
    def _print_results(self):
        print('Area of the lot = ' + str(self._area_normal_lot()) + ' m^2\n\n')
        print('Setbacks (as prescribed under NBCP Rule VIII):\nFront: ' + str(round(self.front, 2)) + 'm\nRear: ' + str(self.rear) + 'm\nSides: ' + str(self.sides) + 'm\n\n')
        print('AMBF = ' + str(self._compute_AMBF()) + 'm^2')
        print('PSO = ' + str(self._compute_PSO()) + '%')
        print('ISA = ' + str(self._compute_ISA()) + 'm^2 --> ' + str(self._lot_percent_ISA()) + '% of the site')
        print('MACA = ' + str(self._compute_MACA()) + '%')
        print('USA = ' + str(self._compute_USA())+ 'm^2 --> ' + str(self._lot_percent_USA()) + '% of the site\n\n')
        print('Based from the Building Code:\nMax PSO = ' + str(self._checker_PSO()) + '\nMax ISA = ' + str(self._checker_ISA()) + '\nMin USA = ' + str(self._checker_USA()) + '\nMax TOSL = ' + str(self._checker_TOSL()) + '\n\nType of Lot = ' + str(self.l_type) + '\nComply? = ' + str(self._checker_Lot_Type()))

