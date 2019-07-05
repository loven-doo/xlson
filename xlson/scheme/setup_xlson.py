from functools import reduce
from operator import getitem

from jsondler import JsonEntry


class XLSonScheme(JsonEntry):

    # json keys
    main_sheet_key = "main_sheet"
    supp_sheets_key = "supp_sheets"
    source_path_key = "source_path"

    # default values
    main_sheet_0 = dict()
    supp_sheets_0 = list()
    source_path_0 = None

    def __init__(self, main_sheet=None, supp_sheets=None, source_path=source_path_0):
        if main_sheet is None:
            main_sheet = self.main_sheet_0
        if supp_sheets is None:
            supp_sheets = self.supp_sheets_0

        self.main_sheet = main_sheet
        self.supp_sheets = supp_sheets
        self.source_path = source_path

    @classmethod
    def attr_scheme(cls):
        """
        json scheme (the keys must match attribute names defined in __init__)
        CAUTION: if attribute is not defined in __init__ method (sublevel key in a json)
            don't include it to the result dict
        :return: {attr_name: (path, in, json, entry,), ...}
        """
        return {
            "main_sheet": (cls.main_sheet_key,),
            "supp_sheets": (cls.supp_sheets_key,),
            "source_path": (cls.source_path_key,),
        }


class XLSonSheetScheme(JsonEntry):

    # json keys
    data_df_key = "data_df"
    meta_df_key = "meta_df"
    entites_key = "entities"
    supp_sheets_key = XLSonScheme.supp_sheets_key
    cell_default_meta_key = "cell_default_meta"
    sheet_name_key = "sheet_name"

    # default values
    data_df_0 = list()
    meta_df_0 = list()
    entites_0 = list()
    cell_default_meta_0 = dict()
    supp_sheets_0 = list()
    sheet_name_0 = None

    main_sheet = False

    def __init__(self,
                 data_df=None,
                 meta_df=None,
                 entities=None,
                 cell_default_meta=None,
                 sheet_name=sheet_name_0,
                 **kwargs):

        if data_df is None:
            data_df = self.data_df_0
        if meta_df is None:
            meta_df = self.meta_df_0
        if entities is None:
            entities = self.entites_0
        if cell_default_meta is None:
            cell_default_meta = self.cell_default_meta_0

        self.data_df = data_df
        self.meta_df = meta_df
        self.entities = entities
        self.cell_default_meta = cell_default_meta
        self._sheet_name = sheet_name

        if self.main_sheet:
            self.supp_sheets = kwargs.get("supp_sheets", self.supp_sheets_0)

    @classmethod
    def attr_scheme(cls):
        """
        json scheme (the keys must match attribute names defined in __init__)
        CAUTION: if attribute is not defined in __init__ method (sublevel key in a json)
            don't include it to the result dict
        :return: {attr_name: (path, in, json, entry,), ...}
        """
        attr_scheme = {
            "data_df": (cls.data_df_key,),
            "meta_df": (cls.meta_df_key,),
            "entities": (cls.entites_key,),
            "cell_default_meta": (cls.cell_default_meta_key,),
            "_sheet_name": (cls.sheet_name_key,),
        }

        if cls.main_sheet:
            attr_scheme["supp_sheets"] = (cls.supp_sheets_key,)
        return attr_scheme

    def get_json(self):
        got_json = super(XLSonSheetScheme, self).get_json()
        if self.main_sheet:
            supp_sheets_path = (self.supp_sheets_key,)  # WARNING: duplication
            reduce(getitem, supp_sheets_path[:-1], got_json)[supp_sheets_path[-1]] = self.supp_sheets
        return got_json


