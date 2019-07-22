from jsondler.json_tools import sort_dicts_list

from xlson import prepare_xl
from xlson.handlers import XLSonSheetHandler
from xlson.scheme import EntityInfo


def xl_to_html(xl_path, html_path, sheet_name=None):
    prep_xlson = prepare_xl(xl_path=xl_path)
    if sheet_name is not None:
        pass
    else:
        sheet_to_html(prep_xlson.main_sheet, html_path)


def sheet_to_html(xlson_sheet, html_path, ent_colors_dict=None, **kwargs):
    assert isinstance(xlson_sheet, XLSonSheetHandler), "ERROR: the value for argument 'xlson_sheet' should be " \
                                                       "an object of xlson.handlers.XLSonSheetHandler class"
    encoding = kwargs.get("encoding", "utf-8")
    html_f = open(html_path, 'w', encoding=encoding)
    html_f.write('<head>\n  <meta charset="%s">\n</head>\n' % encoding)
    if ent_colors_dict is not None:
        html_f.write(ent_colors_html(ent_colors_dict)+"\n")
    html_f.write('<table border="1" style="border-collapse: collapse; border: 1px solid black;">\n')
    data = xlson_sheet.data_df
    meta = xlson_sheet.meta_df
    EntityHandler=xlson_sheet.EntityHandler
    try:
        ents = xlson_sheet.entities
    except KeyError:
        ents = list()
    n_rows = len(data)
    n_cols = len(data[0])
    cell_ents_gen = entities_by_cells(sort_dicts_list(ents,
                                                      prior_list=[("*",)+EntityHandler.attr_scheme()["ent_loc_row"],
                                                                  ("*",)+EntityHandler.attr_scheme()["ent_loc_col"]]),
                                      EntityHandler=EntityHandler)
    cell_ents = next(cell_ents_gen)
    for i in range(n_rows):
        html_f.write("  <tr>\n")
        for j in range(n_cols):
            if meta[i][j]["merged_to"]:
                continue
            else:
                cell_data = None
                if i == cell_ents["row"] and j == cell_ents["col"] and ent_colors_dict is not None:
                    cell_data = get_colored_line(cell_data=str(data[i][j]),
                                                 spans_list=sort_dicts_list(
                                                     in_json=cell_ents["entities"],
                                                     prior_list=[("*",)+EntityHandler.attr_scheme()["ent_loc_start"]]
                                                 ),
                                                 EntityHandler=EntityHandler,
                                                 ent_colors_dict=ent_colors_dict)
                    try:
                        cell_ents = next(cell_ents_gen)
                    except StopIteration:
                        cell_ents = {"row": n_rows, "col": n_cols, "entities": []}
                else:
                    cell_data = str(data[i][j]) if data[i][j] else "    "
                if meta[i][j]["merged_with"]:
                    to_span = get_td_span(meta[i][j]["merged_with"])
                    html_f.write('    <td rowspan="%s" colspan="%s">%s</td>\n' % (str(to_span["rowspan"]),
                                                                                  str(to_span["colspan"]),
                                                                                  cell_data))
                else:
                    html_f.write('    <td>%s</td>\n' % cell_data)
        html_f.write("  </tr>\n")
    html_f.write('</table>\n')
    html_f.close()


def get_td_span(merged_with):
    curr_row = None
    max_col = 0
    rowspan = 1
    colspan = 1
    for coords in merged_with:
        if curr_row is None:
            curr_row = coords[0]
        if coords[1] > max_col:
            max_col = coords[1]
            colspan += 1
        if coords[0] > curr_row:
            curr_row = coords[0]
            rowspan += 1
    return {"rowspan": rowspan, "colspan": colspan}


def ent_colors_html(ent_colors_dict):
    html_tab_list = ['<table border="1" style="border-collapse: collapse; border: 1px solid black;">']
    for ent_type in ent_colors_dict:
        html_tab_list.append('  <tr>')
        html_tab_list.append('    <td><font style="color: %s">%s</font></td>' % (ent_colors_dict[ent_type], ent_type))
        html_tab_list.append('  </tr')
    html_tab_list.append('</table>\n')
    return "\n".join(html_tab_list)


def entities_by_cells(sorted_ents, EntityHandler):
    assert issubclass(EntityHandler, EntityInfo), "ERROR: the value for argument 'EntityHandler' should be a class " \
                                                  "inherited from xlson.sheme.EntityInfo"
    row = None
    col = None
    cell_ents_list = list()
    for ent_dict in sorted_ents:
        ent = EntityHandler.load_from_dict(ent_dict)
        if row is None:
            row = ent.ent_location.row
        if col is None:
            col = ent.ent_location.col
        if row != ent.ent_location.row or col != ent.ent_location.col:
            yield {"row": row, "col": col, "entities": cell_ents_list}
            row = ent.ent_location.row
            col = ent.ent_location.col
            cell_ents_list = list()
        cell_ents_list.append(ent.get_json())
    yield {"row": row, "col": col, "entities": cell_ents_list}


def get_colored_line(cell_data, spans_list, EntityHandler, ent_colors_dict):
    assert issubclass(EntityHandler, EntityInfo), "ERROR: the value for argument 'EntityHandler' should be a class " \
                                                  "inherited from xlson.sheme.EntityInfo"
    last_c = None
    line_list = list()
    for span_dict in spans_list:
        span = EntityHandler.load_from_dict(span_dict)
        l_s = span.ent_location.start
        l_e = span.ent_location.end
        if l_s is None or l_e is None:
            break
        if l_e == -1:
            l_e = len(cell_data)
        if last_c is not None:
            if l_s < last_c:
                continue
            if l_s - last_c >= 1:
                line_list.append(cell_data[last_c: l_s])
        elif l_s > 0:
            line_list.append(cell_data[:l_s])
        line_list.append('<font style="color: %s">%s</font>' % (ent_colors_dict[span.ent_type], cell_data[l_s: l_e]))
        if l_e == -1:
            break
        last_c = l_e
    if last_c != -1 and last_c < len(cell_data):
        line_list.append(cell_data[last_c:])
    return "".join(line_list)
