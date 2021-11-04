from dependency_injector import containers, providers

__all__ = ('KernelContainer',)


class KernelContainer(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True, ini_files=['config.ini'])
