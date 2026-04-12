from pathlib import Path

from mcap.reader import McapReader, make_reader

from mcap_viewer.utils.json_util import dumps_json


def process_attachments(reader: McapReader):
    for attachment in reader.iter_attachments():
        print(f"附件名称: {attachment.name}")
        print(f"媒体类型: {attachment.media_type}")
        print(f"数据大小: {len(attachment.data)} 字节")
        file_path = Path(attachment.name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        with open(f"{attachment.name}", "wb") as output_file:
            output_file.write(attachment.data)


def process_metadata(reader: McapReader):
    for index, metadata in enumerate(reader.iter_metadata()):
        print(f"index: {index}")
        print(f"数据名称: {metadata.name}")
        print(f"数据大小: {len(metadata.metadata)} 字节")
        print(f"数据: {dumps_json(metadata.metadata)}")


def process_schemas(reader: McapReader):
    for schema, channel, message in reader.iter_messages():
        # print(schema.name, schema.encoding, schema.id)
        print(channel.topic, channel.schema_id, channel.message_encoding, channel.id)
        # print(
        #     message.log_time, message.publish_time, message.channel_id, message.sequence
        # )


def print_statistics(stat):
    print(f"attachment_count: {stat.attachment_count}")
    print(f"channel_count: {stat.channel_count}")
    print(f"chunk_count: {stat.chunk_count}")
    print(f"message_count: {stat.message_count}")
    print(f"message_start_time : {stat.message_start_time}")
    print(f"message_end_time: {stat.message_end_time}")
    print(f"metadata_count: {stat.metadata_count}")
    print(f"schema_count: {stat.schema_count}")
    for id, count in stat.channel_message_counts.items():
        print(f"channel {id}: {count}")


def print_channels(channels):
    for id, channel in channels.items():
        print(f"== id: {id} ==")
        print(f"id: {channel.id}")
        print(f"topic: {channel.topic}")
        print(f"message_encoding: {channel.message_encoding}")
        print(f"metadata: {channel.metadata}")
        print(f"schema_id: {channel.schema_id}")


def print_schemas(schemas):
    for id, schema in schemas.items():
        print(f"== id: {id} ==")
        print(f"id: {schema.id}")
        print(f"data: {schema.data}")
        print(f"encoding: {schema.encoding}")
        print(f"name: {schema.name}")


def print_chunk_indexs(chunk_indexes):
    for index, ci in enumerate(chunk_indexes):
        print(f"== {index} ==")
        print(f"chunk_length: {ci.chunk_length}")
        print(f"chunk_start_offset: {ci.chunk_start_offset}")
        print(f"compression: {ci.compression}")
        print(f"compressed_size: {ci.compressed_size}")
        print(f"message_end_time: {ci.message_end_time}")
        print(f"message_index_length: {ci.message_index_length}")
        print(f"message_index_offsets: {ci.message_index_offsets}")
        print(f"message_start_time: {ci.message_start_time}")
        print(f"uncompressed_size: {ci.uncompressed_size}")


def print_summary(reader):
    summary = reader.get_summary()
    # print_statistics(summary.statistics)  # print(summary.channels)
    # print_channels(summary.channels)
    # print_schemas(summary.schemas)
    print_chunk_indexs(summary.chunk_indexes)
    # print(summary.schemas)
    # for schema, channel, message in reader.iter_messages():
    #    print(f"{channel.topic} ({schema.name})")


def main():
    print("Hello from mcap-viewer!")
    mcap_path = "/Users/shaozk/data/mcap/019a44db-f039-77e6-7eb3-82a84434c193.mcap"
    with open(mcap_path, "rb") as f:
        reader = make_reader(f)

        # process_attachments(reader)
        process_metadata(reader)
        # process_schemas(reader)


if __name__ == "__main__":
    main()