class EntityInfo(JsonEntry):

    # json keys
    id_key = "id"
    type_key = "type"
    location_key = "location"
    content_key = "content"
    row_key = "row"
    col_key = "col"
    start_key = "start"
    end_key = "end"
    content_full_key = "full"
    other_cells_key = "other_cells"

    # default values
    ent_id_0 = int()
    ent_type_0 = None
    ent_content_full_0 = None,
    ent_content_start_0 = 0,
    ent_content_end_0 = -1,
    ent_loc_row_0 = int(),
    ent_loc_col_0 = int(),
    ent_loc_start_0 = 0,
    ent_loc_end_0 = -1,
    ent_loc_other_cells_0 = None

    additional_attrs = list()

    def __init__(self,
                 ent_id=ent_id_0,
                 ent_type=ent_type_0,
                 ent_content_full=ent_content_full_0,
                 ent_content_start=ent_content_start_0,
                 ent_content_end=ent_content_end_0,
                 ent_loc_row=ent_loc_row_0,
                 ent_loc_col=ent_loc_col_0,
                 ent_loc_start=ent_loc_start_0,
                 ent_loc_end=ent_loc_end_0,
                 ent_loc_other_cells=ent_loc_other_cells_0,
                 **kwargs):

        self.ent_id = ent_id
        self.ent_type = ent_type
        self.ent_content_full = ent_content_full
        self.ent_content_start = ent_content_start
        self.ent_content_end = ent_content_end
        self.ent_loc_row = ent_loc_row
        self.ent_loc_col = ent_loc_col
        self.ent_loc_start = ent_loc_start
        self.ent_loc_end = ent_loc_end
        self.ent_loc_other_cells = ent_loc_other_cells

        used_attrs = list(self.__dict__.keys())
        for attr in kwargs:
            if attr not in used_attrs:
                self.__dict__[attr] = kwargs[attr]
                used_attrs.append(attr)
                if attr not in self.additional_attrs:
                    self.additional_attrs.append(attr)
        for attr in self.additional_attrs:
            if attr not in used_attrs:
                self.__dict__[attr] = None
                used_attrs.append(attr)

    def __getitem__(self, item):
        return self.get_json()[item]

    def __setitem__(self, key, value):
        got_json = self.get_json()
        got_json[key] = value
        self.__dict__ = self.load_from_dict(got_json).__dict__

    @classmethod
    def attr_scheme(cls):
        """
        json scheme (the keys must match attribute names defined in __init__)
        CAUTION: if attribute is not defined in __init__ method (sublevel key in a json)
            don't include it to the result dict
        :return: {attr_name: (path, in, json, entry,), ...}
        """
        attr_scheme = {
            "ent_id": (cls.id_key,),
            "ent_type": (cls.type_key,),
            "ent_content_full": (cls.content_key, cls.content_full_key),
            "ent_content_start": (cls.content_key, cls.start_key),
            "ent_content_end": (cls.content_key, cls.end_key),
            "ent_loc_row": (cls.location_key, cls.row_key),
            "ent_loc_col": (cls.location_key, cls.col_key),
            "ent_loc_start": (cls.location_key, cls.start_key),
            "ent_loc_end": (cls.location_key, cls.end_key),
            "ent_loc_other_cells": (cls.location_key, cls.other_cells_key),
        }

        attr_scheme.update({attr: (attr,) for attr in cls.additional_attrs})
        return attr_scheme

    @property
    def ent_content(self):
        return EntityContent(self)

    @property
    def ent_location(self):
        return EntityLocation(self)


class EntityContent(object):

    def __init__(self, entity_info):
        assert isinstance(entity_info, EntityInfo)
        self._entity_info = entity_info

    @property
    def full(self):
        return self._entity_info.ent_content_full

    @full.setter
    def full(self, value):
        self._entity_info.ent_content_full = value

    @property
    def start(self):
        return self._entity_info.ent_content_start

    @start.setter
    def start(self, value):
        self._entity_info.ent_content_start = value

    @property
    def end(self):
        return self._entity_info.ent_content_end

    @end.setter
    def end(self, value):
        self._entity_info.ent_content_end = value


class EntityLocation(object):

    def __init__(self, entity_info):
        assert isinstance(entity_info, EntityInfo)
        self._entity_info = entity_info

    @property
    def row(self):
        return self._entity_info.ent_loc_row

    @row.setter
    def row(self, value):
        self._entity_info.ent_loc_row = value

    @property
    def col(self):
        return self._entity_info.ent_loc_col

    @col.setter
    def col(self, value):
        self._entity_info.ent_loc_col = value

    @property
    def start(self):
        return self._entity_info.ent_loc_start

    @start.setter
    def start(self, value):
        self._entity_info.ent_loc_start = value

    @property
    def end(self):
        return self._entity_info.ent_loc_end

    @end.setter
    def end(self, value):
        self._entity_info.ent_loc_end = value

    @property
    def other_cells(self):
        return self._entity_info.ent_loc_other_cells

    @other_cells.setter
    def other_cells(self, value):
        self._entity_info.ent_loc_other_cells = value
