import json

from openpyxl.utils import coordinate_to_tuple
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Color

from jsondler.json_tools import deepdiff
from xlson._lib.obj_tools import expand_attrs_dict, deepupdate_attrs


CELL_DEFAULT_META = {  # TODO: create special object in setup_xlson
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
    'fill': {  # TODO: check for 'patternType'
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
    'border': {  # TODO: use all border directions
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


def cell_meta_to_dict(cell, merged_cells_dict, jsonize=False):
    cell_coords_pair = tuple(map(lambda c: c - 1, coordinate_to_tuple(cell.coordinate)))
    meta_dict = {
        'data_type': cell.data_type,
        'style_id': cell.style_id,
        'pivotButton': cell.pivotButton,
        'alignment': cell.alignment.__dict__,
        'merged_with': merged_cells_dict["merged_with"].get(cell_coords_pair, list()),
        'merged_to': merged_cells_dict["merged_to"].get(cell_coords_pair, None),
        'font': expand_attrs_dict(cell.font.__dict__, 'color'),
        'fill': {
            'bgColor': cell.fill.bgColor.__dict__,
            'fgColor': cell.fill.fgColor.__dict__,
        },
        'border': {
            'outline': cell.border.outline,
            'right': expand_attrs_dict(cell.border.right.__dict__, 'color'),
            'left': expand_attrs_dict(cell.border.left.__dict__, 'color'),
            'top': expand_attrs_dict(cell.border.top.__dict__, 'color'),
            'bottom': expand_attrs_dict(cell.border.bottom.__dict__, 'color'),
        },
    }

    if not deepdiff(d1=CELL_DEFAULT_META, d2=meta_dict):
        meta_dict = None
    #meta_dict = deepdiff(d1=XLSonHandler.cell_default_meta, d2=meta_dict)

    if jsonize:
        return json.dumps(meta_dict)
    else:
        return meta_dict


def fill_cell_meta(cell, meta_dict):
    # cell.data_type = meta_dict['data_type']  # TODO: write data_type compatibility with value check
    # cell.style_id = meta_dict['style_id']  # can't set it
    cell.pivotButton = meta_dict['pivotButton']
    cell.alignment = Alignment(**meta_dict['alignment'])
    if type(meta_dict['font']['color']) is dict:
        cell.font = Font(color=Color(**meta_dict['font']['color']),
                         **{k: v for k, v in meta_dict['font'].items() if k != 'color'})
    else:
        cell.font = Font(**meta_dict['font'])
    cell.fill = PatternFill(fgColor=Color(**meta_dict['fill']['fgColor']),
                            bgColor=Color(**meta_dict['fill']['bgColor']),
                            **{k: v for k, v in meta_dict['fill'].items() if k not in ('fgColor', 'bgColor')})
    # cell.border = Border(**meta_dict["border"])
    return cell
