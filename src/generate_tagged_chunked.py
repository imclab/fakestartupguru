#!/usr/bin/env python

from __future__ import division

import os
import sys
import nltk
import pprint
import cPickle as pickle

from settings import Settings
import models
from ProcessedText import ProcessedText

# -----------------------------------------------------------------------------
#   Constants.
# -----------------------------------------------------------------------------
APP_NAME = "generate_tagged_chunked"
LOG_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, "logs"))
LOG_FILEPATH = os.path.abspath(os.path.join(LOG_PATH, "%s.log" % APP_NAME))
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
#   Logging.
# -----------------------------------------------------------------------------
import logging
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
# -----------------------------------------------------------------------------

def get_processed_biographies(settings, refresh=False):
    logger = logging.getLogger("%s.get_processed_biographies" % APP_NAME)
    logger.debug("entry.")

    # -------------------------------------------------------------------------
    #   If we already have the data available in the pickle then load it;
    #   this takes a long time to do.
    # -------------------------------------------------------------------------
    if refresh == False and os.path.isfile(settings.analyzer_tagged_chunked_filepath):
        logger.debug("Pickled data is available here: '%s'" % settings.analyzer_tagged_chunked_filepath)
        with open(settings.analyzer_tagged_chunked_filepath, "rb") as f_in:
            return pickle.load(f_in)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    #   Get all Officials with available biographies.
    #
    #   Use execute().iterator() to iterate without caching models, using
    #   less memory for large result sets (from peewee cookbook).
    # -------------------------------------------------------------------------
    officials = [official for official in models.Official.select().execute().iterator()
                 if official.bio_text is not None and
                    len(official.bio_text) > 0]
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    #   Process all the biographies for all officials.
    # -------------------------------------------------------------------------
    #processed_biographies = [ProcessedText(official) for official in officials]
    processed_biographies = [ProcessedText(official) for official in officials]
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    #   Persist the processed biographies.
    # -------------------------------------------------------------------------
    with open(settings.analyzer_tagged_chunked_filepath, "wb") as f_out:
        pickle.dump(processed_biographies, f_out, pickle.HIGHEST_PROTOCOL)
    # -------------------------------------------------------------------------

    return processed_biographies

def main():
    logger = logging.getLogger("%s.main" % APP_NAME)
    logger.debug("entry.")

    settings = Settings()

    # -------------------------------------------------------------------------
    #   Load processed biographies. This is a list of ProcessedText objects.
    # -------------------------------------------------------------------------
    processed_biographies = get_processed_biographies(settings, refresh=True)
    #processed_biographies = get_processed_biographies(settings)
    # -------------------------------------------------------------------------

if __name__ == "__main__":
    main()