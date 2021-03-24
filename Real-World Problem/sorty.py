my_list = [4,7,1,8,2,5,3,9,6]


def insertion_sort(seq):
    sorted_seq = [seq[0],]

    for right_num in seq[1:]:
        for i, left_num in enumerate(sorted_seq):

            if right_num < left_num:
                sorted_seq.insert(i, right_num)
            elif right_num > left_num:
                continue

    print(sorted_seq)


insertion_sort(my_list)


