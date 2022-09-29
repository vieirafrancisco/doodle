import os
import re
import time
import requests
from pprint import pprint

from bs4.element import Tag

from sunflower.settings import logging, session


def search_category(item):
    regex = re.search(r"br/(.+)\/l\/(.+)\/", item["href"])
    if regex is not None:
        return {"name": regex.group(1), "initials": regex.group(2), "parent": None}
    regex = re.search(r"br/(.+)\/(.+)\/s\/(.+)\/(.+)\/", item["href"])
    if regex is not None:
        parent = {"name": regex.group(2), "initials": regex.group(3)}
        return {"name": regex.group(1), "initials": regex.group(4), "parent": parent}
    return tuple()


def update_state(state, d):
    tmp_state = state.copy()
    for key, value in d.items():
        if key not in tmp_state.keys():
            tmp_state[key] = list()
        if isinstance(value, list):
            for x in value:
                tmp_state[key].append(x)
        else:
            tmp_state[key].append(value)
    return tmp_state


def tree(tag):
    if not isinstance(tag, Tag):
        return {}
    contents = list(tag.contents)
    if len(contents) == 0:
        return {}
    value = contents[0]
    state = {}
    if value != " ":
        key = tag.get("class") or tag.name
        if tag.get("class") is not None:
            key = key[0]
        return {key: (value, tag.get("style", ""))}

    for content in contents:
        if isinstance(content, Tag):
            result = tree(content)
            state = update_state(state, result)
    return state
