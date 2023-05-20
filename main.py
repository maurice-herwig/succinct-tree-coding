from succinct_tree_coding import Leave, OrderedTree, succinct_tree_coding

if __name__ == '__main__':
    # Compute the succinct tree coding for the example from Jurdzinski and Lazic.
    print(succinct_tree_coding(ordered_tree=OrderedTree(
        leaves={Leave([0, 0]), Leave([1, 0]), Leave([1, 1]), Leave([2, 0]),
                Leave([2, 1]), Leave([2, 2]), Leave([2, 3]),
                Leave([2, 4])})))

    # Compute the succinct tree coding of an own example.
    print(succinct_tree_coding(ordered_tree=OrderedTree(
        leaves={Leave([0, 0]), Leave([0, 1]), Leave([1]), Leave([2, 0]), Leave([2, 1]), Leave([2, 2]), Leave([2, 3]),
                Leave([2, 4])})))
