import js7

client = js7.Client(
    http_config=js7.model.HTTPConfiguration(
        host="192.168.1.1",
        port=4446
    ),
    auth_config=js7.model.AuthConfiguration(
        basic_auth=js7.model.BasicAuth(
            username="root",
            password="root"
        )
    )
)

client.inventory.manage.import_configurations(
    file_path="/path/to/file/or/folder",
    inventory_target_folder="/test-folder"
)
