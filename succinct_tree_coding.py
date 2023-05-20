class OrderedTree:
    def __init__(self, leaves: set):
        """
        Init a new the Ordered Tree object.
        :param leaves: A set of Leaves that contains all the leaves in the tree.
        """
        self.leaves = leaves

    def __repr__(self):
        return f'OrderedTree with the leaves: {str(self.leaves)}'

    def __len__(self):
        return len(self.leaves)

    def get_leaves(self):
        return self.leaves

    def get_branching_directions_root(self):
        """
        Compute and return all branching directions from the root of the tree.
        :return: A set of directions.
        """
        return {leave.get_first_branching_direction() for leave in self.leaves if leave}

    def get_subtree(self, branching_directions: set):
        """
        Create a new tree containing only the leaves that have a given branching direction as a prefix.
        :param branching_directions: A set of directions.
        :return: OrderedTree.
        """
        return OrderedTree(leaves={leave for leave in self.leaves
                                   if leave.get_first_branching_direction() in branching_directions})

    def difference(self, other):
        """
        Create a new tree containing only the leaves not contained in the other OrderedTree.
        :param other: OrderedTree.
        :return: OrderedTree.
        """
        return OrderedTree(leaves=self.get_leaves().difference(other.get_leaves()))

    def union(self, other):
        """
        Generate a new OrderedTree containing as leaves the union of the leaves sets of self and other.
        :param other: OrderedTree.
        :return: OrderedTree.
        """
        return OrderedTree(leaves=self.get_leaves().union(other.get_leaves()))

    def step_down(self):
        """
        Create a new OrderedTree that removes the first branching direction of each leaf.
        :return: OrderedTree.
        """
        return OrderedTree(leaves={leave.step_down() for leave in self.get_leaves()})


class Leave:
    def __init__(self, navigation_path: list):
        """
        Init a new Leave object.
        :param navigation_path: list of objects comparable with the '<' operator, such as integers or strings.
        """
        self.navigation_path = navigation_path

    def __repr__(self):
        return str(self.navigation_path)

    def __len__(self):
        return len(self.navigation_path)

    def get_first_branching_direction(self):
        """
        Get the first branching direction of the navigation path.
        :return: direction.
        """
        return self.navigation_path[0] if len(self.navigation_path) > 0 else None

    def step_down(self):
        """
        Create a new one that removes the first branching direction of the navigation path of this leave.
        :return: Leave
        """
        return Leave(navigation_path=self.navigation_path[1::])

    def add_prefix(self, prefix: list):
        """
        Add a prefix to the own navigation path.
        :param prefix: direction
        :return: Leave
        """
        return Leave(navigation_path=prefix + self.navigation_path)


def succinct_tree_coding(ordered_tree: OrderedTree) -> dict:
    """
    Compute a succinct tree coding for a given ordered tree using the method of Jurdzinski and Lazic published in
    'Succinct progress measures for solving parity games'
    (https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8005092).
    A succinct tree coding maps every leave of an ordered tree of height h and with at most l leaves
    to a '(log_2 l)-bounded adaptive i-counter'.
    :param ordered_tree: OrderedTree
    :return: Dictionary: leave -> decoded as '(log_2 l)-bounded adaptive i-counter'
    """

    def __aux(a: str, b: list):
        """
        A small auxiliary function to add a prefix to the first element of a
        'g-bounded adaptive i-counter' decoded as a list.
        :param a: str: prefix.
        :param b: list: 'g-bounded adaptive i-counter'.
        :return: list: 'g-bounded adaptive i-counter' with the prefix.
        """
        if len(b) == 0:
            return [a]

        b[0] = a + b[0]
        return b

    # Get the number of leaves and a list with all branching directions.
    number_of_leaves = len(ordered_tree)
    branching_directions = list(ordered_tree.get_branching_directions_root())

    # If we have an empty tree, we can return an empty dictionary, to which we can add the other codes.
    if number_of_leaves == 0:
        return {}

    # If we only have one node, we don't need to choose a branching direction, because we have at most one direction.
    elif number_of_leaves == 1:

        # If we have no branching direction, this means that the navigation path of the only left leave is empty,
        # and we can return the leave with no code.
        if len(branching_directions) == 0:
            return {ordered_tree.get_leaves().pop(): []}
        else:
            # Otherwise, we need to step down the only left navigation path, this can we decode with
            # epsilon (unicode: \u03B5).
            return {ordered_tree.get_leaves().pop(): ["\u03B5"] + v for v in
                    succinct_tree_coding(ordered_tree=ordered_tree.step_down()).values()}

    # Choose a branching direction M and compute the subtrees l_< and l_>  as well l_m.
    # we set the first element of the branching_directions list as the first branching direction and compute the
    # corresponding subtrees.
    i = 0
    l_smaller = OrderedTree(leaves=set())
    l_m = ordered_tree.get_subtree(branching_directions={branching_directions[i]})
    l_bigger = ordered_tree.difference(other=l_m)

    # Iterate over the branching direction until we find one that satisfies our conditions.
    # It is easy to prove that we can always find a branching direction that satisfies this.
    while len(l_smaller) > (number_of_leaves / 2) or len(l_bigger) > (number_of_leaves / 2):
        # If the last branching direction does not satisfy the conditions,
        # update the branching direction and the subtrees.
        l_smaller = l_smaller.union(other=l_m)
        i += 1
        l_m = ordered_tree.get_subtree(branching_directions={branching_directions[i]})
        l_bigger = l_bigger.difference(other=l_m)

    # Call succinct_tree_coding recursively for all computed subtrees and add the appropriate prefixes to each result.
    # Finally, merge the three results.
    return {k: __aux("0", v) for k, v in succinct_tree_coding(ordered_tree=l_smaller).items()} | \
        {k.add_prefix([branching_directions[i]]): ["\u03B5"] + v for k, v in
         succinct_tree_coding(ordered_tree=l_m.step_down()).items()} | \
        {k: __aux("1", v) for k, v in succinct_tree_coding(ordered_tree=l_bigger).items()}
