from lot import Lot
from excel_grabber import Excel_Grabber

class Lot_Abutment(Lot):
    def __init__(self, d1, d2, r_type, l_type, a_side):
        super().__init__(d1, d2, r_type, l_type)
        self.a_side = a_side
        self._opt_abutments = ['one side', 'both sides', 'rear']
        self._opt_list = []
        self._opt_res = []
    def _get_setbacks(self):
        for i in range(1, 7):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.front = self.Setbacks[i][0]
                self.rear = self.Setbacks[i][1]
                self.sides = self.Setbacks[i][2]
                break
        if self.a_side.lower() == 'one side':
            self.x_dim = self.d1 - (float(self.sides))
            self.y_dim = self.d2 - float(self.front) - float(self.rear)
        elif self.a_side.lower() == 'both sides':
            self.x_dim = self.d1
            self.y_dim = self.d2 - float(self.front) - float(self.rear)
        else:
            self.x_dim = self.d1 - (float(self.sides))
            self.y_dim = self.d2 - float(self.front)
        return self.x_dim, self.y_dim
    def _suggested_new_result(self):
        self.r_type_conditions = {
            'basic r2':'one side',
            'max r2':'one side',
            'basic r3':['one side', 'both sides', 'rear'], 
            'max r3':['one side', 'both sides', 'rear'], 
            'r4':'both sides', 
            'r5':['one side', 'both sides', 'rear']
            }
        for r_types in self.r_type_conditions:
            if self.r_type == r_types and len(self.r_type_conditions[r_types]) == 3:
                for ab_opts in range(len(self.r_type_conditions[r_types])): 
                    self.a_side = self.r_type_conditions[r_types][ab_opts] 
                    self._get_setbacks() 
                    self._do_operations() 
                self._opts_validator() 
                self._compute_repeat()
                self._add_increments()
    def _do_operations(self):
        self._instance = self.a_side
        self._compute_AMBF()
        self._compute_PSO()
        self._compute_ISA()
        self._compute_USA()
        self.validator = [self._checker_TOSL(), self._checker_PSO(), self._checker_USA(), self._checker_ISA(), self._checker_Lot_Type()]
        self._add_opts()
    def _add_opts(self):
        self._opt_list.append(self._instance)
        self._opt_res.append(self.validator)
    def _opts_validator(self):
        self._True_Statements = []
        for ins in range(len(self._opt_res)):
            num = 0
            for tru in range(len(self._opt_res[ins])):
                if self._opt_res[ins][tru] == True:
                    num += 1
            self._True_Statements.append(num)
        for deter in range(len(self._True_Statements)):
            if self._True_Statements[deter] == max(self._True_Statements):
                self.a_side = self._opt_list[deter]
                break
    def _compute_repeat(self):
        self._compute_PSO()
        self._compute_ISA()
        self._compute_USA()
        self.validate = [self._checker_TOSL(), self._checker_PSO(), self._checker_USA(), self._checker_ISA(), self._checker_Lot_Type()]
    def _add_increments(self):
        counter = 0
        add_num = 0
        while False in self.validate:
            counter += 1
            add_num += 0.05
            new_front = self.front + add_num
            self._incremented_setback(new_front)
            self._compute_AMBF()
            self._compute_repeat()
        self._print_results()
    def _incremented_setback(self, new_front):
        self.front = new_front
        if self.a_side.lower() == 'one side':
            self.x_dim = self.d1 - (float(self.sides))
            self.y_dim = self.d2 - float(self.front) - float(self.rear)
        elif self.a_side.lower() == 'both sides':
            self.x_dim = self.d1
            self.y_dim = self.d2 - float(self.front) - float(self.rear)
        else:
            self.x_dim = self.d1 - (float(self.sides))
            self.y_dim = self.d2 - float(self.front)
        return self.x_dim, self.y_dim
    def _compute_ISA(self):
        if self.a_side.lower() == 'one side':
            ISA = (self.sides*self.y_dim)+(self.d1*self.rear)
        elif self.a_side.lower() == 'both sides':
            ISA = self.d1*self.rear
        else:
            ISA = (2*self.sides*self.y_dim)
        return round(ISA, 2)
    def _checker_TOSL(self):
        self.TOSL = self._compute_USA() + self._compute_ISA()
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.TOSL_Check = Excel_Grabber().FMax_TOSL[i]
                break
        if self.TOSL >= self.TOSL_Check:
            return True
        else:
            return False
    def _checker_PSO(self):
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.PSO_Check = Excel_Grabber().FMax_PSO[i]
                break
        if self._compute_PSO() <= self.PSO_Check:
            return True
        else:
            return False
    def _checker_ISA(self):
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.ISA_Check = Excel_Grabber().FMax_ISA[i]
                break
        if self._lot_percent_ISA() <= self.ISA_Check:
            return True
        else:
            return False
    def _checker_USA(self):
        for i in range(len(self._Type_Residential)):
            if self.r_type.lower() == self._Type_Residential[i]:
                self.USA_Check = Excel_Grabber().FMin_USA[i]
                break
        if self._lot_percent_USA() >= self.USA_Check:
            return True
        else:
            return False
    def _print_results(self):
        print('Area of the lot = ' + str(self._area_normal_lot()) + ' m^2\n\n')
        print('Abutments = ' + str(self.a_side))
        if self.a_side.lower() == 'one side':
            print('Setbacks (as prescribed under NBCP Rule VIII):\nFront: ' + str(round(self.front, 2)) + 'm\nRear: ' + str(self.rear) + 'm\nOne Side: ' + str(self.sides) + 'm\n\n')
        elif self.a_side.lower() == 'both sides':
            print('Setbacks (as prescribed under NBCP Rule VIII):\nFront: ' + str(round(self.front, 2)) + 'm\nRear: ' + str(self.rear) + 'm\n\n')
        else:
            print('Setbacks (as prescribed under NBCP Rule VIII):\nFront: ' + str(round(self.front, 2)) + 'm\nSides: ' + str(self.sides) + 'm\n\n')
        
        print('AMBF = ' + str(self._compute_AMBF()) + 'm^2')
        print('PSO = ' + str(self._compute_PSO()) + '%')
        print('ISA = ' + str(self._compute_ISA()) + 'm^2 --> ' + str(self._lot_percent_ISA()) + '% of the site')
        print('MACA = ' + str(self._compute_MACA()) + '%')
        print('USA = ' + str(self._compute_USA())+ 'm^2 --> ' + str(self._lot_percent_USA()) + '% of the site\n\n')
        print('Based from the Building Code:\nMax PSO = ' + str(self._checker_PSO()) + '\nMax ISA = ' + str(self._checker_ISA()) + '\nMin USA = ' + str(self._checker_USA()) + '\nMax TOSL = ' + str(self._checker_TOSL()) + '\n\nType of Lot = ' + str(self.l_type) + '\nComply? = ' + str(self._checker_Lot_Type()))