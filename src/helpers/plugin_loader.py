import importlib
import importlib.util
import types
from pathlib import Path

from loguru import logger


class PluginLoader:
    def __init__(self, base_dir: str = "src.plugins") -> None:
        self.plugins_loaded: dict[str, types.ModuleType] = {}
        self.base_dir = base_dir

    def _check_plugin_existence(self, plugin_dir: str) -> bool:
        """
        Verifica se o plugin existe baseado no caminho fornecido
        """
        plugin = importlib.util.find_spec(plugin_dir)
        return plugin is not None

    def load_plugin(self, plugin_name: str) -> types.ModuleType | None:
        """
        Carrega o plugin, baseado no nome declarado na função e o caminho em 'base_dir'

        Return
            module ( plugin )
            None ( Caso não exista esse plugin )
        """

        full_plugin_dir = f"{self.base_dir}.{plugin_name}"
        try:
            if not self._check_plugin_existence(full_plugin_dir):
                logger.error(f"Plugin {full_plugin_dir} não encontrado")
                return None
            logger.info(f"Importando: .{plugin_name} from {self.base_dir}")
            plugin = importlib.import_module(f".{plugin_name}", package=self.base_dir)
            return plugin

        except Exception as e:
            logger.error(f"Erro ao carregar plugin: {e}")
            return None

    def load_all_plugins(self) -> dict[str, types.ModuleType]:
        """
        Lê a pasta de plugins e importa todos os arquivos .py encontrados
        Retorna um dicionário com o nome do plugin e o módulo carregado
        """
        base_dir_replaced = self.base_dir.replace(".", "/")
        plugins_dir = Path(base_dir_replaced)

        if not plugins_dir.exists():
            logger.error(f"A pasta {plugins_dir} não foi encontrada.")
            return self.plugins_loaded
        
        for file in plugins_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue

            plugin_name = file.stem
            loaded_module = self.load_plugin(plugin_name)
            logger.info(f"Carregando: {plugin_name}")

            # Mostar desc e obter atribruto dos plugins
            logger.info(getattr(loaded_module, "PLUGIN_DESC"))
            
            if loaded_module is not None:
                self.plugins_loaded[plugin_name] = loaded_module

        return self.plugins_loaded

