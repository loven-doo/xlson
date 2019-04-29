import json
from copy import deepcopy

from jsondler.json_tools.requests import tuplize_json_coord_pairs
from jsondler.json_tools import deepupdate, deepdiff
from jsondler.json_tools.serialization import serialize_field


class XLSonHandler(object):

    cell_default_meta = {
        'data_type': 'n',
        'style_id': 0,
        'pivotButton': False,
        'alignment': {
            'horizontal': None,
            'vertical': None,
            'indent': 0.0,
            'relativeIndent': 0.0,
            'justifyLastLine': None,
            'readingOrder': 0.0,
            'textRotation': 0,
            'wrapText': None,
            'shrinkToFit': None
        },
        'merged_with': [],
        'merged_to': None,
        'font': {
            'name': 'Calibri',
            'family': 2.0,
            'sz': 11.0,
            'b': False,
            'i': False,
            'u': None,
            'strike': None,
            'color': {
                'type': 'theme',
                'theme': 1,
                'tint': 0.0
            },
            'vertAlign': None,
            'charset': 204,
            'outline': None,
            'shadow': None,
            'condense': None,
            'extend': None,
            'scheme': 'minor'
        },
        'fill': {
            'bgColor': {
                'rgb': '00000000',
                'type': 'rgb',
                'tint': 0.0
            },
            'fgColor': {
                'rgb': '00000000',
                'type': 'rgb',
                'tint': 0.0
            },
        },
        'border': {
            'outline': True,
            'right': {
                'style': None,
                'color': None
            },
            'left': {
                'style': None,
                'color': None
            },
            'top': {
                'style': None,
                'color': None
            },
            'bottom': {
                'style': None,
                'color': None
            },
        },
    }

    def __init__(self, xlson):
        self._xlson = XLSonHandler.prepare_xlson(xlson)
        if "cell_default_meta" in xlson:
            self.cell_default_meta = self._xlson["cell_default_meta"]

    @classmethod
    def load(cls, xlson_path):
        with open(xlson_path) as xlson_f:
            xlson = tuplize_coords_in_prep_xl(json.load(xlson_f))
        return cls(xlson=xlson)

    def dump(self, xlson_path):
        xlson_f = open(xlson_path, 'w')
        json.dump(self.xlson, xlson_f, indent=2, default=serialize_field, ensure_ascii=False)
        xlson_f.close()

    @property
    def xlson(self):
        xlson = deepcopy(self._xlson)
        xlson['main_sheet']['meta_df'] = self._xlson['main_sheet']['meta_df'].meta_df
        for supp_sheet in xlson['supp_sheets']:
            supp_sheet['meta_df'] = supp_sheet['meta_df'].meta_df
        return xlson

    def __getitem__(self, item):
        return self._xlson[item]

    def __setitem__(self, key, value):
        self._xlson[key] = value

    def __delitem__(self, key):
        del self._xlson[key]

    def __eq__(self, other):
        return self._xlson == other.xlson

    def pop(self, key):
        return self._xlson.pop(key)

    @staticmethod
    def prepare_xlson(xlson):
        if "cell_default_meta" in xlson:
            cell_default_meta = xlson["cell_default_meta"]
        else:
            cell_default_meta = XLSonHandler.cell_default_meta
        prep_xlson = deepcopy(xlson)
        prep_xlson['main_sheet']['meta_df'] = CellsMetaDF(xlson['main_sheet']['meta_df'],
                                                          cell_default_meta=cell_default_meta)
        for supp_sheet in prep_xlson['supp_sheets']:
            supp_sheet['meta_df'] = CellsMetaDF(supp_sheet['meta_df'],
                                                cell_default_meta=cell_default_meta)
        return prep_xlson


class CellsMetaDF(object):

    def __init__(self, meta_df, cell_default_meta):
        self.meta_df = meta_df
        self.cell_default_meta = cell_default_meta

    def __getitem__(self, item):
        if item < 0:
            item = len(self.meta_df)-item
        return CellsMetaRow(self.meta_df[item], self.cell_default_meta)

    def __setitem__(self, key, value):
        self.meta_df[key] = value

    def __eq__(self, other):
        return self.meta_df == other.meta_df

    def __len__(self):
        return len(self.meta_df)


class CellsMetaRow(object):

    def __init__(self, meta_row, cell_default_meta):
        self.meta_row = meta_row
        self.cell_default_meta = cell_default_meta

    def __getitem__(self, item):
        if item < 0:
            item = len(self.meta_row)-item
        if self.meta_row[item]:
            # return deepupdate(deepcopy(self.cell_default_meta), self.meta_row[item])
            # return CellMeta(cell_default_meta=self.cell_default_meta, cell_diff_meta=self.meta_row[item])
            return self.meta_row[item]
        else:
            return self.cell_default_meta

    def __setitem__(self, key, value):
        if value:
            # self.meta_row[key] = deepdiff(self.cell_default_meta, value)
            self.meta_row[key] = value
        else:
            # self.meta_row[key] = {}
            self.meta_row[key] = None

    def __len__(self):
        return len(self.meta_row)


class CellMeta(object):

    def __init__(self, cell_default_meta, cell_diff_meta):
        self.cell_default_meta = cell_default_meta
        self.cell_diff_meta = cell_diff_meta

    def __getitem__(self, item):
        return self.cell_diff_meta.get(item, self.cell_default_meta[item])


def tuplize_coords_in_prep_xl(prep_xl_dict):
    coords_paths = [
        ("main_sheet", "meta_df", "*", "*", "merged_to"),
        ("main_sheet", "meta_df", "*", "*", "merged_with", "*"),
        ("supp_sheets", "*", "meta_df", "*", "*", "merged_to"),
        ("supp_sheets", "*", "meta_df", "*", "*", "merged_with", "*"),
    ]

    return tuplize_json_coord_pairs(prep_xl_dict, *coords_paths)
