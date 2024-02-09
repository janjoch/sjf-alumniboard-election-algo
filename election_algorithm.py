import numpy as np

import pandas as pd


def pd_styling_color_boolean(val):
    color =''
    if val == True:
        color = 'white'
    elif val == False:
        color = 'lightgrey'
    return 'background-color: %s' % color


def pd_rewrite_bool(val):
    if val == True:
        return "1"
    elif val == False:
        return "0"
    return val


def pd_styling(styler):
    for col in ("votes", "total votes", "weighted rank sum"):
        if(col in styler.data.columns):
            styler.background_gradient(axis=None, cmap="YlGnBu", subset=col)
    styler.format(pd_rewrite_bool)
    styler.applymap(pd_styling_color_boolean)
    styler.set_table_styles([  # create internal CSS classes
        {'selector': '.elected', 'props': 'background-color: green;'},
    ], overwrite=False)
    return styler


class ElectionEvaluation:

    # Compliance rules according to Art. 4 of "Organisationsreglement des SJf-Alumni-Rates" version 30.11.2023
    COMPLIANCE_RULES = {
        "A1": lambda x: x >= 2,
        "A2": lambda x: x >= 1,
        "A3": lambda x: x >= 1,
        "B": lambda x: x >= 3,
        "C": lambda x: x >= 1,
        "D": lambda x: ~x <= 2,
    }
    N_MEMBERS = 7

    def __init__(
        self,
        file_path,
        verbose=True,
    ):
        self.verbose = verbose
        self.results = self.import_xlsx(file_path)
        self.find_compliant_combination()

    @property
    def data(
        self,
    ):
        return self.results
    
    @property
    def data_sorted(
        self,
    ):
        return self.get_sorted()
    
    def _repr_html_(self):
        return self.data_sorted.style.pipe(pd_styling)._repr_html_()

    def import_xlsx(
        self,
        io,
        **kwargs,
    ):
        return pd.read_excel(
            io=io,
            skiprows=(1,),
            false_values=(np.nan, "", pd.NA),
            converters={
                "A1": bool,
                "A2": bool,
                "A3": bool,
                "B": bool,
                "C": bool,
                "D": bool,
            },
            **kwargs,
        )


    def get_sorted(self, by="votes", ascending=False):
        return self.results.sort_values(by=by, ascending=ascending)

    def subset_results(self, selection):
        return self.results.iloc[list(selection)]
    
    def check_compliance(self, selection):
        subset = self.subset_results(selection)
        counts = subset.sum()
        if self.verbose:
            print(counts)
        compliance = {
                key: check(counts[key])
                for (key, check)
                in self.COMPLIANCE_RULES.items()
        }

        return compliance

    def find_compliant_combination(self, n_members=None):
        self._report = pd.DataFrame(columns=("candidates", "ranks", "total votes", "weighted rank sum") + tuple(self.COMPLIANCE_RULES.keys()) + ("compliant",))
        index_sorted = self.get_sorted().index
        gen = self.valid_indexes_int(n_members=n_members)

        while True:

            # bool array for candidate selection
            i = next(gen)
            selection_bool = self.int_to_bool_array(i)

            if(len(selection_bool) > len(index_sorted)):
                print("WARNING: NO COMPLIANT COMBINATION FOUND")
                return

            selection_bool_extended = np.append(selection_bool, [False] * (len(index_sorted) - len(selection_bool)))
            index_selection = index_sorted[selection_bool_extended]

            compliance = self.check_compliance(index_selection)

            compliant = np.array(list(compliance.values())).all()

            self.add_report_row(i, index_selection, selection_bool_extended, compliance, compliant)

            if self.verbose:
                print(index_selection)
                print(self.results["candidate_name"][index_selection])
                print(compliance)

            # COMPLIANT COMBINATION FOUND
            if compliant:
                self.results["elected"] = False
                self.results.loc[index_selection, "elected"] = True
                return index_selection

    def add_report_row(self, i, index_selection, selection_bool, compliance, compliant):
        self._report.loc[len(self._report)] = pd.Series(
            {
                "candidates": ", ".join(self.results["candidate_name"][index_selection]),
                "ranks": ",".join(map(str, np.where(selection_bool)[0])),
                "total votes": self.results["votes"][index_selection].sum(),
                "weighted rank sum": i,
                **compliance,
                "compliant": compliant,
            }
        )

    @property
    def report(self):
        return self._report.style.pipe(pd_styling)

    def int_to_bool_array(self, number):
        return np.flip(
            np.array(
                [
                    bit=="1"
                    for bit
                    in list(bin(number)[2:])
                ]
            )
        )

    def valid_indexes_int(self, n_members=None):
        if n_members is None:
            n_members = self.N_MEMBERS
        i = 0
        while True:
            if(self.int_to_bool_array(i).sum() == n_members):
                yield i
            i += 1


    def valid_indexes_bool(self, n_members=None):
        gen = self.valid_indexes_int(n_members=n_members)
        while True:
            yield self.int_to_bool_array(next(gen))


## no rubber ducks were harmed during debugging ##
