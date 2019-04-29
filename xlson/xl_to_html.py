from xlson import prepare_xl


def xlsx_to_html(xlsx_path, html_path, sheet_name=None):
    prep_new_xl = prepare_xl(xl_path=xlsx_path)
    if sheet_name is not None:
        pass
    else:
        prepsheet_to_html(prep_new_xl["main_sheet"], html_path)


def prepsheet_to_html(prep_sheet, html_path):
    html_f = open(html_path, 'w')
    html_f.write('<table border="1" style="border-collapse: collapse; border: 1px solid black;">\n')
    data = prep_sheet["main_sheet"]["data_df"]
    meta = prep_sheet["main_sheet"]["meta_df"]
    try:
        ents = prep_sheet["main_sheet"]["entities"]
    except KeyError:
        ents = list()
    n_rows = len(data)
    n_cols = len(data[0])
    #cell_ents_gen = entities_by_cells(ents)
    #cell_ents = next(cell_ents_gen)
    for i in range(n_rows):
        html_f.write("  <tr>\n")
        for j in range(n_cols):
            if meta[i][j]["merged_to"]:
                continue
            #if i == cell_ents["row"] and j == cell_ents["col"]:
            #    cell_data = get_colored_line(cell_data=str(data[i][j]),
            #                                 spans_list=sort_dicts_list(
            #                                     in_json=cell_ents["entities"],
            #                                     prior_list=[("*",)+SpanTemplate.location_start]
            #                                 ))
            #    try:
            #        cell_ents = next(cell_ents_gen)
            #    except StopIteration:
            #        cell_ents = {"row": n_rows, "col": n_cols, "entities": []}
            #else:
            cell_data = str(data[i][j]) if data[i][j] else "    "
            if meta[i][j]["merged_with"]:
                to_span = get_td_span(meta[i][j]["merged_with"])
                html_f.write('    <td rowspan="%s" colspan="%s">%s</td>\n' % (str(to_span["rowspan"]),
                                                                              str(to_span["colspan"]),
                                                                              cell_data))
            else:
                html_f.write('    <td>%s</td>\n' % cell_data)
        html_f.write(" </tr>\n")
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