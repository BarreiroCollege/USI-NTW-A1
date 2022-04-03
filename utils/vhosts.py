class Vhost:
    @staticmethod
    def is_secure_path(path: str) -> bool:
        """
        Given a path, check if it is secure, i.e. does not go outside the virtual host filesystem
        :param path: path to be checked
        :return: True if path never leaves host folder
        """

        parts = path.split("/")
        level = 0
        for part in parts:
            # If an empty path is found (//) or a dot (/./), it means no change
            if part == '' or part == '.':
                continue
            # If "previous" path is found (/../), we substract one to the level
            elif part == '..':
                level -= 1
            # Otherwise, we increase by one the subfolder level
            else:
                level += 1

            # If we ever go outside this folder, return False
            if level < 0:
                return False
        # If we never left filesystem root folder, it is safe
        return True
