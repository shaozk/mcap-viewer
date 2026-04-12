import os

import dearpygui.dearpygui as dpg
from mcap.reader import McapReader, make_reader

from mcap_viewer.core.recent_manager import RecentFilesManager


class Application:
    def __init__(self):
        self.recent_manager = RecentFilesManager()
        self.recent_items = []
        self.recent_menu_tag = None
        self.current_file = None
        self.reader = None

        # settings
        self.metadata_tag = "metadata_tag"
        self.metadata_group_tag = "metadata_group_tag"
        self.metadata_items = []

    def setup_menu(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open", callback=self.open_file)
                with dpg.menu(label="Open Recent"):
                    with dpg.group(id="recent_files_group"):
                        self.update_recent_menu()

            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About")

    def setup_settings(self):
        with dpg.window(label="Settings", width=400, height=960, pos=(0, 0)):
            with dpg.tab_bar():
                with dpg.tab(label="Panel"):
                    dpg.add_text("panel page")
                with dpg.tab(label="Topics"):
                    dpg.add_text("topics page")
                with dpg.tab(label="Metadata", tag=self.metadata_tag):
                    with dpg.group(tag=self.metadata_group_tag):
                        pass
                with dpg.tab(label="Attachments"):
                    dpg.add_text("Attachments page")
                with dpg.tab(label="Source Info"):
                    dpg.add_text("panel page")

    def open_file(self):
        with dpg.file_dialog(
            directory_selector=False,
            callback=self.on_file_selected,
            id="file_dialog_id",
            width=700,
            height=400,
        ):
            dpg.add_file_extension(".mcap", color=(150, 255, 150, 255))

    def open_recent_file(self, sender, app_data, user_data):
        filepath = user_data
        if os.path.exists(filepath):
            self.load_file(filepath)
        else:
            dpg.add_info_toast(
                title="file not exist",
                message=f"file {filepath} removed or delted",
                duration=3,
            )
            recent_files = self.recent_manager.get()
            if filepath in recent_files:
                recent_files.remove(filepath)
                for i, f in enumerate(recent_files):
                    self.recent_manager.recent_files = recent_files
                    self.recent_manager.save()
                self.update_recent_menu()

    def load_file(self, filepath):
        print(f"filepath: {filepath}")
        with open(filepath, "rb") as reader:
            self.reader = make_reader(reader)
            self.load_settings(self.reader)

    def on_file_selected(self, sender, app_data):
        print(app_data)
        filepath = app_data["file_path_name"]
        self.recent_manager.add_file(filepath)
        self.update_recent_menu()

    def update_recent_menu(self):
        for item in self.recent_items:
            dpg.delete_item(item)
        self.recent_items.clear()

        recent_files = self.recent_manager.get()

        if not recent_files:
            dpg.add_menu_item(
                label="(empty)", enabled=False, parent=self.recent_menu_tag
            )
        else:
            for filepath in recent_files:
                filename = os.path.basename(filepath)
                item = dpg.add_menu_item(
                    label=f"{filename}",
                    callback=self.open_recent_file,
                    user_data=filepath,
                    parent="recent_files_group",
                )
                self.recent_items.append(item)

            # dpg.add_separator(parent=self.recent_menu_tag)
            # clear_item = dpg.add_menu_item(
            #    label="clear",
            #    callback=self.clear_recent_files,
            #    parent=self.recent_menu_tag,
            # )
            # self.recent_items.append(clear_item)
            print(f"recent len: {len(self.recent_items)}")

    def clear_recent_files(self):
        self.recent_manager.clear()
        self.update_recent_menu()
        dpg.add_info_toast(
            title="cleared", message="recent file list cleared", duration=2
        )

    def load_settings(self, reader: McapReader):
        if dpg.does_item_exist(self.metadata_group_tag):
            dpg.delete_item(self.metadata_group_tag, children_only=True)
        for item in self.metadata_items:
            self.metadata_items.clear()
        for index, metadata in enumerate(reader.iter_metadata()):
            print(f"index: {index}")
            print(f"数据名称: {metadata.name}")
            print(f"数据大小: {len(metadata.metadata)} 字节")
            item = dpg.add_tree_node(
                label=metadata.name, parent=self.metadata_group_tag
            )
            for key, value in metadata.metadata.items():
                dpg.add_text(f"{key}:{value}", parent=item)

            self.metadata_items.append(item)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title="mcap-viewer", width=1200, height=960)
        self.setup_menu()
        self.setup_settings()

        # with dpg.window(label="Data Source Info", width=1200, height=960):
        #     with dpg.table(header_row=True, width=400, height=960, pos=(400, 0)):
        #         # use add_table_column to add columns to the table,
        #         # table columns use slot 0
        #         dpg.add_table_column(label="Topic Name")
        #         dpg.add_table_column(label="Datatype")
        #         dpg.add_table_column(label="Message count")
        #         dpg.add_table_column(label="Frequency")

        #         # add_table_next_column will jump to the next row
        #         # once it reaches the end of the columns
        #         # table next column use slot 1
        #         for i in range(0, 4):
        #             with dpg.table_row():
        #                 for j in range(0, 5):
        #                     dpg.add_text(f"Row{i} Column{j}")

        self.update_recent_menu()

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == "__main__":
    app = Application()
    app.run()
