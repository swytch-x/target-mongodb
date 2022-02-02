"""MongoDB target stream class, which handles writing streams."""

from typing import Any, Dict, List, Tuple, Union

from singer_sdk.sinks import BatchSink

import requests
import urllib.parse

import pymongo
ß
class MongoDbSink(BatchSink):
    """MongoDB target sink class."""

    max_size = 10

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written."""
        # The SDK populates `context["records"]` automatically
        # since we do not override `process_record()`.

        # get connection configs
        connection_string = self.config.get("connection_string")
        db_name = self.config.get("db_name")
        # set the collection based on current stream
        collection = urllib.parse.quote(self.stream_name)

        client = pymongo.MongoClient(connection_string, connectTimeoutMS=2000, retryWrites=True)
        db = client[db_name]

        records = context["records"]

        db[collection].insert_many(records)

        self.logger.info(f"Uploaded {len(records)} records into {collection}")


        # Clean up records
        context["records"] = []
