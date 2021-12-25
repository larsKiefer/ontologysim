import os
import inspect

import sys


class PathTest:
    """
    Tests the given paths
    """
    current_main_dir = ""

    @classmethod
    def check_file_path_current_dir_given(cls, path, current_dir):
        """
        check file without current_main_dir
        :param path:
        :param current_dir:
        :return: string path
        """
        if os.path.isfile(path):
            full_path = path
            return full_path

        file_not_found = True

        while file_not_found:
            full_path = current_dir + path

            if not os.path.isfile(full_path):
                last_current_dir = current_dir
                current_dir = os.path.dirname(current_dir)

                if current_dir == last_current_dir:
                    raise Exception("path not found", path)
            else:
                file_not_found = False

        return full_path


    @classmethod
    def check_file_path(cls, path):
        """
        transform a relative path to a full path

        :param path: path
        :return: full_path
        """
        current_dir = PathTest.current_main_dir
        return cls.check_file_path_current_dir_given(path,current_dir)

    @classmethod
    def check_dir_path_current_dir_given(cls,path,current_dir):
        """

        :param path:
        :param current_dir:
        :return:
        """

        head, tail = os.path.split(path)
        if os.path.isdir(head):
            full_path = path
            return full_path

        file_not_found = True
        while file_not_found:
            full_path = current_dir + head

            if not os.path.isdir(full_path):
                last_current_dir = current_dir
                current_dir = os.path.dirname(current_dir)
                if current_dir == last_current_dir:
                    raise Exception("path not found", path)
            else:
                file_not_found = False

        return full_path + "/" + tail

    @classmethod
    def check_dir_path(cls, path):
        """
        transform a relative path of a dir to a full path

        :param path: path
        :return: full_path
        """
        current_dir = PathTest.current_main_dir
        return cls.check_dir_path_current_dir_given(path,current_dir)

    @classmethod
    def create_new_folder(self, path, folder_name):
        """
        creates a new folder

        :param path: str
        :param folder_name: str
        :return: full path
        """
        newpath_queue = path + folder_name + "/"
        if not os.path.exists(newpath_queue):
            os.makedirs(newpath_queue)
        path_folder = PathTest.check_dir_path(newpath_queue)
        return path_folder