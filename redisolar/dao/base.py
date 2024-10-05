import abc


class SiteNotFound(Exception):
    """A Site with the given ID does not exist."""
    

class SiteDaoBas(abc.ABC):
    @abc.abstractmethod
    def insert(self, site: Site, **kwargs) -> None:
        pass