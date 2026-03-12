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
    for metadata in reader.iter_metadata():
        print(f"数据名称: {metadata.name}")
        print(f"数据大小: {len(metadata.metadata)} 字节")
        print(f"数据: {dumps_json(metadata.metadata)}")


def process_schemas(reader: McapReader):
    for schema, channel, message in reader.iter_messages():
        print(schema.name, schema.encoding, schema.id)
        print(channel.topic, channel.schema_id, channel.message_encoding, channel.id)
        print(
            message.log_time, message.publish_time, message.channel_id, message.sequence
        )


def main():
    print("Hello from mcap-viewer!")
    mcap_path = "/Users/shaozk/data/mcap/019a44db-f039-77e6-7eb3-82a84434c193.mcap"
    with open(mcap_path, "rb") as f:
        reader = make_reader(f)
        summary = reader.get_summary()
        print(summary)

        header = reader.get_header()
        print(header)

        # process_attachments(reader)
        # process_metadata(reader)
        process_schemas(reader)


if __name__ == "__main__":
    main()
