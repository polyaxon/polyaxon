class InitCommands(object):
    COPY = 'copy'
    CREATE = 'create'
    DELETE = 'delete'

    @classmethod
    def is_copy(cls, command):
        return command == cls.COPY

    @classmethod
    def is_create(cls, command):
        return command == cls.CREATE

    @classmethod
    def is_delete(cls, command):
        return command == cls.DELETE


def get_output_args(command, outputs_path, original_outputs_path=None):
    get_or_create = 'if [ ! -d "{dir}" ]; then mkdir -p {dir}; fi;'.format(dir=outputs_path)
    delete_dir = 'if [ -d {path} ]; then rm -r {path}; fi;'.format(path=outputs_path)
    copy_file_if_exist = 'if [ -f {original_path} ]; then cp {original_path} {path}; fi;'.format(
        original_path=original_outputs_path, path=outputs_path)
    copy_dir_if_exist = 'if [ -d {original_path} ]; then cp -r {original_path} {path}; fi;'.format(
        original_path=original_outputs_path, path=outputs_path)
    if InitCommands.is_create(command=command):
        return '{} {}'.format(get_or_create, delete_dir)
    if InitCommands.is_copy(command=command):
        return '{} {} {} {}'.format(
            get_or_create, delete_dir, copy_dir_if_exist, copy_file_if_exist)
    if InitCommands.is_delete(command=command):
        return '{}'.format(delete_dir)
