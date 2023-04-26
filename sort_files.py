import os

def sort_file_words_list(file_path):
    lines_dict = dict()

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            find_index = line.find('  ')
            if -1 != find_index:
                e_words = line[:find_index]
                lines_dict[e_words] = line
        f.close()

    sorted_items = sorted(lines_dict.items(), key=lambda x: x[0])

    with open(file_path, 'w', encoding='utf-8') as f:
        for item in sorted_items:
            f.write(item[1])
        f.close()

folder_path = 'vocabulary'
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        sort_file_words_list(file_path)
    