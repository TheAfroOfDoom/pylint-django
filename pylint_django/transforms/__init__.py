import os
import re
from astroid import MANAGER
from astroid.builder import AstroidBuilder
from astroid import nodes


def _add_transform(package_name, *class_names):
    transforms_dir = os.path.join(os.path.dirname(__file__), 'transforms')
    fake_module_path = os.path.join(transforms_dir, '%s.py' % re.sub('\.', '_', package_name))

    with open(fake_module_path) as f:
        fake_module = f.read()

    fake = AstroidBuilder(MANAGER).string_build(fake_module)

    def set_fake_locals(module):
        if module.name != package_name:
            return
        for class_name in class_names:
            module.locals[class_name] = fake.locals[class_name]

    MANAGER.register_transform(nodes.Module, set_fake_locals)


_add_transform('django.views.generic.base', 'View')
_add_transform('django.db.models', 'Model')
_add_transform('django.forms', 'Form')
