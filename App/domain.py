from collections import namedtuple
import data_controler as data

Movement = namedtuple("movement", "date, amount, concept, tag")

def movent_to_txt(m: Movement):
    return f"\"{m.date}\", \"{m.concept}\", {m.amount}, {m.tag}"

