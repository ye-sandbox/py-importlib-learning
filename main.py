import importlib


def load_plugin(plugin_test):
    relative_path = f".{plugin_test}"
    base_package = "src.plugins"

    print(f"Importando: {relative_path} from {base_package}")

    module = importlib.import_module(relative_path, package=base_package)

    return module

if __name__ == "__main__":
    plugin = load_plugin("plugin_test")

    plugin.test_print()