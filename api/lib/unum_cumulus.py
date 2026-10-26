"""
The models Cumulus owns
"""

import sys

import relations
import relations_unifist

SOURCE = "cumulus"
UNIFIST = relations_unifist.UnifistBase.SOURCE


class Base(relations_unifist.UnifistModel):
    """
    Base class for Cumulus models, whose ids come from the Unifist source
    """

    SOURCE = SOURCE
    UNIFIST = UNIFIST


class Unifist(Base):
    """
    A person
    """

    id = str                    # slug of who
    version = int, 1            # Bumped with every change
    unum = str, False           # The unum of the id
    who = str                   # External id
    what = dict, False          # Whatever else is known
    unum_id = set               # The Unums this Unifist is in, through UnifistUnum

    SLUG = "who"


class Unum(Base):
    """
    A group
    """

    id = str                    # slug of who
    version = int, 1            # Bumped with every change
    unum = str, False           # The unum of the id
    who = str                   # External id
    what = dict, False          # Whatever else is known
    unifist_id = set            # The Unifists in this Unum, through UnifistUnum

    SLUG = "who"


class UnifistUnum(Base):
    """
    Which Unifists are in which Unums
    """

    id = str
    unifist_id = str            # The Unifist in the Unum
    unum_id = str               # The Unum the Unifist is in
    version = int, 1
    unum = str, False
    what = dict, False

    UNIQUE = ["unifist_id", "unum_id"]

relations.ManyToMany(Unifist, Unum, UnifistUnum)


class Entity(Base):
    """
    Stands in for a Unifist or a Unum so it can be the parent of everything else. It has an id of its own,
    like any model, and holds the id of the Unifist or Unum it stands for
    """

    id = str                    # slug of who and unifist_unum
    version = int, 1
    unum = str, False
    who = str                   # External id
    unifist_unum = ["unifist", "unum"]  # Which it stands for
    what = dict, False          # Holds the unifist_id or the unum_id it stands for

    SLUG = ["who", "unifist_unum"]

relations.OneToOne(Unifist, Entity, child_inject="what")
relations.OneToOne(Unum, Entity, child_inject="what")


class Scat(Base):
    """
    One raw problem, recorded as is
    """

    id = str
    version = int, 1
    unum = str, False
    entity_id = str                             # Who recorded it, not who owns it
    description = str                           # What happened
    when = relations_unifist.microseconds       # When it happened
    what = dict, False                          # Holds the flush_id and bucket_id, if any

    INDEX = "when"
    ORDER = "-when"

relations.OneToMany(Entity, Scat)


class Flush(Base):
    """
    The resolving of one or more Scats, and the record it leaves
    """

    id = str
    version = int, 1
    unum = str, False
    entity_id = str                             # Who flushed
    when = relations_unifist.microseconds       # When it was flushed
    what = dict, False                          # Holds the bucket_id, if flushed from a bucket

    INDEX = "when"
    ORDER = "-when"

relations.OneToMany(Entity, Flush)
relations.OneToMany(Flush, Scat, child_inject="what")


class Bucket(Base):
    """
    A named group for one kind of recurring Flush
    """

    id = str                    # slug of name
    version = int, 1
    unum = str, False
    name = str
    what = dict, False

    SLUG = "name"

relations.OneToMany(Bucket, Scat, child_inject="what")
relations.OneToMany(Bucket, Flush, child_inject="what")


def models():
    """
    The Cumulus models, and the Sequence, Slug and Journal tables they take their ids and journal from
    """

    return (
        relations.models(relations_unifist, relations_unifist.UnifistBase) +
        relations.models(sys.modules[__name__], Base)
    )
