"""Joke silo for each user."""

from . import REDIS


class Silo:
    """Silo class.

    Methods:
        create_silo(session_id: str) -> None:
        repopulate_silo(session_id: str) -> None:
        include_joke(session_id: str, joke_id: str) -> None:
        exclude_joke(session_id: str, joke_id: str) -> None:
        get_jokes(session_id: str, count: int = 5) -> list:
    """
    __silo = REDIS

    @classmethod
    def create_silo(cls, session_id: str) -> None:
        """Create a new silo from a user's session.

        The joke field is to be populated with the user's preferences present
        in the user's database. If the field is empty, the joke field is
        populated with randomly generated jokes.

        Args:
            session_id: ID generated for the user's session
        """
        # TODO: Include jokes from user's permenent includes to populate silo
        cls.__silo.set(
            session_id, {'jokes': [], 'includes': [], 'excludes': []})

    @classmethod
    def destroy_silo(cls, session_id: str) -> None:
        """Destroy a silo from a user's session.

        Args:
            session_id: ID generated for the user's session
        """
        cls.__silo.delete(session_id)

    @classmethod
    def include_joke(cls, session_id: str, joke_id: str) -> None:
        """Include a joke to a user's silo.

            Args:
                session_id: ID generated for the session
                joke_id:    ID of the joke to include
        """

    @classmethod
    def exclude_joke(cls, session_id: str, joke_id: str) -> None:
        """Exclude a joke from a user's silo.

            Args:
                session_id: ID generated for the session
                joke_id:    ID of the joke to exclude
        """

    @classmethod
    def get_jokes(cls, session_id: str, count: int = 5) -> list:
        """Get the jokes avaliable for a user from the silo.

            Args:
                session_id: ID generated for the session
                count:      No of results to return
            Returns:
                List of jokes present in user's silo
            Raises:
                KeyError
        """
        obj = cls.__silo.get(session_id)

        jokes = obj[0].get('jokes', [])

        return jokes[:count]

    @classmethod
    def repopulate_jokes(cls, session_id: str) -> None:
        """Repopulate a user's joke silo

            Args:
                session_id: ID generated for the user's session
        """
        # TODO: update silo's jokes with newly generated content
