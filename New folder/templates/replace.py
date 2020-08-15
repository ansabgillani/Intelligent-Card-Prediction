ff = input()

for filename in ff.split(' '):
    file = open(filename)

    output = file.read()
    output = output.split(">")
    replacements = ["href=", "src="]

    for i in range(0, len(output)):
        for replacement in replacements:
            if replacement in output[i]:
                split_line = output[i].split('"')
                for j in range(0, len(split_line)):
                    if replacement in split_line[j]:
                        to_replace = split_line[j+1]
                        break
                if 'html' not in to_replace and \
                        '#' not in to_replace and \
                        'javascript' not in to_replace and \
                        '' != to_replace:
                    output[i] = output[i].replace(to_replace, "{{ url_for('static', filename='"+to_replace+"') }}")

    result = ">".join(output)

    file.close()

    file2 = open(filename, 'w')
    file2.write(result)

    file2.close()
