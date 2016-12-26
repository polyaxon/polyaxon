import tensorflow as tf


def tf_template(name_):
    """This decorator wraps a method with `tf.make_template`. For example,

    Examples:
        ```python
        >>> @tf_template
        ... my_method():
        ...     # Creates variables
        ```
    """

    def template_decorator(func):
        """Inner decorator function"""

        def func_wrapper(*args, **kwargs):
            """Inner wrapper function"""
            templated_func = tf.make_template(name_, func)
            return templated_func(*args, **kwargs)

        return func_wrapper

    return template_decorator
