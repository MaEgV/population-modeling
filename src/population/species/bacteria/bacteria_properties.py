from dataclasses import dataclass, field


@dataclass
class BacteriaProperties:
    """
    A class containing properties of a bacterium that are not inherited by its children.

    Attributes
    ----------
    is_alive : bool
       Is bacteria alive or dead

    age : int
        Current age of bacteria

    Methods
    -------
    get_is_alive(self) -> bool
        Returns status of life status: alive or die

    inc_age(self) -> None
         Increment age counter

    get_age(self) -> int:
        Returns age

    die(self) -> None
        Kill the bacteria

    """
    _is_alive: bool = field(init=False, default=True)
    _age: int = field(init=False, default=0)

    def get_is_alive(self) -> bool:
        """
        True if bacteria is alive, else - False

        Returns
        -------
        bool
            Bacteria status
        """

        return self._is_alive

    def inc_age(self) -> None:

        """
        Increase age counter of bacteria
        When the age exceeds the max_life_time from the genome, the bacteria automatically dies

        Returns
        -------
        None
        """

        self._age += 1

    def get_age(self) -> int:
        """
        Getter of the age property

        Returns
        -------
        int
            age property
        """
        return self._age

    def die(self) -> None:
        """
        Changes the status to deceased

        Returns
        -------
        None
        """

        self._is_alive = False