import os
import constant
import re
class Utils:

    file_name = None
    directory = None
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.directory = os.getcwd()
    
    def _get_directory(self):
        print('directory: ', self.directory)
        return self.directory

    def _create_new_directory(self):
        return os.path.join(self.directory, constant.COM_PATH)

    def _write_new_line(self, port= "", content = ""):
        file_name = "Sample.txt"
        com_path = self._create_new_directory()
        file_path = os.path.join(com_path, file_name)

        if not os.path.exists(com_path):
            os.makedirs(com_path)
        if not os.path.isfile(file_path):
            with open(file_path, 'w+') as f:
                f.write(content)
                f.write('\n')
        else:
            with open(file_path, 'a') as f:
                f.write(content)
                f.write('\n')
    
    """
        COM, Date, Sender, Content -- structure content sms
        Save in sms.txt
    """
    def write_sms_to_file(self, port, phone_number, content = []):
        #find directory save sms file
        _path = self._get_directory()
        _file_path = os.path.join(_path, self.file_name)
        # structure content 
        list_content = []
        print('list content', content)
        for iterator in content:
            _content = iterator.decode()
            group = None
            try:
                group = re.match('(.*),"(.*)","(.*)","","(.*)"*?","(.*)"',_content).groups()
            except:
                print("No content")
            print('group',group)
            if(group != None):
                list_content.append((port, phone_number, group))
        
        if not os.path.isfile(_file_path):
            with open(_file_path, 'w+') as f:
                for x in list_content:
                    f.write(''.join('{}\t{}\t{}\t{} {}\n'.format(x[0], x[1], x[2][2], x[2][3], x[2][4])))
                    f.close()
        else:
            with open(_file_path, 'a') as f:
                for x in list_content:
                    f.write(''.join('{}\t{}\t{}\t{} {}\n'.format(x[0], x[1], x[2][2], x[2][3], x[2][4])))
                    f.close()
        #         f.write('\n'.join('{}\t{} {}\n'.format(x[2],x[3],x[4]) for x in list_content))
    """
        Read file 
    """
    def _read_file(self):
        com_path = self._create_new_directory()
        file_path = os.path.join(com_path, "Sample.txt")
        with open(file_path, 'r') as f:
            print(f.read())
