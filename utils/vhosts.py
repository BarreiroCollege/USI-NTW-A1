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



# check if the header 'Host' exists in vhosts.conf
def host_exists(vhost_name):
    #this is a header

    with open("../vhosts.conf") as f:
        host_lines = f.readlines()

        for line in host_lines:
            current_line = line.split(",")
            current_name = current_line[0]
            if current_name == vhost_name:
                return True


def get_recource(vhost_name, resource_path):
    path = "../{}/{}".format(vhost_name,resource_path)
    try:
        with open(path) as f:
            return f
            

    except FileNotFoundError:
        return None
